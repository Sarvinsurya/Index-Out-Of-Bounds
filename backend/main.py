from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from typing import Dict, Any, Optional

from models import (
    MeetingRequest, MeetingBuddyResponse, ScheduleCard, ContextCard, 
    AgendaCard, FollowUpCard, TranscriptAnalysisRequest, TranscriptAnalysisResponse,
    MeetingTranscript
)
from pydantic import BaseModel
from supabase_client import supabase_client
from strands_agent import MeetingBuddyAgent
from transcript_analyzer import TranscriptAnalyzer
from post_call_analyzer import PostCallAnalyzer
import config

# Initialize FastAPI app
app = FastAPI(
    title="AI Meeting Buddy API",
    description="AI-powered meeting assistance using STRANDS agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agents
meeting_agent = MeetingBuddyAgent()
transcript_analyzer = TranscriptAnalyzer()
post_call_analyzer = PostCallAnalyzer()

# Notification Models
class MeetingScheduleRequest(BaseModel):
    title: str
    date: str
    time_slot: str
    duration: int = 60
    sender_type: str  # 'vendor' or 'distributor'
    sender_name: str

class NotificationResponse(BaseModel):
    id: str
    recipient_id: str
    sender_id: str
    notification_type: str
    title: str
    message: str
    is_read: bool
    priority: str
    created_at: str
    read_at: str = None

# NOTIFICATION ENDPOINTS

@app.post("/api/meeting/schedule-meeting")
async def schedule_meeting(request: MeetingScheduleRequest):
    """Schedule a meeting and create notifications for the other party"""
    try:
        # For now, use hardcoded user IDs from the seed data to bypass RLS issues
        # In production, you'd have proper user authentication and RLS policies
        
        if request.sender_type == 'vendor':
            sender_id = "880e8400-e29b-41d4-a716-446655440001"  # Zoho Chennai
            recipient_id = "880e8400-e29b-41d4-a716-446655440002"  # German Distributor
            recipient_name = "German Distributor Team"
        else:
            sender_id = "880e8400-e29b-41d4-a716-446655440002"  # German Distributor
            recipient_id = "880e8400-e29b-41d4-a716-446655440001"  # Zoho Chennai
            recipient_name = "Zoho Chennai Team"
        
        # Create notification for the recipient
        notification = await supabase_client.create_notification(
            recipient_id=recipient_id,
            sender_id=sender_id,
            notification_type='meeting_request',
            title=f"New Meeting Request from {request.sender_name}",
            message=f"Meeting: {request.title}\nDate: {request.date}\nTime: {request.time_slot}\nDuration: {request.duration} minutes",
            priority='high'
        )
        
        if not notification:
            raise HTTPException(
                status_code=500,
                detail="Failed to create notification"
            )
        
        return {
            "success": True,
            "message": "Meeting request sent successfully",
            "notification_id": notification['id'],
            "recipient": recipient_name
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scheduling meeting: {str(e)}"
        )

@app.get("/api/notifications/{user_type}")
async def get_notifications(user_type: str, unread_only: bool = False):
    """Get notifications for a user type (vendor/distributor)"""
    try:
        # Use hardcoded user IDs from seed data
        if user_type == 'vendor':
            user_id = "880e8400-e29b-41d4-a716-446655440001"  # Zoho Chennai
        elif user_type == 'distributor':
            user_id = "880e8400-e29b-41d4-a716-446655440002"  # German Distributor
        else:
            return {"notifications": []}
        
        notifications = await supabase_client.get_user_notifications(user_id, unread_only)
        
        return {"notifications": notifications}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching notifications: {str(e)}"
        )

@app.post("/api/notifications/{notification_id}/mark-read")
async def mark_notification_read(notification_id: str):
    """Mark a notification as read"""
    try:
        # Update notification in database
        response = supabase_client.client.table('notifications')\
            .update({
                'is_read': True,
                'read_at': datetime.now().isoformat()
            })\
            .eq('id', notification_id)\
            .execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Notification not found"
            )
        
        return {"success": True, "message": "Notification marked as read"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error marking notification as read: {str(e)}"
        )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Meeting Buddy API is running",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "api_status": "healthy",
        "agent_status": "initialized", 
        "data_files": {
            "calendar": bool(meeting_agent.calendar_data),
            "past_meetings": bool(meeting_agent.past_meetings),
            "sales_data": bool(meeting_agent.sales_data)
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/meeting/generate", response_model=MeetingBuddyResponse)
async def generate_meeting_data(request: MeetingRequest):
    """
    Main endpoint to generate all meeting data using STRANDS agent
    
    This endpoint processes the request and returns:
    - Schedule suggestions
    - Key context and insights  
    - AI-generated agenda
    - Follow-up actions status
    """
    try:
        # Prepare request data
        request_data = {
            "participants": request.participants,
            "timezone_chennai": request.timezone_chennai,
            "timezone_germany": request.timezone_germany,
            "current_time": request.current_time.isoformat() if request.current_time else datetime.now().isoformat()
        }
        
        # Generate response using STRANDS agent
        response = await meeting_agent.generate_meeting_response(request_data)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating meeting data: {str(e)}"
        )

