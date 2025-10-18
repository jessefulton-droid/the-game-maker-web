#!/bin/bash

# The Game Maker - Startup Script
# This script sets up and runs the Flask application

echo "🎮 Starting The Game Maker..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r backend/requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from template..."
    cp env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter to continue (or Ctrl+C to exit and edit .env first)..."
fi

# Run the Flask app
echo "🚀 Starting Flask app..."
echo "📱 Open http://localhost:5000 in your browser"
echo ""
python backend/app.py

