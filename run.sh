#!/bin/bash

# 🚀 AI Meeting Buddy - Complete Setup & Run Script
# This script sets up and runs both frontend and backend

echo "🤖 AI Meeting Buddy - Starting Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status "Created .env from .env.example"
        print_warning "Please edit .env file with your API keys before running the application!"
        echo ""
        echo "Required API keys:"
        echo "- OPENAI_API_KEY (your Gemini API key)"
        echo "- SUPABASE_URL (your Supabase URL)"
        echo "- SUPABASE_KEY (your Supabase key)"
        echo ""
        read -p "Press Enter after updating .env file..."
    else
        print_error ".env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Function to setup backend
setup_backend() {
    print_info "Setting up Backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
        print_status "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    print_status "Backend dependencies installed"
    
    cd ..
}

# Function to setup frontend
setup_frontend() {
    print_info "Setting up Frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_info "Installing Node.js dependencies..."
        npm install
        print_status "Frontend dependencies installed"
    else
        print_status "Frontend dependencies already installed"
    fi
    
    cd ..
}

# Function to run backend
run_backend() {
    print_info "Starting Backend Server..."
    cd backend
    source venv/bin/activate
    print_status "Backend starting on http://localhost:8000"
    print_info "API Documentation: http://localhost:8000/docs"
    print_info "Health Check: http://localhost:8000/health"
    echo ""
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to run frontend
run_frontend() {
    print_info "Starting Frontend Server..."
    cd frontend
    print_status "Frontend starting on http://localhost:3000"
    echo ""
    npm start
}

# Function to run both in background
run_both() {
    print_info "Starting both Backend and Frontend..."
    
    # Start backend in background
    cd backend
    source venv/bin/activate
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend in background
    cd frontend
    npm start > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Backend started (PID: $BACKEND_PID) on http://localhost:8000"
    print_status "Frontend started (PID: $FRONTEND_PID) on http://localhost:3000"
    echo ""
    print_info "Logs:"
    print_info "  Backend: tail -f backend.log"
    print_info "  Frontend: tail -f frontend.log"
    echo ""
    print_info "To stop both servers:"
    print_info "  kill $BACKEND_PID $FRONTEND_PID"
    echo ""
    
    # Keep script running
    wait
}

# Function to show status
show_status() {
    print_info "Checking application status..."
    echo ""
    
    # Check backend
    if curl -s http://localhost:8000/health > /dev/null; then
        print_status "Backend is running on http://localhost:8000"
    else
        print_warning "Backend is not running"
    fi
    
    # Check frontend
    if curl -s http://localhost:3000 > /dev/null; then
        print_status "Frontend is running on http://localhost:3000"
    else
        print_warning "Frontend is not running"
    fi
}

# Function to stop all services
stop_all() {
    print_info "Stopping all services..."
    
    # Kill backend processes
    pkill -f "uvicorn main:app"
    
    # Kill frontend processes
    pkill -f "npm start"
    pkill -f "react-scripts start"
    
    print_status "All services stopped"
}

# Main menu
show_menu() {
    echo ""
    echo "🤖 AI Meeting Buddy - Control Panel"
    echo "=================================="
    echo "1. Setup Backend"
    echo "2. Setup Frontend"
    echo "3. Setup Both (Backend + Frontend)"
    echo "4. Run Backend Only"
    echo "5. Run Frontend Only"
    echo "6. Run Both (Backend + Frontend)"
    echo "7. Show Status"
    echo "8. Stop All Services"
    echo "9. Exit"
    echo ""
}

# Main script logic
if [ $# -eq 0 ]; then
    # Interactive mode
    while true; do
        show_menu
        read -p "Choose an option (1-9): " choice
        
        case $choice in
            1)
                setup_backend
                ;;
            2)
                setup_frontend
                ;;
            3)
                setup_backend
                setup_frontend
                ;;
            4)
                run_backend
                ;;
            5)
                run_frontend
                ;;
            6)
                run_both
                ;;
            7)
                show_status
                ;;
            8)
                stop_all
                ;;
            9)
                print_info "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-9."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
else
    # Command line mode
    case $1 in
        "setup-backend")
            setup_backend
            ;;
        "setup-frontend")
            setup_frontend
            ;;
        "setup")
            setup_backend
            setup_frontend
            ;;
        "backend")
            run_backend
            ;;
        "frontend")
            run_frontend
            ;;
        "both")
            run_both
            ;;
        "status")
            show_status
            ;;
        "stop")
            stop_all
            ;;
        *)
            echo "Usage: $0 [setup-backend|setup-frontend|setup|backend|frontend|both|status|stop]"
            echo ""
            echo "Examples:"
            echo "  $0 setup          # Setup both backend and frontend"
            echo "  $0 backend        # Run backend only"
            echo "  $0 frontend       # Run frontend only"
            echo "  $0 both           # Run both backend and frontend"
            echo "  $0 status         # Check status of services"
            echo "  $0 stop           # Stop all services"
            ;;
    esac
fi
