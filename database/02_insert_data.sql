-- =====================================================
-- AI MEETING BUDDY - COMPLETE DATA INSERTION
-- =====================================================
-- This is the single, definitive data insertion script
-- Run this after 01_create_schema.sql to populate all tables

-- Temporarily disable RLS for data insertion
ALTER TABLE public.users DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.organizations DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meetings DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_participants DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.calendar_availability DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_transcripts DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.speaker_segments DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_topics DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_decisions DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.action_items DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.products DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.sales_performance DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.key_customers DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.regional_sales DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.partnership_metrics DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_effectiveness DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_processing_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_config DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- INSERT CORE DATA
-- =====================================================

-- 1. Organizations
INSERT INTO public.organizations (id, name, type, timezone, working_hours_start, working_hours_end) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Zoho Chennai', 'vendor', 'Asia/Kolkata', '09:00:00', '18:00:00'),
('550e8400-e29b-41d4-a716-446655440002', 'German Distributor', 'distributor', 'Europe/Berlin', '08:00:00', '17:00:00');

-- 2. Products
INSERT INTO public.products (id, product_id, product_name, category) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'ZOHO_CRM_ENTERPRISE', 'Zoho CRM Enterprise', 'CRM'),
('660e8400-e29b-41d4-a716-446655440002', 'ZOHO_WORKPLACE', 'Zoho Workplace', 'Productivity'),
('660e8400-e29b-41d4-a716-446655440003', 'ZOHO_ANALYTICS', 'Zoho Analytics', 'Analytics');

-- 3. Demo Users (auth_user_id is NULL for demo purposes)
INSERT INTO public.users (id, auth_user_id, user_type, name, email, organization, timezone) VALUES
('880e8400-e29b-41d4-a716-446655440001', NULL, 'vendor', 'Chennai Team Lead', 'chennai@zoho.com', 'Zoho Chennai', 'Asia/Kolkata'),
('880e8400-e29b-41d4-a716-446655440002', NULL, 'distributor', 'German Team Lead', 'germany@distributor.com', 'German Distributor', 'Europe/Berlin');

-- =====================================================
-- INSERT SALES DATA
-- =====================================================

-- 4. Sales Performance (Q3 2025)
INSERT INTO public.sales_performance (product_id, region, quarter, sales_amount, target_amount, growth_rate) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'Germany', 'Q3 2025', 145000.00, 150000.00, 9.8),
('660e8400-e29b-41d4-a716-446655440002', 'Germany', 'Q3 2025', 89000.00, 100000.00, -6.3),
('660e8400-e29b-41d4-a716-446655440003', 'Germany', 'Q3 2025', 76000.00, 80000.00, 11.8);

-- 5. Key Customers
INSERT INTO public.key_customers (product_id, customer_name, region, revenue_contribution) VALUES
-- Zoho CRM Enterprise customers
('660e8400-e29b-41d4-a716-446655440001', 'BMW Group', 'Germany', 48000.00),
('660e8400-e29b-41d4-a716-446655440001', 'SAP', 'Germany', 52000.00),
('660e8400-e29b-41d4-a716-446655440001', 'Volkswagen', 'Germany', 45000.00),
-- Zoho Workplace customers
('660e8400-e29b-41d4-a716-446655440002', 'Deutsche Bank', 'Germany', 32000.00),
('660e8400-e29b-41d4-a716-446655440002', 'Siemens', 'Germany', 28000.00),
('660e8400-e29b-41d4-a716-446655440002', 'Bosch', 'Germany', 29000.00),
-- Zoho Analytics customers
('660e8400-e29b-41d4-a716-446655440003', 'Mercedes-Benz', 'Germany', 28000.00),
('660e8400-e29b-41d4-a716-446655440003', 'Lufthansa', 'Germany', 25000.00),
('660e8400-e29b-41d4-a716-446655440003', 'BASF', 'Germany', 23000.00);

-- 6. Regional Sales Breakdown
INSERT INTO public.regional_sales (product_id, region, sub_region, quarter, sales_amount) VALUES
-- Zoho CRM Enterprise
('660e8400-e29b-41d4-a716-446655440001', 'Germany', 'Bavaria', 'Q3 2025', 65000.00),
('660e8400-e29b-41d4-a716-446655440001', 'Germany', 'North Rhine-Westphalia', 'Q3 2025', 48000.00),
('660e8400-e29b-41d4-a716-446655440001', 'Germany', 'Baden-Württemberg', 'Q3 2025', 32000.00),
-- Zoho Workplace
('660e8400-e29b-41d4-a716-446655440002', 'Germany', 'Bavaria', 'Q3 2025', 35000.00),
('660e8400-e29b-41d4-a716-446655440002', 'Germany', 'North Rhine-Westphalia', 'Q3 2025', 28000.00),
('660e8400-e29b-41d4-a716-446655440002', 'Germany', 'Baden-Württemberg', 'Q3 2025', 26000.00),
-- Zoho Analytics
('660e8400-e29b-41d4-a716-446655440003', 'Germany', 'Bavaria', 'Q3 2025', 28000.00),
('660e8400-e29b-41d4-a716-446655440003', 'Germany', 'North Rhine-Westphalia', 'Q3 2025', 25000.00),
('660e8400-e29b-41d4-a716-446655440003', 'Germany', 'Baden-Württemberg', 'Q3 2025', 23000.00);

