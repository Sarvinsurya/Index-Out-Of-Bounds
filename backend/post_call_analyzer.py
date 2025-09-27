"""
Post-Call Analysis Module
Advanced AI-powered analysis of meeting transcripts to extract key insights,
action items, and relationship metrics.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from models import TranscriptAnalysisRequest, TranscriptAnalysisResponse
import config
from supabase_client import supabase_client


class PostCallAnalyzer:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.base_url = config.OPENAI_BASE_URL
        self.model_name = config.AI_MODEL
        
        # Check if using Gemini API
        self.is_gemini = 'generativelanguage.googleapis.com' in self.base_url
        
        # Analysis prompts
        self.SYSTEM_PROMPT = """
You are an advanced AI system for comprehensive meeting transcript analysis.
Your task is to extract structured data from meeting transcripts and provide actionable insights.

Extract the following information:
1. Key topics and decisions discussed
2. Action items with assignments and priorities
3. Follow-up items and next steps
4. Schedule changes mentioned
5. Business insights and opportunities
6. Relationship and sentiment analysis
7. Risk factors and concerns

Return a single valid JSON object with all extracted information.
"""

        self.USER_PROMPT_TEMPLATE = """
Analyze the following meeting transcript and extract comprehensive insights.

Transcript:
---
{transcript}
---

