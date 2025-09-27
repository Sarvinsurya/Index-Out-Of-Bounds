from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Request Models
class MeetingRequest(BaseModel):
    participants: List[str] = ["Zoho Chennai", "German Distributor"]
    timezone_chennai: str = "Asia/Kolkata"
    timezone_germany: str = "Europe/Berlin"
    current_time: Optional[datetime] = None

# NEW: Meeting Transcription Models
class SpeakerSegment(BaseModel):
    """Individual speaker segment in transcript"""
    speaker: str
    timestamp: str
    content: str
    confidence: float = 0.95

class MeetingTranscript(BaseModel):
    """Complete meeting transcript with speaker identification"""
    meeting_id: str
    meeting_date: datetime
    participants: List[str]
    segments: List[SpeakerSegment]
    duration_minutes: int
    transcript_confidence: float

class TranscriptAnalysisRequest(BaseModel):
    """Request to analyze meeting transcript"""
    transcript: MeetingTranscript
    analyze_actions: bool = True
    analyze_scheduling: bool = True
    analyze_decisions: bool = True

class ExtractedInsight(BaseModel):
    """Insights extracted from transcript"""
    type: str  # "action_item", "decision", "scheduling", "concern", "commitment"
    speaker: str
    content: str
    timestamp: str
    confidence: float
    requires_action: bool = False

class ScheduleChange(BaseModel):
    """Detected schedule changes from transcript"""
    old_time: Optional[str]
    new_time: str
    timezone: str
    confidence: float
    proposed_by: str
    timestamp: str

class TranscriptAnalysisResponse(BaseModel):
    """Complete analysis of meeting transcript"""
    meeting_summary: str
    key_insights: List[ExtractedInsight]
    action_items: List[Dict[str, Any]]
    decisions_made: List[Dict[str, Any]]
    schedule_changes: List[ScheduleChange]
    sentiment_analysis: Dict[str, Any]
    next_meeting_suggestions: List[str]
    analysis_confidence: float

# Response Models for the 4 Cards

class ScheduleCard(BaseModel):
    """Card 1: Instant Schedule"""
    suggested_time_ist: str
    suggested_time_cet: str
    suggested_time_utc: str
    availability_confidence: float
    alternative_slots: List[Dict[str, Any]]
    slots: List[Dict[str, Any]]  # Frontend-compatible slots with start/end
    meeting_duration: int = 60  # minutes
    ai_status: str = "active"  # "active", "quota_exceeded", "error"
    fallback_used: bool = False

class ContextCard(BaseModel):
    """Card 2: Key Context"""
    last_meeting_date: str
    last_meeting_summary: str
    key_insights: List[str]
    sales_highlights: List[Dict[str, Any]]
    relationship_status: str
    trust_score: float

class AgendaCard(BaseModel):
    """Card 3: AI Generated Agenda"""
    agenda_title: str
    estimated_duration: int
    agenda_items: List[Dict[str, Any]]
    discussion_priorities: List[str]
    suggested_outcomes: List[str]
    prep_reminders: List[str]
    ai_status: str = "active"  # "active", "quota_exceeded", "error"
    fallback_used: bool = False

class FollowUpCard(BaseModel):
    """Card 4: Follow-up from Last Meet"""
    pending_actions: List[Dict[str, Any]]
    completed_actions: List[Dict[str, Any]]
    overdue_items: List[Dict[str, Any]]
    action_completion_rate: float
    next_review_date: str
    ai_status: str = "active"  # "active", "quota_exceeded", "error"
    fallback_used: bool = False

# Complete API Response
class MeetingBuddyResponse(BaseModel):
    meeting_info: Dict[str, str]
    schedule_card: ScheduleCard
    context_card: ContextCard
    agenda_card: AgendaCard
    followup_card: FollowUpCard
    generated_at: datetime
    ai_confidence: float