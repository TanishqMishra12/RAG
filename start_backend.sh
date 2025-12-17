#!/bin/bash

# Start the FastAPI backend server
echo "Starting FastAPI backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one from .env.example"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
