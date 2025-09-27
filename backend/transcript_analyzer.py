from openai import OpenAI
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pytz
from models import (
    MeetingTranscript, SpeakerSegment, TranscriptAnalysisRequest, 
    TranscriptAnalysisResponse, ExtractedInsight, ScheduleChange
)
import config

class TranscriptAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        
    async def analyze_transcript(self, request: TranscriptAnalysisRequest) -> TranscriptAnalysisResponse:
        """Main method to analyze meeting transcript and extract insights"""
        
        transcript = request.transcript
        
        # Extract different types of insights
        insights = await self._extract_insights(transcript)
        action_items = await self._extract_action_items(transcript)
        decisions = await self._extract_decisions(transcript)
        schedule_changes = await self._detect_schedule_changes(transcript)
        sentiment = await self._analyze_sentiment(transcript)
        summary = await self._generate_summary(transcript)
        
        return TranscriptAnalysisResponse(
            meeting_summary=summary,
            key_insights=insights,
            action_items=action_items,
            decisions_made=decisions,
            schedule_changes=schedule_changes,
            sentiment_analysis=sentiment,
            next_meeting_suggestions=await self._suggest_next_meeting(transcript),
            analysis_confidence=0.85
        )
    
    async def _extract_insights(self, transcript: MeetingTranscript) -> List[ExtractedInsight]:
        """Extract key insights from transcript using AI"""
        
        # Prepare transcript text for AI analysis
        transcript_text = self._format_transcript_for_ai(transcript)
        
        prompt = f"""
        Analyze this meeting transcript and extract key insights. Look for:
        - Important decisions or commitments
        - Concerns or issues raised
        - Action items mentioned
        - Business opportunities
        - Relationship dynamics
        
        Transcript:
        {transcript_text}
        
        Return insights in this JSON format:
        {{
            "insights": [
                {{
                    "type": "decision|action_item|concern|opportunity|commitment",
                    "speaker": "speaker_name",
                    "content": "what was said",
                    "timestamp": "HH:MM",
                    "confidence": 0.95,
                    "requires_action": true/false
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return [
                ExtractedInsight(**insight) 
                for insight in result.get("insights", [])
            ]
            
        except Exception as e:
            print(f"Error extracting insights: {e}")
            return self._fallback_extract_insights(transcript)
    
    async def _detect_schedule_changes(self, transcript: MeetingTranscript) -> List[ScheduleChange]:
        """Detect scheduling changes mentioned in the conversation"""
        
        transcript_text = self._format_transcript_for_ai(transcript)
        
        # Use AI to detect schedule-related conversations
        prompt = f"""
        Analyze this meeting transcript for any mentions of scheduling changes, rescheduling, or time changes.
        Look for phrases like:
        - "Let's reschedule to..."
        - "Move the meeting to..."
        - "Can we meet at..."
        - "Change it to evening 5 PM"
        - "Next week Tuesday"
        
        Transcript:
        {transcript_text}
        
        Return schedule changes in this JSON format:
        {{
            "schedule_changes": [
                {{
                    "old_time": "current_time_if_mentioned",
                    "new_time": "2025-09-27 17:00",
                    "timezone": "IST|CET|UTC",
                    "confidence": 0.9,
                    "proposed_by": "speaker_name",
                    "timestamp": "HH:MM"
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2  # Lower temperature for factual extraction
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return [
                ScheduleChange(**change) 
                for change in result.get("schedule_changes", [])
            ]
            
        except Exception as e:
            print(f"Error detecting schedule changes: {e}")
            return self._fallback_detect_schedule_changes(transcript)
    
    async def _extract_action_items(self, transcript: MeetingTranscript) -> List[Dict[str, Any]]:
        """Extract action items from the conversation"""
        
        transcript_text = self._format_transcript_for_ai(transcript)
        
        prompt = f"""
        Extract action items from this meeting transcript. Look for:
        - Tasks assigned to specific people
        - Deadlines mentioned
        - Commitments made
        - Follow-up items
        
        Transcript:
        {transcript_text}
        
        Return action items in this JSON format:
        {{
            "action_items": [
                {{
                    "task": "Complete Q3 sales report",
                    "assignee": "German Team",
                    "due_date": "2025-10-05",
                    "priority": "high|medium|low",
                    "status": "pending",
                    "mentioned_by": "speaker_name",
                    "timestamp": "HH:MM"
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("action_items", [])
            
        except Exception as e:
            print(f"Error extracting action items: {e}")
            return []
    
    async def _extract_decisions(self, transcript: MeetingTranscript) -> List[Dict[str, Any]]:
        """Extract decisions made during the meeting"""
        
        transcript_text = self._format_transcript_for_ai(transcript)
        
        prompt = f"""
        Extract decisions made in this meeting. Look for:
        - Agreements reached
        - Plans decided
        - Budget approvals
        - Strategic directions
        
        Transcript:
        {transcript_text}
        
        Return decisions in this JSON format:
        {{
            "decisions": [
                {{
                    "decision": "Increase marketing budget by 20%",
                    "decided_by": "Chennai Team Lead",
                    "impact": "Will boost Q4 sales efforts",
                    "timestamp": "HH:MM",
                    "confidence": 0.9
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("decisions", [])
            
        except Exception as e:
            print(f"Error extracting decisions: {e}")
            return []
    
    async def _analyze_sentiment(self, transcript: MeetingTranscript) -> Dict[str, Any]:
        """Analyze the sentiment and tone of the meeting"""
        
        transcript_text = self._format_transcript_for_ai(transcript)
        
        prompt = f"""
        Analyze the sentiment and tone of this meeting transcript.
        
        Transcript:
        {transcript_text}
        
        Return sentiment analysis in this JSON format:
        {{
            "overall_sentiment": "positive|neutral|negative",
            "collaboration_score": 8.5,
            "trust_indicators": ["good communication", "agreements reached"],
            "concerns_raised": ["timeline pressure", "budget constraints"],
            "relationship_health": "strong|moderate|weak"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "overall_sentiment": "neutral",
                "collaboration_score": 7.0,
                "trust_indicators": [],
                "concerns_raised": [],
                "relationship_health": "moderate"
            }
    
    async def _generate_summary(self, transcript: MeetingTranscript) -> str:
        """Generate a concise summary of the meeting"""
        
        transcript_text = self._format_transcript_for_ai(transcript)
        
        prompt = f"""
        Generate a concise 2-3 sentence summary of this meeting transcript.
        Focus on the main topics discussed and key outcomes.
        
        Transcript:
        {transcript_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Meeting focused on business performance and strategic planning."
    
    async def _suggest_next_meeting(self, transcript: MeetingTranscript) -> List[str]:
        """Suggest topics for the next meeting based on this conversation"""
        
        return [
            "Follow up on action items from this meeting",
            "Review progress on Q4 targets",
            "Discuss upcoming product launches",
            "Address any outstanding concerns"
        ]
    
    def _format_transcript_for_ai(self, transcript: MeetingTranscript) -> str:
        """Format transcript for AI analysis"""
        
        formatted_lines = []
        for segment in transcript.segments:
            formatted_lines.append(f"[{segment.timestamp}] {segment.speaker}: {segment.content}")
        
        return "\n".join(formatted_lines)
    
    def _fallback_extract_insights(self, transcript: MeetingTranscript) -> List[ExtractedInsight]:
        """Fallback insight extraction using rule-based approach"""
        
        insights = []
        
        for segment in transcript.segments:
            content_lower = segment.content.lower()
            
            # Simple rule-based detection
            if any(word in content_lower for word in ["decide", "agree", "confirm"]):
                insights.append(ExtractedInsight(
                    type="decision",
                    speaker=segment.speaker,
                    content=segment.content,
                    timestamp=segment.timestamp,
                    confidence=0.7,
                    requires_action=False
                ))
            
            elif any(word in content_lower for word in ["action", "task", "will do", "responsible"]):
                insights.append(ExtractedInsight(
                    type="action_item",
                    speaker=segment.speaker,
                    content=segment.content,
                    timestamp=segment.timestamp,
                    confidence=0.7,
                    requires_action=True
                ))
        
        return insights
    
    def _fallback_detect_schedule_changes(self, transcript: MeetingTranscript) -> List[ScheduleChange]:
        """Fallback schedule detection using regex patterns"""
        
        schedule_changes = []
        
        # Regex patterns for common scheduling phrases
        patterns = [
            r"reschedule.*?(\d{1,2}:?\d{0,2})\s*(am|pm|AM|PM)",
            r"move.*?meeting.*?(\d{1,2}:?\d{0,2})\s*(am|pm|AM|PM)",
            r"change.*?to.*?(\d{1,2}:?\d{0,2})\s*(am|pm|AM|PM)",
            r"evening\s*(\d{1,2})\s*(pm|PM)"
        ]
        
        for segment in transcript.segments:
            for pattern in patterns:
                matches = re.finditer(pattern, segment.content, re.IGNORECASE)
                for match in matches:
                    time_str = match.group(1)
                    period = match.group(2) if len(match.groups()) > 1 else "PM"
                    
                    schedule_changes.append(ScheduleChange(
                        old_time=None,
                        new_time=f"2025-09-27 {time_str} {period}",
                        timezone="IST",
                        confidence=0.8,
                        proposed_by=segment.speaker,
                        timestamp=segment.timestamp
                    ))
        
        return schedule_changes

    def create_sample_transcript(self) -> MeetingTranscript:
        """Create a sample transcript for testing"""
        
        segments = [
            SpeakerSegment(
                speaker="Chennai Team Lead",
                timestamp="10:00",
                content="Good morning everyone. Let's start with our Q3 performance review.",
                confidence=0.95
            ),
            SpeakerSegment(
                speaker="German Distributor",
                timestamp="10:01",
                content="Thanks for organizing this. We've seen some challenges with Zoho Workplace sales this quarter.",
                confidence=0.93
            ),
            SpeakerSegment(
                speaker="Chennai Team Lead",
                timestamp="10:02",
                content="Yes, we noticed that too. We should focus on improving our competitive positioning. I'll prepare a detailed analysis by next Friday.",
                confidence=0.96
            ),
            SpeakerSegment(
                speaker="German Distributor",
                timestamp="10:03",
                content="That would be great. Also, can we reschedule our next meeting to evening 5 PM? That works better for our team.",
                confidence=0.94
            ),
            SpeakerSegment(
                speaker="Chennai Team Lead",
                timestamp="10:04",
                content="Sure, evening 5 PM works perfectly. I'll send out a calendar update. We also need to discuss the Q4 marketing budget increase.",
                confidence=0.97
            ),
            SpeakerSegment(
                speaker="German Distributor",
                timestamp="10:05",
                content="Perfect. Let's approve the 20% budget increase as discussed. Our team will provide the Q3 regional breakdown by Monday.",
                confidence=0.95
            )
        ]
        
        return MeetingTranscript(
            meeting_id="meeting_20250926",
            meeting_date=datetime.now(),
            participants=["Chennai Team Lead", "German Distributor"],
            segments=segments,
            duration_minutes=30,
            transcript_confidence=0.94
        )