Return a JSON object with this exact structure:
{{
    "key_topics": [
        {{"topic": "string", "importance": "high|medium|low", "discussion_time": "string"}}
    ],
    "key_decisions": [
        {{"decision": "string", "impact": "high|medium|low", "stakeholders": ["string"]}}
    ],
    "action_items": [
        {{
            "title": "string",
            "description": "string",
            "assigned_to": "string",
            "priority": "high|medium|low",
            "due_date": "YYYY-MM-DD or null",
            "action_type": "follow_up|decision|research|review|schedule"
        }}
    ],
    "follow_up_items": [
        {{"item": "string", "priority": "high|medium|low", "timeline": "string"}}
    ],
    "schedule_changes": [
        {{"change": "string", "new_time": "string", "reason": "string"}}
    ],
    "key_insights": [
        {{"insight": "string", "category": "business_opportunity|risk|process_improvement", "impact": "high|medium|low"}}
    ],
    "concerns_raised": [
        {{"concern": "string", "severity": "high|medium|low", "stakeholder": "string"}}
    ],
    "next_steps": [
        {{"step": "string", "owner": "string", "timeline": "string"}}
    ],
    "sentiment_analysis": {{
        "overall_sentiment": "positive|negative|neutral|mixed",
        "relationship_health_score": 0.85,
        "engagement_level": "high|medium|low",
        "collaboration_quality": "excellent|good|fair|poor"
    }},
    "business_metrics": {{
        "meeting_effectiveness_score": 0.80,
        "productivity_indicators": {{
            "decisions_made": 3,
            "action_items_created": 5,
            "issues_resolved": 2
        }},
        "risk_factors": [
            {{"risk": "string", "severity": "high|medium|low", "mitigation": "string"}}
        ]
    }}
}}
"""

    async def _make_ai_call(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make AI API call using either OpenAI-compatible or Gemini API"""
        if self.is_gemini:
            return await self._make_gemini_call(prompt, max_tokens)
        else:
            return await self._make_openai_call(prompt, max_tokens)
    
    async def _make_gemini_call(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make API call to Gemini"""
        import aiohttp
        
        url = f"{self.base_url}/models/{self.model_name}:generateContent"
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [{
                'parts': [{'text': prompt}]
            }],
            'generationConfig': {
                'maxOutputTokens': max_tokens,
                'temperature': 0.3
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{url}?key={self.api_key}", 
                                  headers=headers, 
                                  json=data, 
                                  timeout=60) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    return content
                else:
                    error_text = await response.text()
                    raise Exception(f"Gemini API Error {response.status}: {error_text}")
    
    async def _make_openai_call(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make API call to OpenAI-compatible API"""
        from openai import OpenAI
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    async def analyze_transcript(self, transcript_text: str, meeting_id: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of meeting transcript
        """
        try:
            print(f" Starting post-call analysis with {self.model_name}...")
            
            # Prepare the prompt
            user_prompt = self.USER_PROMPT_TEMPLATE.format(transcript=transcript_text)
            
            # Make AI call
            start_time = datetime.now()
            ai_response = await self._make_ai_call(user_prompt, 2000)
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            print(f"🤖 AI analysis completed in {processing_time:.0f}ms")
            
            # Parse AI response
            analysis_result = self._parse_ai_response(ai_response)
            
            # Add metadata
            analysis_result['ai_metadata'] = {
                'model_used': self.model_name,
                'processing_time_ms': int(processing_time),
                'confidence_score': 0.85,  # Could be calculated based on response quality
                'analysis_version': '1.0',
                'analyzed_at': datetime.now().isoformat()
            }
            
            # Store in database if meeting_id provided
            if meeting_id:
                await self._store_analysis_results(analysis_result, meeting_id, transcript_text)
            
            return analysis_result
            
        except Exception as e:
            print(f"🚨 Post-call analysis failed: {e}")
            return self._get_fallback_analysis(transcript_text)

    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        try:
            # Clean up response
            response_text = ai_response.strip()
            
            # Remove markdown formatting if present
            if '```json' in response_text:
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            # Parse JSON
            analysis_data = json.loads(response_text)
            
            # Validate and clean data
            return self._validate_analysis_data(analysis_data)
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {ai_response[:500]}...")
            return self._get_fallback_analysis("")
        except Exception as e:
            print(f"⚠️ Error parsing AI response: {e}")
            return self._get_fallback_analysis("")

    def _validate_analysis_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean analysis data"""
        # Ensure all required fields exist with proper structure
        validated_data = {
            'key_topics': data.get('key_topics', []),
            'key_decisions': data.get('key_decisions', []),
            'action_items': data.get('action_items', []),
            'follow_up_items': data.get('follow_up_items', []),
            'schedule_changes': data.get('schedule_changes', []),
            'key_insights': data.get('key_insights', []),
            'concerns_raised': data.get('concerns_raised', []),
            'next_steps': data.get('next_steps', []),
            'sentiment_analysis': data.get('sentiment_analysis', {
                'overall_sentiment': 'neutral',
                'relationship_health_score': 0.5,
                'engagement_level': 'medium',
                'collaboration_quality': 'good'
            }),
            'business_metrics': data.get('business_metrics', {
                'meeting_effectiveness_score': 0.5,
                'productivity_indicators': {},
                'risk_factors': []
            })
        }
        
        return validated_data

    def _get_fallback_analysis(self, transcript_text: str) -> Dict[str, Any]:
        """Provide fallback analysis when AI fails"""
        return {
            'key_topics': [
                {'topic': 'General Discussion', 'importance': 'medium', 'discussion_time': 'N/A'}
            ],
            'key_decisions': [],
            'action_items': [],
            'follow_up_items': [],
            'schedule_changes': [],
            'key_insights': [
                {'insight': 'Meeting transcript processed with fallback analysis', 'category': 'process_improvement', 'impact': 'low'}
            ],
            'concerns_raised': [],
            'next_steps': [],
            'sentiment_analysis': {
                'overall_sentiment': 'neutral',
                'relationship_health_score': 0.5,
                'engagement_level': 'medium',
                'collaboration_quality': 'good'
            },
            'business_metrics': {
                'meeting_effectiveness_score': 0.5,
                'productivity_indicators': {},
                'risk_factors': []
            },
            'ai_metadata': {
                'model_used': 'fallback',
                'processing_time_ms': 0,
                'confidence_score': 0.3,
                'analysis_version': '1.0',
                'analyzed_at': datetime.now().isoformat()
            }
        }

    async def _store_analysis_results(self, analysis_result: Dict[str, Any], meeting_id: str, transcript_text: str):
        """Store analysis results in database"""
        try:
            # First, store the transcript
            transcript_data = {
                'meeting_id': meeting_id,
                'transcript_text': transcript_text,
                'processing_status': 'completed',
                'uploaded_by': 'system'  # Could be actual user ID
            }
            
            transcript_response = supabase_client.client.table('meeting_transcripts').insert(transcript_data).execute()
            
            if transcript_response.data:
                transcript_id = transcript_response.data[0]['id']
                
                # Store the analysis
                analysis_data = {
                    'transcript_id': transcript_id,
                    'analysis_type': 'post_call_analysis',
                    'key_topics': analysis_result.get('key_topics', []),
                    'key_decisions': analysis_result.get('key_decisions', []),
                    'action_items': analysis_result.get('action_items', []),
                    'follow_up_items': analysis_result.get('follow_up_items', []),
                    'schedule_changes': analysis_result.get('schedule_changes', []),
                    'key_insights': analysis_result.get('key_insights', []),
                    'concerns_raised': analysis_result.get('concerns_raised', []),
                    'next_steps': analysis_result.get('next_steps', []),
                    'overall_sentiment': analysis_result.get('sentiment_analysis', {}).get('overall_sentiment', 'neutral'),
                    'relationship_health_score': analysis_result.get('sentiment_analysis', {}).get('relationship_health_score', 0.5),
                    'engagement_level': analysis_result.get('sentiment_analysis', {}).get('engagement_level', 'medium'),
                    'collaboration_quality': analysis_result.get('sentiment_analysis', {}).get('collaboration_quality', 'good'),
                    'meeting_effectiveness_score': analysis_result.get('business_metrics', {}).get('meeting_effectiveness_score', 0.5),
                    'productivity_indicators': analysis_result.get('business_metrics', {}).get('productivity_indicators', {}),
                    'risk_factors': analysis_result.get('business_metrics', {}).get('risk_factors', []),
                    'ai_model_used': analysis_result.get('ai_metadata', {}).get('model_used', 'unknown'),
                    'processing_time_ms': analysis_result.get('ai_metadata', {}).get('processing_time_ms', 0),
                    'confidence_score': analysis_result.get('ai_metadata', {}).get('confidence_score', 0.5)
                }
                
                analysis_response = supabase_client.client.table('transcript_analysis').insert(analysis_data).execute()
                
                if analysis_response.data:
                    analysis_id = analysis_response.data[0]['id']
                    
                    # Store action items separately for tracking
                    await self._store_action_items(analysis_result.get('action_items', []), analysis_id, meeting_id)
                    
                    # Store insights separately
                    await self._store_meeting_insights(analysis_result.get('key_insights', []), analysis_id, meeting_id)
                    
                    print(f"✅ Analysis results stored in database (ID: {analysis_id})")
                else:
                    print("⚠️ Failed to store analysis results")
            else:
                print("⚠️ Failed to store transcript")
                
        except Exception as e:
            print(f"🚨 Error storing analysis results: {e}")

    async def _store_action_items(self, action_items: List[Dict], analysis_id: str, meeting_id: str):
        """Store action items in database"""
        try:
            for item in action_items:
                action_data = {
                    'analysis_id': analysis_id,
                    'meeting_id': meeting_id,
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'action_type': item.get('action_type', 'follow_up'),
                    'priority': item.get('priority', 'medium'),
                    'assigned_to_name': item.get('assigned_to', ''),
                    'due_date': item.get('due_date'),
                    'status': 'pending',
                    'context_notes': f"Extracted from transcript analysis"
                }
                
                supabase_client.client.table('action_items').insert(action_data).execute()
                
        except Exception as e:
            print(f"🚨 Error storing action items: {e}")

    async def _store_meeting_insights(self, insights: List[Dict], analysis_id: str, meeting_id: str):
        """Store meeting insights in database"""
        try:
            for insight in insights:
                insight_data = {
                    'analysis_id': analysis_id,
                    'meeting_id': meeting_id,
                    'insight_type': insight.get('category', 'business_opportunity'),
                    'title': insight.get('insight', '')[:500],  # Truncate if too long
                    'description': insight.get('insight', ''),
                    'impact_level': insight.get('impact', 'medium'),
                    'status': 'new'
                }
                
                supabase_client.client.table('meeting_insights').insert(insight_data).execute()
                
        except Exception as e:
            print(f"🚨 Error storing meeting insights: {e}")

    async def get_analysis_summary(self, meeting_id: str) -> Dict[str, Any]:
        """Get summary of analysis results for a meeting"""
        try:
            # Get latest analysis for the meeting
            response = supabase_client.client.table('transcript_analysis')\
                .select('*, meeting_transcripts!inner(meeting_id)')\
                .eq('meeting_transcripts.meeting_id', meeting_id)\
                .order('analyzed_at', desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                analysis = response.data[0]
                
                # Get action items
                action_items_response = supabase_client.client.table('action_items')\
                    .select('*')\
                    .eq('analysis_id', analysis['id'])\
                    .execute()
                
                # Get insights
                insights_response = supabase_client.client.table('meeting_insights')\
                    .select('*')\
                    .eq('analysis_id', analysis['id'])\
                    .execute()
                
                return {
                    'analysis': analysis,
                    'action_items': action_items_response.data or [],
                    'insights': insights_response.data or [],
                    'summary': {
                        'total_action_items': len(action_items_response.data or []),
                        'total_insights': len(insights_response.data or []),
                        'relationship_health': analysis.get('relationship_health_score', 0.5),
                        'meeting_effectiveness': analysis.get('meeting_effectiveness_score', 0.5),
                        'overall_sentiment': analysis.get('overall_sentiment', 'neutral')
                    }
                }
            else:
                return {'error': 'No analysis found for this meeting'}
                
        except Exception as e:
            print(f"🚨 Error getting analysis summary: {e}")
            return {'error': str(e)}
