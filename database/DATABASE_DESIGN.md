# 🗄️ AI Meeting Buddy - Supabase Database Design

## 📋 **OVERVIEW**

This document outlines the comprehensive database schema for the AI Meeting Buddy application using Supabase PostgreSQL. The design supports all current features while providing scalability for future enhancements.

## 🎯 **DESIGN PRINCIPLES**

1. **Data Integrity**: Foreign key constraints and proper relationships
2. **Performance**: Strategic indexing for common queries
3. **Security**: Row Level Security (RLS) policies for data protection
4. **Scalability**: Normalized structure supporting growth
5. **AI Integration**: Dedicated tables for AI processing and metrics
6. **Audit Trail**: Timestamps and change tracking

## 📊 **DATABASE SCHEMA OVERVIEW**

### **Core Entity Relationships:**
```
Users ←→ Organizations ←→ Meetings ←→ Action Items
  ↓           ↓              ↓           ↓
Calendar   Sales Data   Transcripts  Follow-ups
  ↓           ↓              ↓           ↓
Availability Metrics   AI Insights  Notifications
```

## 🗂️ **TABLE DESCRIPTIONS & JUSTIFICATIONS**

### **1. AUTHENTICATION & USER MANAGEMENT**

#### `users` Table
**Purpose**: Extends Supabase auth.users with application-specific data
**Justification**: Needed to store user roles (vendor/distributor), organization info, and preferences

| Column | Type | Purpose |
|--------|------|---------|
| `id` | UUID | Links to Supabase auth.users |
| `user_type` | VARCHAR | Vendor or distributor role |
| `name` | VARCHAR | Display name |
| `organization` | VARCHAR | Company/team name |
| `timezone` | VARCHAR | User's timezone for scheduling |

#### `organizations` Table
**Purpose**: Manages vendor and distributor organizations
**Justification**: Supports multi-tenant architecture and organization-specific settings

| Column | Type | Purpose |
|--------|------|---------|
| `name` | VARCHAR | Organization name |
| `type` | VARCHAR | Vendor or distributor |
| `timezone` | VARCHAR | Organization timezone |
| `working_hours_*` | TIME | Business hours for scheduling |

### **2. MEETING MANAGEMENT**

#### `meetings` Table
**Purpose**: Core meeting records with scheduling information
**Justification**: Central entity for all meeting-related data and relationships

| Column | Type | Purpose |
|--------|------|---------|
| `meeting_date` | DATE | Meeting date |
| `start_time` | TIMESTAMPTZ | Meeting start with timezone |
| `end_time` | TIMESTAMPTZ | Meeting end with timezone |
| `status` | VARCHAR | Scheduled, completed, cancelled |
| `duration_minutes` | INTEGER | Meeting length |

#### `meeting_participants` Table
**Purpose**: Links users to meetings (many-to-many relationship)
**Justification**: Supports meetings with multiple participants from different organizations

#### `calendar_availability` Table
**Purpose**: Stores individual calendar busy/free slots
**Justification**: Replaces JSON file with queryable, user-specific availability data

| Column | Type | Purpose |
|--------|------|---------|
| `user_id` | UUID | Owner of the calendar slot |
| `date` | DATE | Calendar date |
| `start_time` | TIME | Slot start time |
| `end_time` | TIME | Slot end time |
| `is_busy` | BOOLEAN | Busy or free slot |

### **3. MEETING CONTENT & ANALYSIS**

#### `meeting_transcripts` Table
**Purpose**: Stores AI-processed meeting transcripts
**Justification**: Enables transcript analysis, search, and AI insights generation

#### `speaker_segments` Table
**Purpose**: Individual speaker contributions within transcripts
**Justification**: Supports speaker identification, sentiment analysis, and detailed transcript processing

#### `meeting_topics` Table
**Purpose**: Topics discussed in each meeting
**Justification**: Replaces JSON array with queryable, prioritized topics for better analysis

#### `meeting_decisions` Table
**Purpose**: Key decisions made during meetings
**Justification**: Tracks decision-making process and impact levels for follow-up

### **4. ACTION ITEMS & FOLLOW-UPS**

#### `action_items` Table
**Purpose**: Tasks assigned during meetings with tracking
**Justification**: Replaces JSON structure with full CRUD operations, status tracking, and due date management

| Column | Type | Purpose |
|--------|------|---------|
| `assignee_id` | UUID | Person responsible |
| `task` | TEXT | Action description |
| `due_date` | DATE | Deadline |
| `status` | VARCHAR | Pending, completed, overdue |
| `priority` | VARCHAR | Task priority level |

### **5. SALES & BUSINESS INTELLIGENCE**

#### `products` Table
**Purpose**: Master list of Zoho products
**Justification**: Normalizes product data and supports product-specific analytics

#### `sales_performance` Table
**Purpose**: Quarterly sales data by product and region
**Justification**: Replaces JSON with queryable sales metrics for AI trust score calculation

| Column | Type | Purpose |
|--------|------|---------|
| `sales_amount` | DECIMAL | Actual sales |
| `target_amount` | DECIMAL | Sales target |
| `achievement_percent` | DECIMAL | Auto-calculated achievement |
| `quarter` | VARCHAR | Time period |

#### `key_customers` & `regional_sales` Tables
**Purpose**: Detailed sales breakdown and customer information
**Justification**: Supports granular sales analysis and customer relationship tracking

### **6. RELATIONSHIP & TRUST METRICS**

