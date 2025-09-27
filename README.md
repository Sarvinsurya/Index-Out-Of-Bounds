# 🤖 AI Meeting Buddy

> **Transforming chaotic meetings into productive, AI-powered collaboration sessions**

*Built for the Zoho Hackathon 2025 - Solving real-world meeting pain points with intelligent automation*

## ✨ Latest Updates

- ✅ **Gemini 2.0 Flash Integration**: Powered by Google's latest AI model
- ✅ **Environment Variables**: Secure configuration management
- ✅ **Performance Optimized**: Reduced timeouts and improved response times
- ✅ **Hidden Fallback Notifications**: Clean user experience
- ✅ **Production Ready**: Complete frontend and backend integration

## 🎯 Problem Statement

Global vendor-distributor partnerships (like Zoho Chennai ↔ German partners) suffer from:
- ❌ Endless email chains for scheduling across time zones
- ❌ Unprepared participants who forget previous discussions
- ❌ Lost decisions and missed follow-ups
- ❌ Wasted time in unproductive meetings

## 💡 Our Solution

**AI Meeting Buddy** - An intelligent meeting assistant that makes every meeting productive from start to finish.

### 🚀 Core Features

#### 📅 **Smart Cross-Timezone Scheduling**
- Automatically finds optimal meeting slots across Chennai (IST) ↔ Germany (CET)
- Intelligent conflict resolution with confidence scoring
- Buffer time management and duration optimization

#### 🎙️ **Revolutionary Transcript Analysis** ⭐ *BREAKTHROUGH FEATURE*
- **Real-time conversation processing** with speaker identification
- **Automatic schedule change detection**: "reschedule to evening 5 PM" → Calendar updates
- **Smart action item extraction** with automatic assignment
- **Decision tracking** and commitment analysis
- **Sentiment analysis** for relationship health monitoring

#### 🧠 **AI-Powered Meeting Intelligence**
- Context generation from past meetings and sales data
- Intelligent agenda creation based on conversation history
- Trust score calculation and relationship analytics
- Follow-up tracking with completion rate monitoring

#### 🏗️ **Enterprise-Ready Architecture**
- Tool-call based modular design for scalability
- Individual card generators for flexible frontend integration
- Robust fallback systems for reliable operation

## 🏆 Project Structure

```
AI-meeting-Buddy/
├── 📄 .env.example      # Environment variables template
├── 📄 .gitignore        # Git ignore rules
├── 📁 backend/          # FastAPI + AI Processing Engine
│   ├── main.py          # API server with all endpoints
│   ├── strands_agent.py # Core meeting intelligence with Gemini API
│   ├── transcript_analyzer.py # AI transcript processing
│   ├── models.py        # Pydantic data models
│   ├── config.py        # Environment configuration
│   ├── requirements.txt # Python dependencies
│   ├── supabase_client.py # Database integration
│   ├── data/           # Mock data for demo
│   └── venv/           # Virtual environment
├── 📁 frontend/         # React Dashboard (COMPLETE!)
│   ├── src/            # React source code
│   ├── public/         # Static assets
│   ├── build/          # Production build
│   └── package.json    # Node dependencies
├── 📁 database/        # Database schema and setup
│   ├── 01_create_schema.sql
│   ├── 02_insert_data.sql
│   └── SETUP_GUIDE.md
└── 📁 demo/            # Demo scripts and tools
    ├── demo_tool_calls.py
    ├── demo_transcript_analysis.py
    └── start.py
```

## 🛠️ Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Sarvinsurya/Index-Out-Of-Bounds.git
cd Index-Out-Of-Bounds

# Copy environment template and configure
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
# Frontend will be available at http://localhost:3000
```

### API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get complete meeting preparation
curl -X POST http://localhost:8000/api/meeting/generate \
  -H "Content-Type: application/json" \
  -d '{"participants": ["Zoho Chennai", "German Distributor"]}'

# Analyze meeting transcript (BREAKTHROUGH FEATURE!)
curl -X POST http://localhost:8000/api/transcript/quick-analyze \
  -H "Content-Type: application/json" \
  -d @sample_transcript.json
```

