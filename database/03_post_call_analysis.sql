-- Post-Call Analysis Database Schema
-- This file creates tables for storing meeting transcripts and analysis results

-- Table for storing meeting transcripts
CREATE TABLE IF NOT EXISTS meeting_transcripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    transcript_text TEXT NOT NULL,
    transcript_file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_size INTEGER,
    upload_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    uploaded_by UUID REFERENCES users(id),
    processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing AI analysis results from transcripts
CREATE TABLE IF NOT EXISTS transcript_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transcript_id UUID REFERENCES meeting_transcripts(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL, -- 'post_call_analysis', 'action_extraction', 'sentiment_analysis'
    
    -- Key characteristics and insights
    key_topics JSONB, -- Array of main topics discussed
    key_decisions JSONB, -- Array of decisions made
    action_items JSONB, -- Array of action items with assignments
    follow_up_items JSONB, -- Array of follow-up items
    schedule_changes JSONB, -- Array of scheduling changes mentioned
    key_insights JSONB, -- Array of important insights
    concerns_raised JSONB, -- Array of concerns or issues raised
    next_steps JSONB, -- Array of next steps planned
    
    -- Sentiment and relationship analysis
    overall_sentiment VARCHAR(50), -- positive, negative, neutral, mixed
    relationship_health_score DECIMAL(3,2), -- 0.00 to 1.00
    engagement_level VARCHAR(50), -- high, medium, low
    collaboration_quality VARCHAR(50), -- excellent, good, fair, poor
    
    -- Business metrics
    meeting_effectiveness_score DECIMAL(3,2), -- 0.00 to 1.00
    productivity_indicators JSONB, -- Various productivity metrics
    risk_factors JSONB, -- Identified risks or concerns
    
    -- AI processing metadata
    ai_model_used VARCHAR(100), -- e.g., 'gemini-2.0-flash'
    processing_time_ms INTEGER,
    confidence_score DECIMAL(3,2), -- 0.00 to 1.00
    analysis_version VARCHAR(20) DEFAULT '1.0',
    
    -- Timestamps
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing extracted action items with tracking
CREATE TABLE IF NOT EXISTS action_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES transcript_analysis(id) ON DELETE CASCADE,
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    
    -- Action item details
    title VARCHAR(500) NOT NULL,
    description TEXT,
    action_type VARCHAR(100), -- 'follow_up', 'decision', 'research', 'review', 'schedule'
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    
    -- Assignment and tracking
    assigned_to UUID REFERENCES users(id),
    assigned_to_name VARCHAR(255), -- For external participants
    assigned_by UUID REFERENCES users(id),
    
    -- Status and dates
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, cancelled
    due_date DATE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- Context and metadata
    context_notes TEXT,
    related_topics JSONB,
    estimated_effort VARCHAR(50), -- low, medium, high
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing meeting insights and learnings
CREATE TABLE IF NOT EXISTS meeting_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES transcript_analysis(id) ON DELETE CASCADE,
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    
    -- Insight details
    insight_type VARCHAR(100) NOT NULL, -- 'business_opportunity', 'risk_identified', 'process_improvement', 'relationship_insight'
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    impact_level VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    
    -- Categorization
    category VARCHAR(100), -- 'sales', 'product', 'partnership', 'operations', 'strategy'
    tags JSONB, -- Array of tags for filtering
    
    -- Business context
    business_value TEXT,
    recommended_actions JSONB,
    stakeholders JSONB, -- Array of relevant stakeholders
    
    -- Status and follow-up
    status VARCHAR(50) DEFAULT 'new', -- new, reviewed, actioned, archived
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing relationship and sentiment tracking
CREATE TABLE IF NOT EXISTS relationship_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES transcript_analysis(id) ON DELETE CASCADE,
    meeting_id UUID REFERENCES meetings(id) ON DELETE CASCADE,
    
    -- Relationship details
    participant_1_id UUID REFERENCES users(id),
    participant_1_name VARCHAR(255),
    participant_2_id UUID REFERENCES users(id),
    participant_2_name VARCHAR(255),
    
    -- Metrics
    communication_quality DECIMAL(3,2), -- 0.00 to 1.00
    collaboration_level DECIMAL(3,2), -- 0.00 to 1.00
    trust_indicators JSONB,
    conflict_indicators JSONB,
    
    -- Sentiment analysis
    overall_sentiment VARCHAR(50),
    sentiment_breakdown JSONB, -- Detailed sentiment by topic/time
    
    -- Context
    interaction_context TEXT,
    relationship_stage VARCHAR(50), -- 'new', 'developing', 'established', 'strategic'
    
    -- Timestamps
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_meeting_transcripts_meeting_id ON meeting_transcripts(meeting_id);
CREATE INDEX IF NOT EXISTS idx_meeting_transcripts_status ON meeting_transcripts(processing_status);
CREATE INDEX IF NOT EXISTS idx_meeting_transcripts_uploaded_by ON meeting_transcripts(uploaded_by);

CREATE INDEX IF NOT EXISTS idx_transcript_analysis_transcript_id ON transcript_analysis(transcript_id);
CREATE INDEX IF NOT EXISTS idx_transcript_analysis_type ON transcript_analysis(analysis_type);
CREATE INDEX IF NOT EXISTS idx_transcript_analysis_analyzed_at ON transcript_analysis(analyzed_at);

CREATE INDEX IF NOT EXISTS idx_action_items_analysis_id ON action_items(analysis_id);
CREATE INDEX IF NOT EXISTS idx_action_items_meeting_id ON action_items(meeting_id);
CREATE INDEX IF NOT EXISTS idx_action_items_assigned_to ON action_items(assigned_to);
CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status);
CREATE INDEX IF NOT EXISTS idx_action_items_due_date ON action_items(due_date);

