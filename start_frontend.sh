#!/bin/bash

# Start the Streamlit frontend
echo "Starting Streamlit frontend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one from .env.example"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start Streamlit
streamlit run frontend/app.py --server.port 8501
