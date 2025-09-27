# 🚀 Supabase Setup Guide for AI Meeting Buddy

## 📋 **PREREQUISITES**

- Supabase account (free tier available)
- Your Supabase project credentials:
  - **Project URL**: `https://pbigwnpzvduzjodjfntm.supabase.co`
  - **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## 🗄️ **STEP 1: CREATE DATABASE SCHEMA**

### **1.1 Access Supabase SQL Editor**
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `pbigwnpzvduzjodjfntm`
3. Navigate to **SQL Editor** in the left sidebar
4. Click **New Query**

### **1.2 Execute Schema Creation**
1. Copy the entire contents of `database/supabase_schema.sql`
2. Paste into the SQL Editor
3. Click **Run** to execute the schema creation
4. Verify all tables are created in the **Table Editor**

### **1.3 Verify Schema Creation**
Expected tables (19 total):
- ✅ `users`
- ✅ `organizations` 
- ✅ `meetings`
- ✅ `meeting_participants`
- ✅ `calendar_availability`
- ✅ `meeting_transcripts`
- ✅ `speaker_segments`
- ✅ `meeting_topics`
- ✅ `meeting_decisions`
- ✅ `action_items`
- ✅ `products`
- ✅ `sales_performance`
- ✅ `key_customers`
- ✅ `regional_sales`
- ✅ `partnership_metrics`
- ✅ `meeting_effectiveness`
- ✅ `ai_processing_logs`
- ✅ `notifications`
- ✅ `system_config`

## 📊 **STEP 2: SEED INITIAL DATA**

### **2.1 Execute Seed Script**
1. Create a new query in SQL Editor
2. Copy the entire contents of `database/seed_data.sql`
3. Paste and execute
4. Verify data insertion in Table Editor

### **2.2 Verify Seed Data**
Check these tables have data:
- **organizations**: 2 records (Zoho Chennai, German Distributor)
- **products**: 3 records (CRM, Workplace, Analytics)
- **sales_performance**: 3 records (Q3 2025 data)
- **action_items**: 8 records (various statuses)
- **partnership_metrics**: 1 record (trust score 8.4)

## 🔐 **STEP 3: CONFIGURE AUTHENTICATION**

### **3.1 Enable Authentication**
1. Go to **Authentication** → **Settings**
2. Enable **Email** provider
3. Set **Site URL** to `http://localhost:3000` (for development)
4. Configure **Redirect URLs**:
   - `http://localhost:3000`
   - `http://localhost:3000/auth/callback`

### **3.2 Create Test Users**
1. Go to **Authentication** → **Users**
2. Click **Add User**
3. Create vendor user:
   - **Email**: `vendor@zoho.com`
   - **Password**: `demo123456`
   - **Confirm**: Yes
4. Create distributor user:
   - **Email**: `distributor@germany.com`
   - **Password**: `demo123456`
   - **Confirm**: Yes

### **3.3 Update Users Table**
After creating auth users, update the `users` table:

```sql
-- Get the auth user IDs first
SELECT id, email FROM auth.users;

-- Insert into users table (replace UUIDs with actual auth.users IDs)
INSERT INTO public.users (id, user_type, name, email, organization, timezone) VALUES
('YOUR_VENDOR_AUTH_ID', 'vendor', 'Zoho Chennai Team', 'vendor@zoho.com', 'Zoho Chennai', 'Asia/Kolkata'),
('YOUR_DISTRIBUTOR_AUTH_ID', 'distributor', 'German Distributor Team', 'distributor@germany.com', 'German Distributor', 'Europe/Berlin');
```

## 🔧 **STEP 4: INSTALL BACKEND DEPENDENCIES**

### **4.1 Install Supabase Python Client**
```bash
cd backend
pip install supabase
```

### **4.2 Update Requirements**
Add to `backend/requirements.txt`:
```
supabase>=2.0.0
```

## ⚙️ **STEP 5: UPDATE BACKEND CONFIGURATION**

### **5.1 Update config.py**
Add Supabase configuration to `backend/config.py`:

```python
# Supabase Configuration
SUPABASE_URL = "https://pbigwnpzvduzjodjfntm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBiaWd3bnB6dmR1empvZGpmbnRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MDU0NzUsImV4cCI6MjA3NDQ4MTQ3NX0.1xi5vjO-2eACQ78jeRDNyBN2Z8NgCYcYD-vlO7_lVQ8"

# Database Mode
USE_SUPABASE = True  # Set to False to use JSON files
```

### **5.2 Update strands_agent.py**
Modify the data loading methods to use Supabase:

```python
from supabase_client import supabase_client

class MeetingBuddyAgent:
    def __init__(self):
        # ... existing code ...
        
        # Use Supabase instead of JSON files
        if getattr(config, 'USE_SUPABASE', False):
            self.use_database = True
        else:
            self.use_database = False
            # Keep existing JSON loading as fallback
    
    async def _load_past_meetings(self):
        if self.use_database:
            return await supabase_client.get_past_meetings()
        else:
            return self._load_json_data("data/past_meetings.json")
    
    async def _load_sales_data(self):
        if self.use_database:
            return await supabase_client.get_sales_performance()
        else:
            return self._load_json_data("data/sales_data.json")
```