CREATE INDEX IF NOT EXISTS idx_meeting_insights_analysis_id ON meeting_insights(analysis_id);
CREATE INDEX IF NOT EXISTS idx_meeting_insights_meeting_id ON meeting_insights(meeting_id);
CREATE INDEX IF NOT EXISTS idx_meeting_insights_type ON meeting_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_meeting_insights_status ON meeting_insights(status);

CREATE INDEX IF NOT EXISTS idx_relationship_metrics_analysis_id ON relationship_metrics(analysis_id);
CREATE INDEX IF NOT EXISTS idx_relationship_metrics_meeting_id ON relationship_metrics(meeting_id);

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_meeting_transcripts_updated_at BEFORE UPDATE ON meeting_transcripts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_transcript_analysis_updated_at BEFORE UPDATE ON transcript_analysis FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_action_items_updated_at BEFORE UPDATE ON action_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_meeting_insights_updated_at BEFORE UPDATE ON meeting_insights FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE meeting_transcripts IS 'Stores uploaded meeting transcripts and their processing status';
COMMENT ON TABLE transcript_analysis IS 'Stores AI analysis results from meeting transcripts';
COMMENT ON TABLE action_items IS 'Tracks action items extracted from meeting transcripts';
COMMENT ON TABLE meeting_insights IS 'Stores business insights and learnings from meetings';
COMMENT ON TABLE relationship_metrics IS 'Tracks relationship and sentiment metrics between participants';

COMMENT ON COLUMN transcript_analysis.key_topics IS 'JSON array of main topics discussed in the meeting';
COMMENT ON COLUMN transcript_analysis.action_items IS 'JSON array of action items with assignments and details';
COMMENT ON COLUMN transcript_analysis.schedule_changes IS 'JSON array of scheduling changes mentioned in the transcript';
COMMENT ON COLUMN transcript_analysis.relationship_health_score IS 'Overall health score of the relationship (0.00-1.00)';
COMMENT ON COLUMN transcript_analysis.meeting_effectiveness_score IS 'Overall effectiveness score of the meeting (0.00-1.00)';
 