@app.get("/api/meeting/schedule", response_model=ScheduleCard)
async def get_schedule_card():
    """Tool Call: Get Schedule Card"""
    try:
        import asyncio
        current_time = datetime.now().isoformat()
        # Add timeout to prevent hanging
        schedule_card = await asyncio.wait_for(
            meeting_agent.generate_schedule_card(current_time),
            timeout=25.0  # 25 second timeout for schedule generation
        )
        return schedule_card
        
    except asyncio.TimeoutError:
        print("⏰ Schedule endpoint timed out, returning fallback")
        # Return fallback schedule data
        return ScheduleCard(
            available_slots=[],
            best_slot=None,
            alternative_slots=[],
            timezone_info={
                "chennai": "Asia/Kolkata",
                "germany": "Europe/Berlin"
            },
            ai_status="timeout",
            fallback_used=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating schedule card: {str(e)}"
        )

@app.get("/api/meeting/context", response_model=ContextCard)
async def get_context_card():
    """Tool Call: Get Context Card"""
    try:
        context_card = await meeting_agent.generate_context_card()
        return context_card
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating context card: {str(e)}"
        )

@app.get("/api/meeting/agenda", response_model=AgendaCard)
async def get_agenda_card():
    """Tool Call: Get AI Generated Agenda Card"""
    try:
        import asyncio
        # Add timeout to prevent hanging
        agenda_card = await asyncio.wait_for(
            meeting_agent.generate_agenda_card(), 
            timeout=15.0  # 15 second timeout for AI operations
        )
        return agenda_card
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating agenda card: {str(e)}"
        )

@app.get("/api/meeting/followups", response_model=FollowUpCard)
async def get_followup_card():
    """Tool Call: Get Follow-up Card"""
    try:
        import asyncio
        # Add timeout to prevent hanging
        followup_card = await asyncio.wait_for(
            meeting_agent.generate_followup_card(), 
            timeout=15.0  # 15 second timeout for AI operations
        )
        return followup_card
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating followup card: {str(e)}"
        )

# TRANSCRIPT PROCESSING ENDPOINTS

@app.post("/api/transcript/analyze", response_model=TranscriptAnalysisResponse)
async def analyze_meeting_transcript(request: TranscriptAnalysisRequest):
    """
    Analyze meeting transcript to extract insights, action items, and scheduling changes
    
    This endpoint processes real meeting transcripts and can:
    - Extract action items and assign them to participants
    - Detect scheduling changes (e.g., "reschedule to evening 5 PM")
    - Identify key decisions and commitments
    - Analyze sentiment and relationship health
    """
    try:
        analysis = await transcript_analyzer.analyze_transcript(request)
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing transcript: {str(e)}"
        )

@app.get("/api/transcript/sample")
async def get_sample_transcript():
    """Get a sample transcript for testing the analysis"""
    try:
        sample_transcript = transcript_analyzer.create_sample_transcript()
        return sample_transcript
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating sample transcript: {str(e)}"
        )

@app.post("/api/transcript/quick-analyze")
async def quick_analyze_transcript(transcript: MeetingTranscript):
    """Quick analysis of transcript - simplified endpoint"""
    try:
        request = TranscriptAnalysisRequest(transcript=transcript)
        analysis = await transcript_analyzer.analyze_transcript(request)
        
        # Return simplified response focusing on actionable items
        return {
            "summary": analysis.meeting_summary,
            "action_items": analysis.action_items,
            "schedule_changes": analysis.schedule_changes,
            "key_decisions": analysis.decisions_made,
            "next_steps": analysis.next_meeting_suggestions,
            "analysis_confidence": analysis.analysis_confidence
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in quick analysis: {str(e)}"
        )

@app.get("/api/data/raw")
async def get_raw_data():
    """Get raw data for debugging (development only)"""
    return {
        "calendar_data": meeting_agent.calendar_data,
        "past_meetings": meeting_agent.past_meetings,
        "sales_data": meeting_agent.sales_data
    }

