#!/bin/bash

# AI Flashcard Generator - Development Server Starter
echo "🚀 Starting AI Flashcard Generator development servers..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start Backend
echo "🐍 Starting FastAPI backend server..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo "⚛️  Starting React frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Both servers are starting up..."
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait
