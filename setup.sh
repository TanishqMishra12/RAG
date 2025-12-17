#!/bin/bash

# Setup script for Event-Driven RAG Document Assistant

echo "=== Event-Driven RAG Document Assistant Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find virtual environment activation script"
    exit 1
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p uploads data qdrant_storage

# Start Qdrant with Docker
echo ""
echo "Starting Qdrant with Docker Compose..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
    echo "✅ Qdrant started successfully"
else
    echo "⚠️  Docker Compose not found. Please install Docker and start Qdrant manually:"
    echo "   docker-compose up -d"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Start the backend: ./start_backend.sh"
echo "3. Start the frontend: ./start_frontend.sh"
echo "4. Open http://localhost:8501 in your browser"
echo ""