## 🌐 **STEP 6: UPDATE FRONTEND AUTHENTICATION**

### **6.1 Install Supabase JS Client**
```bash
cd frontend
npm install @supabase/supabase-js
```

### **6.2 Create Supabase Client**
Create `frontend/src/lib/supabase.js`:

```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://pbigwnpzvduzjodjfntm.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBiaWd3bnB6dmR1empvZGpmbnRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MDU0NzUsImV4cCI6MjA3NDQ4MTQ3NX0.1xi5vjO-2eACQ78jeRDNyBN2Z8NgCYcYD-vlO7_lVQ8'

export const supabase = createClient(supabaseUrl, supabaseKey)
```

### **6.3 Update AuthContext**
Replace mock authentication with Supabase auth:

```javascript
import { supabase } from '../lib/supabase'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null)
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const login = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
    return data
  }

  const logout = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }

  // ... rest of the context
}
```

## 🧪 **STEP 7: TESTING THE INTEGRATION**

### **7.1 Test Database Connection**
Create a test script `backend/test_supabase.py`:

```python
import asyncio
from supabase_client import supabase_client

async def test_connection():
    # Test basic connection
    meetings = await supabase_client.get_past_meetings()
    print(f"Found {len(meetings)} past meetings")
    
    # Test sales data
    sales = await supabase_client.get_sales_performance()
    print(f"Sales data: {sales}")
    
    # Test action items
    actions = await supabase_client.get_action_items()
    print(f"Action items: {len(actions['pending_actions'])} pending")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run the test:
```bash
cd backend
python test_supabase.py
```

### **7.2 Test Frontend Authentication**
1. Start the frontend: `npm start`
2. Go to login page
3. Try logging in with test credentials:
   - **Vendor**: `vendor@zoho.com` / `demo123456`
   - **Distributor**: `distributor@germany.com` / `demo123456`

### **7.3 Test API Endpoints**
Test the backend APIs:
```bash
# Test schedule endpoint
curl http://localhost:8000/api/meeting/schedule

# Test context endpoint  
curl http://localhost:8000/api/meeting/context

# Test agenda endpoint
curl http://localhost:8000/api/meeting/agenda

# Test follow-ups endpoint
curl http://localhost:8000/api/meeting/followups
```

## 🚀 **STEP 8: DEPLOYMENT CONSIDERATIONS**

### **8.1 Environment Variables**
For production, use environment variables:

```bash
# Backend .env
SUPABASE_URL=https://pbigwnpzvduzjodjfntm.supabase.co
SUPABASE_KEY=your_supabase_anon_key
USE_SUPABASE=true

# Frontend .env
REACT_APP_SUPABASE_URL=https://pbigwnpzvduzjodjfntm.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### **8.2 Security Checklist**
- ✅ RLS policies enabled on all tables
- ✅ API keys properly configured
- ✅ CORS settings for production domains
- ✅ User authentication working
- ✅ Data access permissions verified

### **8.3 Performance Monitoring**
Monitor these metrics in Supabase dashboard:
- Database connections
- Query performance
- API usage
- Authentication events
- Storage usage

## 🔧 **TROUBLESHOOTING**

### **Common Issues:**

1. **"relation does not exist" error**
   - Ensure schema was created successfully
   - Check table names match exactly

2. **Authentication not working**
   - Verify Site URL in Supabase settings
   - Check API keys are correct
   - Ensure users exist in auth.users table

3. **RLS blocking queries**
   - Verify user is authenticated
   - Check RLS policies match your use case
   - Test with RLS disabled temporarily

4. **Data not appearing**
   - Verify seed data was inserted
   - Check foreign key relationships
   - Ensure proper user permissions

### **Debug Commands:**
```sql
-- Check if tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check RLS status
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables WHERE schemaname = 'public';

-- Check user data
SELECT * FROM auth.users;
SELECT * FROM public.users;
```

## ✅ **SUCCESS CRITERIA**

Your Supabase integration is successful when:

1. ✅ All 19 tables created with proper relationships
2. ✅ Seed data inserted successfully
3. ✅ Authentication working with test users
4. ✅ Backend can query database successfully
5. ✅ Frontend can authenticate users
6. ✅ All API endpoints return data from database
7. ✅ RLS policies protecting user data
8. ✅ AI features working with database backend

## 🎯 **NEXT STEPS**

After successful setup:

1. **Migrate Existing Data**: Import any additional real data
2. **Customize RLS**: Adjust security policies for your needs
3. **Add Indexes**: Optimize for your query patterns
4. **Set up Monitoring**: Configure alerts and dashboards
5. **Plan Backups**: Set up automated database backups
6. **Scale Planning**: Monitor usage and plan for growth

Your AI Meeting Buddy is now powered by a robust, scalable Supabase database! 🚀