@app.get("/api/debug/meetings")
async def debug_meetings():
    """Debug endpoint to check meeting data from database"""
    try:
        past_meetings = await supabase_client.get_past_meetings(limit=1)
        return {
            "past_meetings": past_meetings,
            "count": len(past_meetings)
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/test/create-notification")
async def create_test_notification():
    """Create a test notification to debug the system"""
    try:
        # Try to create a notification directly
        notification_data = {
            "recipient_id": "880e8400-e29b-41d4-a716-446655440002",
            "sender_id": "880e8400-e29b-41d4-a716-446655440001",
            "notification_type": "meeting_request",
            "title": "Test Notification",
            "message": "This is a test notification",
            "priority": "high"
        }
        
        response = supabase_client.client.table('notifications').insert(notification_data).execute()
        
        return {
            "success": True,
            "message": "Test notification created",
            "notification": response.data[0] if response.data else None,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create test notification"
        }

# POST-CALL ANALYSIS ENDPOINTS

class TranscriptUploadRequest(BaseModel):
    transcript_text: str
    meeting_id: str = None
    file_name: str = None

class PostCallAnalysisResponse(BaseModel):
    success: bool
    analysis_id: Optional[str] = None
    analysis_result: Optional[Dict[str, Any]] = None
    message: str
    error: Optional[str] = None

@app.post("/api/transcript/upload", response_model=PostCallAnalysisResponse)
async def upload_and_analyze_transcript(request: TranscriptUploadRequest):
    """
    Upload meeting transcript and perform comprehensive post-call analysis
    
    This endpoint:
    - Accepts transcript text
    - Performs AI-powered analysis
    - Extracts key insights, action items, and metrics
    - Stores results in database
    - Updates follow-up items and context
    """
    try:
        print(f"📝 Processing transcript upload...")
        
        # Perform comprehensive analysis
        analysis_result = await post_call_analyzer.analyze_transcript(
            request.transcript_text, 
            request.meeting_id
        )
        
        return PostCallAnalysisResponse(
            success=True,
            analysis_id=analysis_result.get('ai_metadata', {}).get('analysis_id'),
            analysis_result=analysis_result,
            message="Transcript analyzed successfully"
        )
        
    except Exception as e:
        print(f"🚨 Transcript upload failed: {e}")
        return PostCallAnalysisResponse(
            success=False,
            message="Failed to analyze transcript",
            error=str(e)
        )

@app.get("/api/transcript/analysis/{meeting_id}")
async def get_meeting_analysis(meeting_id: str):
    """
    Get comprehensive analysis results for a specific meeting
    """
    try:
        analysis_summary = await post_call_analyzer.get_analysis_summary(meeting_id)
        return analysis_summary
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving analysis: {str(e)}"
        )

@app.get("/api/transcript/action-items/{meeting_id}")
async def get_meeting_action_items(meeting_id: str):
    """
    Get all action items for a specific meeting
    """
    try:
        response = supabase_client.client.table('action_items')\
            .select('*')\
            .eq('meeting_id', meeting_id)\
            .order('created_at', desc=True)\
            .execute()
        
        return {
            "action_items": response.data or [],
            "total_count": len(response.data or [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving action items: {str(e)}"
        )

@app.get("/api/transcript/insights/{meeting_id}")
async def get_meeting_insights(meeting_id: str):
    """
    Get all insights for a specific meeting
    """
    try:
        response = supabase_client.client.table('meeting_insights')\
            .select('*')\
            .eq('meeting_id', meeting_id)\
            .order('created_at', desc=True)\
            .execute()
        
        return {
            "insights": response.data or [],
            "total_count": len(response.data or [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving insights: {str(e)}"
        )

@app.post("/api/transcript/action-items/{action_item_id}/update-status")
async def update_action_item_status(action_item_id: str, status: str):
    """
    Update the status of an action item
    """
    try:
        response = supabase_client.client.table('action_items')\
            .update({
                'status': status,
                'updated_at': datetime.now().isoformat()
            })\
            .eq('id', action_item_id)\
            .execute()
        
        if response.data:
            return {"success": True, "message": "Action item status updated"}
        else:
            raise HTTPException(status_code=404, detail="Action item not found")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating action item: {str(e)}"
        )

@app.get("/api/transcript/analytics/dashboard")
async def get_analytics_dashboard():
    """
    Get analytics dashboard data for all meetings
    """
    try:
        # Get recent analyses
        recent_analyses = supabase_client.client.table('transcript_analysis')\
            .select('*')\
            .order('analyzed_at', desc=True)\
            .limit(10)\
            .execute()
        
        # Get action items summary
        action_items_summary = supabase_client.client.table('action_items')\
            .select('status')\
            .execute()
        
        # Get insights summary
        insights_summary = supabase_client.client.table('meeting_insights')\
            .select('insight_type, impact_level')\
            .execute()
        
        # Calculate metrics
        total_analyses = len(recent_analyses.data or [])
        total_action_items = len(action_items_summary.data or [])
        total_insights = len(insights_summary.data or [])
        
        # Calculate completion rates
        completed_actions = len([item for item in (action_items_summary.data or []) if item.get('status') == 'completed'])
        completion_rate = (completed_actions / total_action_items * 100) if total_action_items > 0 else 0
        
        return {
            "dashboard_metrics": {
                "total_analyses": total_analyses,
                "total_action_items": total_action_items,
                "total_insights": total_insights,
                "action_completion_rate": round(completion_rate, 2),
                "recent_analyses": recent_analyses.data or []
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving analytics: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG
    )
