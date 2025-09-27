#!/usr/bin/env python3
"""
Demo script for Post-Call Analysis functionality
Tests the new transcript analysis endpoints and features
"""

import asyncio
import json
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Sample meeting transcript for testing
SAMPLE_TRANSCRIPT = """
Meeting Transcript - Product Strategy Discussion
Date: 2024-01-15
Participants: Sarah (Product Manager), Mike (Engineering Lead), Lisa (Design Lead), Tom (Sales Director)

Sarah: Good morning everyone. Thanks for joining today's product strategy meeting. Let's start by reviewing our Q1 roadmap.

Mike: I've been working on the new user dashboard feature. We're about 80% complete, but we've hit some performance issues with the data loading. I think we need to push the release date by two weeks.

Lisa: That's concerning. The design is ready, but if we delay, we'll miss the marketing campaign launch. Can we prioritize the performance optimization?

Tom: From a sales perspective, this dashboard is critical for our enterprise deals. We have three prospects waiting for this feature. A delay could cost us significant revenue.

Sarah: Let's address this systematically. Mike, what specific performance issues are we seeing?

Mike: The main issue is with the real-time data sync. When users have large datasets, the dashboard becomes unresponsive. We need to implement pagination and lazy loading.

Lisa: I can help redesign the loading states to make the experience smoother while the data loads.

Tom: What if we release a beta version to our top prospects? That way we can get feedback and still meet some of the sales commitments.

Sarah: That's a good compromise. Let's create an action plan:
1. Mike will focus on the performance optimization - target completion in 10 days
2. Lisa will design the loading states and beta feedback collection
3. Tom will coordinate with prospects for beta testing
4. We'll schedule a follow-up meeting next Friday to review progress

Mike: Sounds good. I'll also need to coordinate with the DevOps team for the deployment pipeline changes.

Lisa: I'm concerned about the user experience during the beta phase. We should have a clear rollback plan if issues arise.

Tom: Agreed. I'll draft a beta agreement that sets clear expectations with our prospects.

Sarah: Excellent. Let's also discuss the Q2 roadmap. I've been thinking about the mobile app integration.

Mike: The mobile team is ready to start, but we need the API endpoints finalized first.

Lisa: I have some initial mockups for the mobile interface. Should we schedule a design review session?

Tom: Mobile is becoming increasingly important for our enterprise clients. I'd like to be involved in the design decisions.

Sarah: Perfect. Let's schedule the mobile design review for next Tuesday. Mike, can you provide the API specifications by then?

Mike: Yes, I'll have the first draft ready by Monday.

Lisa: I'll prepare the mobile mockups and user flow diagrams.

Tom: I'll gather feedback from our enterprise clients about their mobile requirements.

Sarah: Great. One more thing - I've been hearing concerns about our customer support response times. This is affecting our customer satisfaction scores.

Mike: The support team mentioned they're overwhelmed with technical questions. Maybe we need better documentation.

Lisa: I can help create user guides and FAQ sections.

Tom: From a sales perspective, good support is crucial for renewals. We should prioritize this.

Sarah: Let's add this to our action items:
5. Create comprehensive user documentation
6. Implement a knowledge base system
7. Train support team on new features

Mike: I can work with the support team to identify the most common technical issues.

Lisa: I'll create visual guides and video tutorials.

Tom: I'll coordinate with customer success to understand the pain points.

Sarah: Excellent. Let's wrap up with next steps. Everyone has clear action items, and we have follow-up meetings scheduled. Any other concerns?

Mike: Just want to confirm - the performance optimization is our top priority, right?

Sarah: Yes, absolutely. That's blocking everything else.

Lisa: I'm excited about the mobile project. I think it will really differentiate us in the market.

Tom: The beta approach for the dashboard is smart. It shows we're responsive to customer needs.

Sarah: Perfect. Thanks everyone for the productive discussion. Let's reconvene next Friday to review progress. Have a great week!

Meeting ended at 10:45 AM.
"""