-- =====================================================
-- INSERT MEETING DATA
-- =====================================================

-- 7. Partnership Metrics
INSERT INTO public.partnership_metrics (
    vendor_org_id, distributor_org_id, partnership_start_date, 
    total_meetings, average_effectiveness, action_completion_rate, 
    trust_score, relationship_status
) VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440002',
    '2024-03-15', 15, 7.8, 0.82, 8.4, 'strong'
);

-- 8. Sample Meetings
INSERT INTO public.meetings (id, meeting_date, start_time, end_time, duration_minutes, status, created_by, created_at) VALUES
('770e8400-e29b-41d4-a716-446655440001', '2025-08-15', '2025-08-15 14:30:00+05:30', '2025-08-15 15:30:00+05:30', 60, 'completed', '880e8400-e29b-41d4-a716-446655440001', '2025-08-10 10:00:00+00:00'),
('770e8400-e29b-41d4-a716-446655440002', '2025-07-20', '2025-07-20 15:00:00+05:30', '2025-07-20 16:15:00+05:30', 75, 'completed', '880e8400-e29b-41d4-a716-446655440002', '2025-07-15 09:00:00+00:00');

-- 9. Meeting Participants
INSERT INTO public.meeting_participants (meeting_id, user_id, organization_id, participant_type) VALUES
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'vendor'),
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', 'distributor'),
('770e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'vendor'),
('770e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', 'distributor');

-- 10. Meeting Topics
INSERT INTO public.meeting_topics (meeting_id, topic, priority) VALUES
-- Meeting 1 topics
('770e8400-e29b-41d4-a716-446655440001', 'Q3 Sales Performance Review', 1),
('770e8400-e29b-41d4-a716-446655440001', 'Product X Launch Strategy', 2),
('770e8400-e29b-41d4-a716-446655440001', 'Customer Feedback from Bavaria Region', 3),
('770e8400-e29b-41d4-a716-446655440001', 'Q4 Marketing Campaign Planning', 4),
-- Meeting 2 topics
('770e8400-e29b-41d4-a716-446655440002', 'Mid-year performance review', 1),
('770e8400-e29b-41d4-a716-446655440002', 'Product roadmap discussion', 2),
('770e8400-e29b-41d4-a716-446655440002', 'Partnership expansion opportunities', 3),
('770e8400-e29b-41d4-a716-446655440002', 'Technical support issues', 4);

-- 11. Meeting Decisions
INSERT INTO public.meeting_decisions (meeting_id, decision, decision_maker, impact_level) VALUES
-- Meeting 1 decisions
('770e8400-e29b-41d4-a716-446655440001', 'Increase marketing budget for Product X by 20%', 'Zoho Chennai Team', 'high'),
('770e8400-e29b-41d4-a716-446655440001', 'Focus on enterprise customers in Q4', 'Joint Decision', 'high'),
('770e8400-e29b-41d4-a716-446655440001', 'Weekly sync calls during product launch', 'German Team', 'medium'),
-- Meeting 2 decisions
('770e8400-e29b-41d4-a716-446655440002', 'Expand partnership to Austria market', 'Joint Decision', 'high'),
('770e8400-e29b-41d4-a716-446655440002', 'Implement new support ticketing system', 'Zoho Chennai Team', 'medium'),
('770e8400-e29b-41d4-a716-446655440002', 'Monthly technical training sessions', 'German Team', 'medium');

-- 12. Action Items
INSERT INTO public.action_items (meeting_id, assignee_id, assignee_name, task, due_date, status, priority) VALUES
-- Completed action items
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440002', 'German Team', 'Provide detailed customer feedback report', '2025-08-30', 'completed', 'high'),
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440001', 'Chennai Team', 'Prepare Product X training materials', '2025-09-01', 'completed', 'high'),
('770e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440001', 'Chennai Team', 'Research Austria market requirements', '2025-08-05', 'completed', 'high'),
('770e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440002', 'German Team', 'Set up support ticketing system', '2025-08-15', 'completed', 'medium'),
-- Overdue action items
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440002', 'German Team', 'Share Q3 regional sales breakdown', '2025-09-15', 'overdue', 'medium'),
-- Pending action items
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440001', 'Chennai Team', 'Finalize Q4 marketing strategy document', '2025-10-01', 'pending', 'high'),
('770e8400-e29b-41d4-a716-446655440002', '880e8400-e29b-41d4-a716-446655440001', 'Chennai Team', 'Develop Austria market entry plan', '2025-10-15', 'pending', 'high'),
-- In progress action items
('770e8400-e29b-41d4-a716-446655440001', '880e8400-e29b-41d4-a716-446655440002', 'German Team', 'Conduct customer satisfaction survey', '2025-09-30', 'in_progress', 'medium');

-- 13. Meeting Effectiveness Ratings
INSERT INTO public.meeting_effectiveness (meeting_id, effectiveness_score, sentiment, feedback_notes, rated_by) VALUES
('770e8400-e29b-41d4-a716-446655440001', 8.5, 'positive', 'Very productive meeting with clear action items and good collaboration', '880e8400-e29b-41d4-a716-446655440001'),
('770e8400-e29b-41d4-a716-446655440002', 7.2, 'neutral', 'Good discussion but some topics need follow-up', '880e8400-e29b-41d4-a716-446655440002');

-- =====================================================
-- INSERT CALENDAR & SYSTEM DATA
-- =====================================================

-- 14. Calendar Availability (next 3 days)
INSERT INTO public.calendar_availability (user_id, date, start_time, end_time, is_busy, event_title) VALUES
-- Chennai Team busy slots
('880e8400-e29b-41d4-a716-446655440001', '2025-09-27', '09:00:00', '10:30:00', true, 'Team Standup'),
('880e8400-e29b-41d4-a716-446655440001', '2025-09-27', '14:00:00', '15:30:00', true, 'Product Review'),
('880e8400-e29b-41d4-a716-446655440001', '2025-09-27', '16:00:00', '17:00:00', true, 'Client Call'),
('880e8400-e29b-41d4-a716-446655440001', '2025-09-28', '10:00:00', '11:00:00', true, 'Sprint Planning'),
('880e8400-e29b-41d4-a716-446655440001', '2025-09-28', '15:00:00', '16:30:00', true, 'Technical Discussion'),
-- German Team busy slots
('880e8400-e29b-41d4-a716-446655440002', '2025-09-27', '09:00:00', '10:00:00', true, 'Morning Briefing'),
('880e8400-e29b-41d4-a716-446655440002', '2025-09-27', '11:30:00', '12:30:00', true, 'Customer Meeting'),
('880e8400-e29b-41d4-a716-446655440002', '2025-09-27', '14:00:00', '15:30:00', true, 'Sales Review');

-- 15. System Configuration
INSERT INTO public.system_config (config_key, config_value, description) VALUES
('ai_model_primary', 'deepseek/deepseek-chat', 'Primary AI model for processing'),
('ai_model_fallback', 'business_intelligence', 'Fallback when AI is unavailable'),
('default_meeting_duration', '60', 'Default meeting duration in minutes'),
('trust_score_weights', '{"meeting_effectiveness": 0.25, "action_completion": 0.20, "business_performance": 0.20, "partnership_longevity": 0.15, "communication_quality": 0.10, "revenue_achievement": 0.10}', 'Weights for trust score calculation'),
('working_hours_buffer', '30', 'Buffer time in minutes before/after working hours'),
('max_ai_retries', '3', 'Maximum retries for AI API calls'),
('notification_retention_days', '30', 'Days to keep notifications');

-- 16. AI Processing Logs (sample data)
INSERT INTO public.ai_processing_logs (operation_type, ai_model, ai_status, fallback_used, processing_time_ms, confidence_score) VALUES
('scheduling', 'deepseek/deepseek-chat', 'active', false, 1250, 0.92),
('trust_calculation', 'deepseek/deepseek-chat', 'active', false, 890, 0.88),
('agenda_generation', 'deepseek/deepseek-chat', 'active', false, 1450, 0.91),
('followup_analysis', 'business_intelligence', 'quota_exceeded', true, 45, 0.85);

-- =====================================================
-- RE-ENABLE ROW LEVEL SECURITY
-- =====================================================

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meetings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.calendar_availability ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_transcripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.speaker_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.action_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sales_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.key_customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.regional_sales ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.partnership_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meeting_effectiveness ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_processing_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_config ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- VERIFY DATA INSERTION
-- =====================================================

SELECT 'Data insertion completed successfully!' as status;

-- Show record counts for verification
SELECT 'RECORD COUNTS:' as summary;
SELECT 'Users' as table_name, count(*) as records FROM public.users
UNION ALL
SELECT 'Organizations', count(*) FROM public.organizations
UNION ALL
SELECT 'Products', count(*) FROM public.products
UNION ALL
SELECT 'Meetings', count(*) FROM public.meetings
UNION ALL
SELECT 'Action Items', count(*) FROM public.action_items
UNION ALL
SELECT 'Sales Performance', count(*) FROM public.sales_performance
UNION ALL
SELECT 'Partnership Metrics', count(*) FROM public.partnership_metrics
UNION ALL
SELECT 'Calendar Availability', count(*) FROM public.calendar_availability
UNION ALL
SELECT 'System Config', count(*) FROM public.system_config
ORDER BY table_name;

SELECT 'AI Meeting Buddy database is ready for use!' as final_status;
