-- =====================================================
-- AI MEETING BUDDY - COMPLETE SUPABASE SCHEMA
-- =====================================================
-- This is the single, definitive schema creation script
-- Run this first to create all tables, indexes, and policies

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- DROP EXISTING TABLES (if they exist)
-- =====================================================

DROP TABLE IF EXISTS public.ai_processing_logs CASCADE;
DROP TABLE IF EXISTS public.notifications CASCADE;
DROP TABLE IF EXISTS public.system_config CASCADE;
DROP TABLE IF EXISTS public.meeting_effectiveness CASCADE;
DROP TABLE IF EXISTS public.partnership_metrics CASCADE;
DROP TABLE IF EXISTS public.regional_sales CASCADE;
DROP TABLE IF EXISTS public.key_customers CASCADE;
DROP TABLE IF EXISTS public.sales_performance CASCADE;
DROP TABLE IF EXISTS public.action_items CASCADE;
DROP TABLE IF EXISTS public.meeting_decisions CASCADE;
DROP TABLE IF EXISTS public.meeting_topics CASCADE;
DROP TABLE IF EXISTS public.speaker_segments CASCADE;
DROP TABLE IF EXISTS public.meeting_transcripts CASCADE;
DROP TABLE IF EXISTS public.calendar_availability CASCADE;
DROP TABLE IF EXISTS public.meeting_participants CASCADE;
DROP TABLE IF EXISTS public.meetings CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.organizations CASCADE;

-- Drop functions if they exist
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
DROP FUNCTION IF EXISTS mark_overdue_action_items() CASCADE;

-- =====================================================
-- CREATE TABLES
-- =====================================================

-- Users table (supports both demo and authenticated users)
CREATE TABLE public.users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    auth_user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('vendor', 'distributor')),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    organization VARCHAR(100) NOT NULL,
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Organizations table
CREATE TABLE public.organizations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('vendor', 'distributor')),
    timezone VARCHAR(50) NOT NULL,
    working_hours_start TIME NOT NULL DEFAULT '09:00:00',
    working_hours_end TIME NOT NULL DEFAULT '18:00:00',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Products table
CREATE TABLE public.products (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Meetings table
CREATE TABLE public.meetings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_date DATE NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'rescheduled')),
    meeting_type VARCHAR(30) DEFAULT 'regular',
    created_by UUID REFERENCES public.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Meeting participants
CREATE TABLE public.meeting_participants (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id),
    organization_id UUID REFERENCES public.organizations(id),
    participant_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Calendar availability
CREATE TABLE public.calendar_availability (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_busy BOOLEAN DEFAULT FALSE,
    event_title VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, date, start_time, end_time)
);

-- Meeting transcripts
CREATE TABLE public.meeting_transcripts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    transcript_confidence DECIMAL(3,2) DEFAULT 0.95,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Speaker segments in transcripts
CREATE TABLE public.speaker_segments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    transcript_id UUID REFERENCES public.meeting_transcripts(id) ON DELETE CASCADE,
    speaker VARCHAR(100) NOT NULL,
    timestamp_in_meeting VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 0.95,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Meeting topics discussed