def test_transcript_upload():
    """Test the transcript upload and analysis endpoint"""
    print("🧪 Testing Post-Call Analysis - Transcript Upload")
    print("=" * 60)
    
    # Test data
    test_data = {
        "transcript_text": SAMPLE_TRANSCRIPT,
        "meeting_id": "demo-meeting-001",
        "file_name": "product_strategy_meeting.txt"
    }
    
    try:
        print("📤 Uploading transcript for analysis...")
        response = requests.post(
            f"{API_BASE}/transcript/upload",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcript uploaded successfully!")
            print(f"📊 Analysis ID: {result.get('analysis_id', 'N/A')}")
            print(f"💬 Message: {result.get('message', 'N/A')}")
            
            # Display analysis results
            analysis_result = result.get('analysis_result', {})
            if analysis_result:
                print("\n📈 Analysis Results:")
                print("-" * 40)
                
                # Sentiment Analysis
                sentiment = analysis_result.get('sentiment_analysis', {})
                print(f"🎭 Overall Sentiment: {sentiment.get('overall_sentiment', 'N/A')}")
                print(f"💚 Relationship Health: {sentiment.get('relationship_health_score', 0) * 100:.0f}%")
                print(f"📊 Meeting Effectiveness: {analysis_result.get('business_metrics', {}).get('meeting_effectiveness_score', 0) * 100:.0f}%")
                
                # Key Topics
                topics = analysis_result.get('key_topics', [])
                if topics:
                    print(f"\n📋 Key Topics ({len(topics)}):")
                    for i, topic in enumerate(topics[:3], 1):
                        print(f"  {i}. {topic.get('topic', 'N/A')} ({topic.get('importance', 'N/A')})")
                
                # Action Items
                actions = analysis_result.get('action_items', [])
                if actions:
                    print(f"\n✅ Action Items ({len(actions)}):")
                    for i, action in enumerate(actions[:3], 1):
                        print(f"  {i}. {action.get('title', 'N/A')} - {action.get('assigned_to', 'Unassigned')}")
                
                # Key Insights
                insights = analysis_result.get('key_insights', [])
                if insights:
                    print(f"\n💡 Key Insights ({len(insights)}):")
                    for i, insight in enumerate(insights[:2], 1):
                        print(f"  {i}. {insight.get('insight', 'N/A')} ({insight.get('impact', 'N/A')})")
            
            return result.get('analysis_id')
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
        return None
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")
        return None

def test_meeting_analysis(meeting_id):
    """Test getting analysis results for a meeting"""
    print(f"\n🔍 Testing Meeting Analysis Retrieval")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/transcript/analysis/{meeting_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis retrieved successfully!")
            
            if 'error' in result:
                print(f"⚠️ {result['error']}")
            else:
                summary = result.get('summary', {})
                print(f"📊 Summary:")
                print(f"  - Total Action Items: {summary.get('total_action_items', 0)}")
                print(f"  - Total Insights: {summary.get('total_insights', 0)}")
                print(f"  - Relationship Health: {summary.get('relationship_health', 0) * 100:.0f}%")
                print(f"  - Overall Sentiment: {summary.get('overall_sentiment', 'N/A')}")
        else:
            print(f"❌ Analysis retrieval failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")

def test_action_items(meeting_id):
    """Test getting action items for a meeting"""
    print(f"\n📝 Testing Action Items Retrieval")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/transcript/action-items/{meeting_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Action items retrieved successfully!")
            
            action_items = result.get('action_items', [])
            total_count = result.get('total_count', 0)
            
            print(f"📋 Total Action Items: {total_count}")
            
            if action_items:
                print("\nAction Items:")
                for i, item in enumerate(action_items[:3], 1):
                    print(f"  {i}. {item.get('title', 'N/A')}")
                    print(f"     Status: {item.get('status', 'N/A')}")
                    print(f"     Priority: {item.get('priority', 'N/A')}")
                    if item.get('assigned_to_name'):
                        print(f"     Assigned to: {item.get('assigned_to_name')}")
                    print()
        else:
            print(f"❌ Action items retrieval failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")

def test_insights(meeting_id):
    """Test getting insights for a meeting"""
    print(f"\n💡 Testing Insights Retrieval")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/transcript/insights/{meeting_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Insights retrieved successfully!")
            
            insights = result.get('insights', [])
            total_count = result.get('total_count', 0)
            
            print(f"💡 Total Insights: {total_count}")
            
            if insights:
                print("\nKey Insights:")
                for i, insight in enumerate(insights[:3], 1):
                    print(f"  {i}. {insight.get('title', 'N/A')}")
                    print(f"     Type: {insight.get('insight_type', 'N/A')}")
                    print(f"     Impact: {insight.get('impact_level', 'N/A')}")
                    print()
        else:
            print(f"❌ Insights retrieval failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")

def test_analytics_dashboard():
    """Test the analytics dashboard endpoint"""
    print(f"\n📊 Testing Analytics Dashboard")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE}/transcript/analytics/dashboard")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analytics dashboard retrieved successfully!")
            
            metrics = result.get('dashboard_metrics', {})
            print(f"📈 Dashboard Metrics:")
            print(f"  - Total Analyses: {metrics.get('total_analyses', 0)}")
            print(f"  - Total Action Items: {metrics.get('total_action_items', 0)}")
            print(f"  - Total Insights: {metrics.get('total_insights', 0)}")
            print(f"  - Action Completion Rate: {metrics.get('action_completion_rate', 0)}%")
        else:
            print(f"❌ Analytics dashboard failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
    except Exception as e:
        print(f"🚨 Unexpected error: {e}")

def main():
    """Run all post-call analysis tests"""
    print("🚀 Post-Call Analysis Demo")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Upload and analyze transcript
    analysis_id = test_transcript_upload()
    
    if analysis_id:
        meeting_id = "demo-meeting-001"
        
        # Test 2: Get meeting analysis
        test_meeting_analysis(meeting_id)
        
        # Test 3: Get action items
        test_action_items(meeting_id)
        
        # Test 4: Get insights
        test_insights(meeting_id)
        
        # Test 5: Analytics dashboard
        test_analytics_dashboard()
    
    print("\n🎉 Post-Call Analysis Demo Complete!")
    print("=" * 60)
    print("✅ All tests completed")
    print("📊 Check the database for stored analysis results")
    print("🌐 Visit http://localhost:3000/upload-transcript to test the UI")

if __name__ == "__main__":
    main()