## 🎮 Demo Features

### 🎯 Tool Call Architecture Demo
```bash
cd demo
python demo_tool_calls.py
```
Shows individual card generation for modular frontend integration.

### 🎙️ Transcript Analysis Demo
```bash
cd demo  
python demo_transcript_analysis.py
```
Demonstrates AI-powered conversation analysis and automatic action extraction.

## 🌟 API Reference

### Meeting Dashboard APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/meeting/generate` | POST | Complete 4-card meeting preparation |
| `/api/meeting/schedule` | GET | Smart scheduling suggestions |
| `/api/meeting/context` | GET | Key insights and history |
| `/api/meeting/agenda` | GET | AI-generated agenda |
| `/api/meeting/followups` | GET | Action item tracking |

### 🎙️ Transcript Processing APIs (BREAKTHROUGH!)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/transcript/analyze` | POST | Full transcript analysis |
| `/api/transcript/quick-analyze` | POST | Simplified analysis |
| `/api/transcript/sample` | GET | Sample transcript for testing |

## 💻 Technical Excellence

### Backend Technologies
- **FastAPI**: High-performance async API framework
- **Pydantic**: Type-safe data validation and serialization
- **Gemini 2.0 Flash**: Google's latest AI model for natural language processing
- **Supabase**: Real-time database and authentication
- **Pytz**: Robust timezone handling for global teams
- **Uvicorn**: Production-ready ASGI server
- **aiohttp**: Async HTTP client for API calls

### Architecture Highlights
- **Tool-Call Pattern**: Modular, reusable components
- **Async Processing**: Non-blocking transcript analysis with aiohttp
- **Environment Configuration**: Secure API key management
- **Fallback Systems**: Intelligent business logic when AI is unavailable
- **Cross-Timezone Logic**: Chennai IST ↔ Germany CET optimization
- **Real-time Frontend**: React dashboard with live data updates
- **Enterprise Scalability**: Microservice-ready design

## 🎯 Hackathon Demo Script

### 1. **Smart Scheduling** (30 seconds)
Show automatic time zone coordination and conflict resolution
```bash
curl http://localhost:8001/api/meeting/schedule | jq
```

### 2. **Transcript Magic** ⭐ (60 seconds)
Upload conversation → Extract scheduling changes and action items
```bash
curl -X POST http://localhost:8001/api/transcript/quick-analyze \
  -d '{transcript with "reschedule to 5 PM"}' | jq
```

### 3. **Meeting Intelligence** (30 seconds)
Show context-aware agenda generation and relationship analytics
```bash
curl -X POST http://localhost:8001/api/meeting/generate | jq
```

### 4. **Architecture Excellence** (30 seconds)
Demonstrate tool-call modularity and scalability benefits

## 🏅 Hackathon Judging Criteria

✅ **Innovation**: Transcript-to-action automation (industry-first!)  
✅ **Technical Depth**: Advanced AI integration with robust architecture  
✅ **Business Value**: Solves actual pain points in global partnerships  
✅ **Scalability**: Enterprise-ready tool-call architecture  
✅ **Demo Quality**: Multiple impressive endpoints with real-world scenarios  

## 🔮 Future Enhancements

- 🔊 **Live Audio Processing**: Real-time meeting transcription
- 📊 **Advanced Analytics**: Meeting effectiveness tracking
- 🔗 **Calendar Integration**: Google/Outlook sync
- 🌐 **Multi-language Support**: Global team communication
- 🤖 **Voice Commands**: "AI, schedule follow-up for next week"
- 📱 **Mobile App**: Native iOS/Android applications
- 🔔 **Push Notifications**: Real-time meeting alerts

## 👥 Team


---


*Start with `cd backend && uvicorn main:app --port 8000` and experience the future of meeting intelligence!*