#### `partnership_metrics` Table
**Purpose**: AI-calculated trust scores and relationship status
**Justification**: Centralizes partnership health metrics for AI-enhanced relationship management

| Column | Type | Purpose |
|--------|------|---------|
| `trust_score` | DECIMAL | AI-calculated trust (0-10) |
| `relationship_status` | VARCHAR | Partnership health status |
| `action_completion_rate` | DECIMAL | Follow-up completion rate |
| `average_effectiveness` | DECIMAL | Meeting quality score |

#### `meeting_effectiveness` Table
**Purpose**: Post-meeting ratings and feedback
**Justification**: Provides data for AI trust score calculation and meeting quality improvement

### **7. AI & SYSTEM MANAGEMENT**

#### `ai_processing_logs` Table
**Purpose**: Tracks AI operations, status, and fallback usage
**Justification**: Monitors AI service health, quota usage, and system performance

| Column | Type | Purpose |
|--------|------|---------|
| `operation_type` | VARCHAR | Scheduling, agenda, trust calc |
| `ai_model` | VARCHAR | DeepSeek, GPT, etc. |
| `ai_status` | VARCHAR | Active, quota exceeded, error |
| `fallback_used` | BOOLEAN | Whether fallback was used |
| `processing_time_ms` | INTEGER | Performance monitoring |

#### `notifications` Table
**Purpose**: User notifications and alerts
**Justification**: Replaces frontend-only notifications with persistent, cross-session messaging

#### `system_config` Table
**Purpose**: Application configuration and settings
**Justification**: Centralized configuration management for AI models, timeouts, and business rules

## 🔐 **SECURITY IMPLEMENTATION**

### **Row Level Security (RLS) Policies:**

1. **User Data**: Users can only access their own profile data
2. **Meeting Access**: Users can only see meetings they participate in
3. **Calendar Privacy**: Users can only manage their own calendar
4. **Action Items**: Users can only view/update items assigned to them
5. **Notifications**: Users can only see their own notifications
6. **Organization Data**: Members can access their organization's sales data

### **Authentication Integration:**
- Leverages Supabase auth.users for secure authentication
- JWT tokens for API access
- Role-based access control (vendor/distributor)

## 📈 **PERFORMANCE OPTIMIZATIONS**

### **Strategic Indexes:**
- `idx_meetings_date`: Fast meeting lookups by date
- `idx_calendar_user_date`: Efficient availability queries
- `idx_action_items_assignee`: Quick action item retrieval
- `idx_sales_product_quarter`: Fast sales performance queries
- `idx_notifications_unread`: Efficient unread notification counts

### **Computed Columns:**
- `achievement_percent`: Auto-calculated from sales vs. target
- Triggers for automatic `updated_at` timestamp updates

## 🔄 **DATA MIGRATION STRATEGY**

### **From JSON to Database:**

1. **Past Meetings**: `past_meetings.json` → `meetings`, `meeting_topics`, `meeting_decisions`, `action_items`
2. **Sales Data**: `sales_data.json` → `products`, `sales_performance`, `key_customers`, `regional_sales`
3. **Calendar**: `calendar_availability.json` → `calendar_availability`
4. **Relationship Metrics**: Calculated fields → `partnership_metrics`

### **Migration Benefits:**
- **Queryability**: Complex queries instead of JSON parsing
- **Relationships**: Proper foreign keys and joins
- **Scalability**: Handles growth without performance degradation
- **Consistency**: ACID transactions and data integrity
- **Real-time**: Live updates and subscriptions

## 🚀 **AI ENHANCEMENT CAPABILITIES**

### **Trust Score Calculation:**
The database supports the 6-factor AI trust score calculation:

1. **Meeting Effectiveness** (25%): From `meeting_effectiveness` table
2. **Action Completion** (20%): From `action_items` status tracking
3. **Business Performance** (20%): From `sales_performance` achievement rates
4. **Partnership Longevity** (15%): From `partnership_metrics` duration
5. **Communication Quality** (10%): From `meeting_effectiveness` sentiment
6. **Revenue Achievement** (10%): From `sales_performance` vs targets

### **AI Processing Pipeline:**
1. **Data Collection**: Real-time data from all tables
2. **AI Analysis**: DeepSeek/GPT processing with fallback
3. **Result Storage**: Calculated metrics in `partnership_metrics`
4. **Audit Trail**: All operations logged in `ai_processing_logs`

## 📊 **REPORTING & ANALYTICS**

### **Dashboard Queries:**
- Real-time trust scores and relationship status
- Meeting effectiveness trends
- Action item completion rates
- Sales performance vs targets
- AI service health monitoring

### **Business Intelligence:**
- Partnership health dashboards
- Sales performance analytics
- Meeting productivity metrics
- AI vs fallback usage statistics

## 🔮 **FUTURE SCALABILITY**

### **Ready for Enhancement:**
- **Multi-tenant**: Organization-based data isolation
- **Advanced AI**: More sophisticated ML models
- **Real-time Collaboration**: Live meeting features
- **Mobile Support**: Offline-first capabilities
- **Integration APIs**: Third-party calendar/CRM sync

### **Performance Scaling:**
- **Read Replicas**: For analytics workloads
- **Partitioning**: Time-based partitioning for large datasets
- **Caching**: Redis integration for frequently accessed data
- **CDN**: Global distribution for static assets

This database design provides a robust foundation for the AI Meeting Buddy application while maintaining flexibility for future enhancements and scaling requirements.
