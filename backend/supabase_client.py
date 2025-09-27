"""
Supabase Client Configuration for AI Meeting Buddy
Handles database connections and operations
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime, date
import json

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client with configuration"""
        self.supabase_url = "https://pbigwnpzvduzjodjfntm.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBiaWd3bnB6dmR1empvZGpmbnRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MDU0NzUsImV4cCI6MjA3NDQ4MTQ3NX0.1xi5vjO-2eACQ78jeRDNyBN2Z8NgCYcYD-vlO7_lVQ8"
        
        # Create Supabase client
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    # =====================================================
    # USER MANAGEMENT
    # =====================================================
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user details by ID"""
        try:
            response = self.client.table('users').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    async def get_users_by_type(self, user_type: str) -> List[Dict]:
        """Get all users of a specific type (vendor/distributor)"""
        try:
            response = self.client.table('users').select('*').eq('user_type', user_type).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching users by type: {e}")
            return []
    
    # =====================================================
    # MEETING MANAGEMENT
    # =====================================================
    
    async def get_past_meetings(self, limit: int = 10) -> List[Dict]:
        """Get past meetings with all related data"""
        try:
            response = self.client.table('meetings')\
                .select('''
                    *,
                    meeting_topics(*),
                    meeting_decisions(*),
                    action_items(*),
                    meeting_effectiveness(*)
                ''')\
                .eq('status', 'completed')\
                .order('meeting_date', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error fetching past meetings: {e}")
            return []
    
    async def create_meeting(self, meeting_data: Dict) -> Optional[Dict]:
        """Create a new meeting"""
        try:
            response = self.client.table('meetings').insert(meeting_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating meeting: {e}")
            return None
    
    async def get_meeting_by_id(self, meeting_id: str) -> Optional[Dict]:
        """Get meeting with all related data"""
        try:
            response = self.client.table('meetings')\
                .select('''
                    *,
                    meeting_topics(*),
                    meeting_decisions(*),
                    action_items(*),
                    meeting_effectiveness(*)
                ''')\
                .eq('id', meeting_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching meeting: {e}")
            return None
    
    # =====================================================
    # CALENDAR & AVAILABILITY
    # =====================================================
    
    async def get_calendar_availability(self, user_id: str, date_str: str) -> List[Dict]:
        """Get calendar availability for a user on a specific date"""
        try:
            response = self.client.table('calendar_availability')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('date', date_str)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error fetching calendar availability: {e}")
            return []
    
    async def get_team_availability(self, team_type: str, date_str: str) -> Dict:
        """Get availability for entire team (vendor/distributor)"""
        try:
            # Get users of the team type
            users = await self.get_users_by_type(team_type)
            if not users:
                return {}
            
            # For simplicity, get availability for the first user of each type
            # In production, you'd aggregate availability for all team members
            user_id = users[0]['id']
            availability = await self.get_calendar_availability(user_id, date_str)
            
            # Convert to the format expected by the existing code
            busy_slots = []
            working_hours = {"start": "09:00", "end": "18:00"}  # Default
            
            for slot in availability:
                if slot['is_busy']:
                    # Handle both string and datetime objects
                    start_time = slot['start_time']
                    end_time = slot['end_time']
                    
                    if isinstance(start_time, str):
                        # If it's already a string, use it directly
                        start_str = start_time
                        end_str = end_time
                    else:
                        # If it's a datetime object, format it
                        start_str = start_time.strftime('%H:%M')
                        end_str = end_time.strftime('%H:%M')
                    
                    busy_slots.append({
                        "start": start_str,
                        "end": end_str
                    })
            
            return {
                "date": date_str,
                "busy_slots": busy_slots,
                "working_hours": working_hours
            }
        except Exception as e:
            print(f"Error fetching team availability: {e}")
            return {}
    
    # =====================================================
    # SALES DATA
    # =====================================================
    
    async def get_sales_performance(self, quarter: str = "Q3 2025") -> Dict:
        """Get sales performance data"""
        try:
            # Get sales performance
            sales_response = self.client.table('sales_performance')\
                .select('''
                    *,
                    products(product_id, product_name)
                ''')\
                .eq('quarter', quarter)\
                .execute()
            
            # Get key customers
            customers_response = self.client.table('key_customers')\
                .select('''
                    *,
                    products(product_id, product_name)
                ''')\
                .execute()
            
            # Get regional sales
            regional_response = self.client.table('regional_sales')\
                .select('*')\
                .eq('quarter', quarter)\
                .execute()
            
            # Transform to match existing JSON structure
            products = []
            total_revenue = 0
            total_target = 0
            
            for sale in sales_response.data:
                product_data = {
                    "product_id": sale['products']['product_id'],
                    "product_name": sale['products']['product_name'],
                    "q3_sales": float(sale['sales_amount']),
                    "target": float(sale['target_amount']),
                    "achievement_percent": float(sale['achievement_percent']),
                    "growth_rate": float(sale['growth_rate']),
                    "key_customers": [],
                    "regional_breakdown": {}
                }
                
                # Add key customers for this product
                product_customers = [c for c in customers_response.data if c['products']['product_id'] == sale['products']['product_id']]
                product_data['key_customers'] = [c['customer_name'] for c in product_customers]
                
                # Add regional breakdown
                product_regional = [r for r in regional_response.data if r['product_id'] == sale['product_id']]
                for region in product_regional:
                    product_data['regional_breakdown'][region['sub_region']] = float(region['sales_amount'])
                
                products.append(product_data)
                total_revenue += float(sale['sales_amount'])
                total_target += float(sale['target_amount'])
            
            return {
                "sales_performance": {
                    "current_quarter": quarter,
                    "region": "Germany",
                    "products": products,
                    "total_revenue": total_revenue,
                    "total_target": total_target,
                    "overall_achievement": round((total_revenue / total_target) * 100, 1) if total_target > 0 else 0
                }
            }
        except Exception as e:
            print(f"Error fetching sales data: {e}")
            return {}
    
    # =====================================================
    # ACTION ITEMS & FOLLOW-UPS
    # =====================================================
    
    async def get_action_items(self) -> Dict:
        """Get action items categorized by status"""
        try:
            response = self.client.table('action_items')\
                .select('*')\
                .order('due_date', desc=False)\
                .execute()
            
            pending_actions = []
            completed_actions = []
            overdue_items = []
            
            total_items = len(response.data)
            completed_count = 0
            
            for item in response.data:
                action_data = {
                    "id": item['id'],
                    "assignee": item['assignee_name'],
                    "task": item['task'],
                    "due_date": item['due_date'],
                    "status": item['status'],
                    "priority": item['priority']
                }
                
                if item['status'] == 'completed':
                    completed_actions.append(action_data)
                    completed_count += 1
                elif item['status'] == 'overdue':
                    overdue_items.append(action_data)
                else:
                    pending_actions.append(action_data)
            
            completion_rate = (completed_count / total_items * 100) if total_items > 0 else 0
            
            return {
                "pending_actions": pending_actions,
                "completed_actions": completed_actions,
                "overdue_items": overdue_items,
                "action_completion_rate": round(completion_rate, 1),
                "next_review_date": "2025-10-01"  # Could be calculated based on pending items
            }
        except Exception as e:
            print(f"Error fetching action items: {e}")
            return {
                "pending_actions": [],
                "completed_actions": [],
                "overdue_items": [],
                "action_completion_rate": 0.0,
                "next_review_date": "2025-10-01"
            }
    
    # =====================================================
    # PARTNERSHIP METRICS
    # =====================================================
    
    async def get_partnership_metrics(self) -> Dict:
        """Get partnership metrics and relationship data"""
        try:
            response = self.client.table('partnership_metrics')\
                .select('*')\
                .execute()
            
            if not response.data:
                return {}
            
            metrics = response.data[0]  # Assuming one partnership for now
            
            return {
                "total_meetings": metrics['total_meetings'],
                "average_effectiveness": float(metrics['average_effectiveness']),
                "action_completion_rate": float(metrics['action_completion_rate']),
                "trust_score": float(metrics['trust_score']),
                "relationship_status": metrics['relationship_status'],
                "partnership_duration_months": self._calculate_partnership_duration(metrics['partnership_start_date'])
            }
        except Exception as e:
            print(f"Error fetching partnership metrics: {e}")
            return {}
    
    def _calculate_partnership_duration(self, start_date: str) -> int:
        """Calculate partnership duration in months"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            today = date.today()
            months = (today.year - start.year) * 12 + (today.month - start.month)
            return max(months, 0)
        except:
            return 0
    
    # =====================================================
    # AI PROCESSING LOGS
    # =====================================================
    
    async def log_ai_processing(self, operation_type: str, ai_model: str, ai_status: str, 
                              fallback_used: bool = False, processing_time_ms: int = 0, 
                              confidence_score: float = 0.0, error_message: str = None):
        """Log AI processing operation"""
        try:
            log_data = {
                "operation_type": operation_type,
                "ai_model": ai_model,
                "ai_status": ai_status,
                "fallback_used": fallback_used,
                "processing_time_ms": processing_time_ms,
                "confidence_score": confidence_score,
                "error_message": error_message
            }
            
            self.client.table('ai_processing_logs').insert(log_data).execute()
        except Exception as e:
            print(f"Error logging AI processing: {e}")
    
    # =====================================================
    # NOTIFICATIONS
    # =====================================================
    
    async def create_notification(self, recipient_id: str, sender_id: str, 
                                notification_type: str, title: str, message: str, 
                                priority: str = "normal"):
        """Create a new notification"""
        try:
            notification_data = {
                "recipient_id": recipient_id,
                "sender_id": sender_id,
                "notification_type": notification_type,
                "title": title,
                "message": message,
                "priority": priority
            }
            
            response = self.client.table('notifications').insert(notification_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
    
    async def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        """Get notifications for a user"""
        try:
            query = self.client.table('notifications').select('*').eq('recipient_id', user_id)
            
            if unread_only:
                query = query.eq('is_read', False)
            
            response = query.order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching notifications: {e}")
            return []
    
    # =====================================================
    # UTILITY METHODS
    # =====================================================
    
    async def update_partnership_metrics(self, trust_score: float, relationship_status: str):
        """Update partnership metrics with new AI-calculated values"""
        try:
            update_data = {
                "trust_score": trust_score,
                "relationship_status": relationship_status,
                "last_calculated_at": datetime.now().isoformat()
            }
            
            # Update the first (and likely only) partnership record
            response = self.client.table('partnership_metrics')\
                .update(update_data)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating partnership metrics: {e}")
            return None
    
    async def get_system_config(self, config_key: str) -> Optional[str]:
        """Get system configuration value"""
        try:
            response = self.client.table('system_config')\
                .select('config_value')\
                .eq('config_key', config_key)\
                .execute()
            
            return response.data[0]['config_value'] if response.data else None
        except Exception as e:
            print(f"Error fetching system config: {e}")
            return None

# Global instance
supabase_client = SupabaseClient()
