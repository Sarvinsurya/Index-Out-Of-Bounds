# 🚀 AI Meeting Buddy - Backend

FastAPI-powered intelligent meeting assistant with advanced transcript analysis.

## 🏃 Quick Start

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API key in config.py

# Start development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 API Testing

```bash
# Health check
curl http://localhost:8000/health

# Complete meeting data
curl -X POST http://localhost:8000/api/meeting/generate \
  -H "Content-Type: application/json" \
  -d '{"participants": ["Zoho Chennai", "German Distributor"]}'

# Transcript analysis (BREAKTHROUGH FEATURE!)
curl http://localhost:8000/api/transcript/sample | \
curl -X POST http://localhost:8000/api/transcript/quick-analyze \
  -H "Content-Type: application/json" -d @-
```

## 🏗️ Architecture

- **main.py**: FastAPI server with all endpoints
- **strands_agent.py**: Core meeting intelligence with tool calls
- **transcript_analyzer.py**: AI-powered conversation analysis
- **models.py**: Pydantic data models and validation
- **config.py**: Configuration and environment management
- **data/**: Mock data for development and demos

## 🎯 Key Features

✅ **Cross-timezone scheduling** (Chennai ↔ Germany)  
✅ **AI transcript analysis** with schedule change detection  
✅ **Tool-call architecture** for modular frontend integration  
✅ **Robust fallback systems** for production reliability  
✅ **Enterprise-ready** async processing  

## 🔧 Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

Ready for hackathon demo! 🏆