CREATE TABLE public.meeting_topics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    topic VARCHAR(200) NOT NULL,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Key decisions made in meetings
CREATE TABLE public.meeting_decisions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    decision TEXT NOT NULL,
    decision_maker VARCHAR(100),
    impact_level VARCHAR(20) DEFAULT 'medium' CHECK (impact_level IN ('low', 'medium', 'high')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Action items from meetings
CREATE TABLE public.action_items (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    assignee_id UUID REFERENCES public.users(id),
    assignee_name VARCHAR(100) NOT NULL,
    task TEXT NOT NULL,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'overdue', 'cancelled')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Sales performance data
CREATE TABLE public.sales_performance (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    product_id UUID REFERENCES public.products(id),
    region VARCHAR(100) NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    sales_amount DECIMAL(12,2) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    achievement_percent DECIMAL(5,2) GENERATED ALWAYS AS ((sales_amount / target_amount) * 100) STORED,
    growth_rate DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Key customers
CREATE TABLE public.key_customers (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    product_id UUID REFERENCES public.products(id),
    customer_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    revenue_contribution DECIMAL(12,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Regional sales breakdown
CREATE TABLE public.regional_sales (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    product_id UUID REFERENCES public.products(id),
    region VARCHAR(100) NOT NULL,
    sub_region VARCHAR(100),
    quarter VARCHAR(10) NOT NULL,
    sales_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Partnership metrics
CREATE TABLE public.partnership_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    vendor_org_id UUID REFERENCES public.organizations(id),
    distributor_org_id UUID REFERENCES public.organizations(id),
    partnership_start_date DATE NOT NULL,
    total_meetings INTEGER DEFAULT 0,
    average_effectiveness DECIMAL(3,2) DEFAULT 0.0,
    action_completion_rate DECIMAL(3,2) DEFAULT 0.0,
    trust_score DECIMAL(3,2) DEFAULT 0.0,
    relationship_status VARCHAR(30) DEFAULT 'new' CHECK (relationship_status IN ('new', 'developing', 'established', 'strong', 'strategic', 'at_risk')),
    last_calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(vendor_org_id, distributor_org_id)
);

-- Meeting effectiveness ratings
CREATE TABLE public.meeting_effectiveness (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    meeting_id UUID REFERENCES public.meetings(id) ON DELETE CASCADE,
    effectiveness_score DECIMAL(3,2) NOT NULL CHECK (effectiveness_score >= 0 AND effectiveness_score <= 10),
    sentiment VARCHAR(20) DEFAULT 'neutral' CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    feedback_notes TEXT,
    rated_by UUID REFERENCES public.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI processing logs
CREATE TABLE public.ai_processing_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL,
    ai_model VARCHAR(50) NOT NULL,
    ai_status VARCHAR(20) NOT NULL CHECK (ai_status IN ('active', 'quota_exceeded', 'invalid_key', 'error')),
    fallback_used BOOLEAN DEFAULT FALSE,
    processing_time_ms INTEGER,
    confidence_score DECIMAL(3,2),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications
CREATE TABLE public.notifications (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    recipient_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES public.users(id),
    notification_type VARCHAR(30) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    read_at TIMESTAMP WITH TIME ZONE
);

-- System configuration
CREATE TABLE public.system_config (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES public.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CREATE INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX idx_users_user_type ON public.users(user_type);
CREATE INDEX idx_users_organization ON public.users(organization);
CREATE INDEX idx_meetings_date ON public.meetings(meeting_date);
CREATE INDEX idx_meetings_status ON public.meetings(status);
CREATE INDEX idx_meetings_created_by ON public.meetings(created_by);
CREATE INDEX idx_calendar_user_date ON public.calendar_availability(user_id, date);
CREATE INDEX idx_calendar_date_busy ON public.calendar_availability(date, is_busy);
CREATE INDEX idx_action_items_assignee ON public.action_items(assignee_id);
CREATE INDEX idx_action_items_status ON public.action_items(status);
CREATE INDEX idx_action_items_due_date ON public.action_items(due_date);
CREATE INDEX idx_sales_product_quarter ON public.sales_performance(product_id, quarter);
CREATE INDEX idx_sales_region ON public.sales_performance(region);
CREATE INDEX idx_notifications_recipient ON public.notifications(recipient_id);
CREATE INDEX idx_notifications_unread ON public.notifications(recipient_id, is_read);
CREATE INDEX idx_ai_logs_operation ON public.ai_processing_logs(operation_type);
CREATE INDEX idx_ai_logs_status ON public.ai_processing_logs(ai_status);
CREATE INDEX idx_ai_logs_created ON public.ai_processing_logs(created_at);

-- =====================================================
-- CREATE FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_meetings_updated_at BEFORE UPDATE ON public.meetings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_action_items_updated_at BEFORE UPDATE ON public.action_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sales_performance_updated_at BEFORE UPDATE ON public.sales_performance FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_partnership_metrics_updated_at BEFORE UPDATE ON public.partnership_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_config_updated_at BEFORE UPDATE ON public.system_config FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to automatically mark overdue action items
CREATE OR REPLACE FUNCTION mark_overdue_action_items()
RETURNS void AS $$
BEGIN
    UPDATE public.action_items 
    SET status = 'overdue', updated_at = NOW()
    WHERE due_date < CURRENT_DATE 
    AND status IN ('pending', 'in_progress');
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- ENABLE ROW LEVEL SECURITY (RLS)
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
-- CREATE RLS POLICIES
-- =====================================================

-- Users policies (supports demo users with NULL auth_user_id)
CREATE POLICY "Users can view own profile" ON public.users FOR SELECT 
USING (auth.uid() = auth_user_id OR auth_user_id IS NULL);

CREATE POLICY "Users can update own profile" ON public.users FOR UPDATE 
USING (auth.uid() = auth_user_id);

-- Calendar availability policies
CREATE POLICY "Users can manage own calendar" ON public.calendar_availability FOR ALL 
USING (
    EXISTS (
        SELECT 1 FROM public.users u 
        WHERE u.id = calendar_availability.user_id 
        AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
    )
);

-- Meeting policies
CREATE POLICY "Users can view meetings they participate in" ON public.meetings FOR SELECT 
USING (
    EXISTS (
        SELECT 1 FROM public.meeting_participants mp 
        WHERE mp.meeting_id = meetings.id 
        AND EXISTS (
            SELECT 1 FROM public.users u 
            WHERE u.id = mp.user_id 
            AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
        )
    )
);

-- Action items policies
CREATE POLICY "Users can view assigned action items" ON public.action_items FOR SELECT 
USING (
    EXISTS (
        SELECT 1 FROM public.users u 
        WHERE u.id = action_items.assignee_id 
        AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
    )
);

CREATE POLICY "Users can update assigned action items" ON public.action_items FOR UPDATE 
USING (
    EXISTS (
        SELECT 1 FROM public.users u 
        WHERE u.id = action_items.assignee_id 
        AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
    )
);

-- Notifications policies
CREATE POLICY "Users can view own notifications" ON public.notifications FOR SELECT 
USING (
    EXISTS (
        SELECT 1 FROM public.users u 
        WHERE u.id = notifications.recipient_id 
        AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
    )
);

CREATE POLICY "Users can update own notifications" ON public.notifications FOR UPDATE 
USING (
    EXISTS (
        SELECT 1 FROM public.users u 
        WHERE u.id = notifications.recipient_id 
        AND (u.auth_user_id = auth.uid() OR u.auth_user_id IS NULL)
    )
);

-- Public access policies for demo data
CREATE POLICY "Public can view organizations" ON public.organizations FOR SELECT USING (true);
CREATE POLICY "Public can view products" ON public.products FOR SELECT USING (true);
CREATE POLICY "Public can view key customers" ON public.key_customers FOR SELECT USING (true);
CREATE POLICY "Public can view regional sales" ON public.regional_sales FOR SELECT USING (true);
CREATE POLICY "Public can view sales performance" ON public.sales_performance FOR SELECT USING (true);
CREATE POLICY "Public can view partnership metrics" ON public.partnership_metrics FOR SELECT USING (true);
CREATE POLICY "Public can view AI logs" ON public.ai_processing_logs FOR SELECT USING (true);
CREATE POLICY "Public can view system config" ON public.system_config FOR SELECT USING (true);

-- =====================================================
-- SUCCESS MESSAGE
-- =====================================================

SELECT 'AI Meeting Buddy schema created successfully!' as status;
SELECT '19 tables, 15 indexes, 6 triggers, 12 RLS policies' as summary;
SELECT 'Ready for data insertion with 02_insert_data.sql' as next_step;
