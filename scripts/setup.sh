#!/bin/bash

# AI Flashcard Generator - Setup Script
echo "🚀 Setting up AI Flashcard Generator..."

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v16 or higher."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup Backend
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please add your OpenAI API key to backend/.env"
fi

cd ..

# Setup Frontend
echo "⚛️  Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env file
if [ ! -f .env ]; then
    echo "Creating frontend .env file..."
    cp .env.example .env
fi

cd ..

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to backend/.env:"
echo "   echo 'OPENAI_API_KEY=your_api_key_here' > backend/.env"
echo ""
echo "2. Start the development servers:"
echo "   ./scripts/start-dev.sh"
echo ""
echo "3. Open http://localhost:5173 in your browser"
