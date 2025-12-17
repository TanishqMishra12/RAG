.PHONY: help setup install start-backend start-frontend start-qdrant stop-qdrant validate clean

help:
	@echo "Event-Driven RAG Document Assistant - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Run initial setup (creates venv, installs deps)"
	@echo "  make install        - Install Python dependencies"
	@echo "  make validate       - Validate setup and configuration"
	@echo ""
	@echo "Running Services:"
	@echo "  make start-qdrant   - Start Qdrant with Docker Compose"
	@echo "  make stop-qdrant    - Stop Qdrant"
	@echo "  make start-backend  - Start FastAPI backend"
	@echo "  make start-frontend - Start Streamlit frontend"
	@echo ""
	@echo "Development:"
	@echo "  make format         - Format code with black"
	@echo "  make lint           - Run linting checks"
	@echo "  make clean          - Clean temporary files"
	@echo ""

setup:
	@echo "Running setup..."
	@./setup.sh

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

validate:
	@echo "Validating setup..."
	@python validate_setup.py

start-qdrant:
	@echo "Starting Qdrant..."
	docker-compose up -d
	@echo "Qdrant started at http://localhost:6333"

stop-qdrant:
	@echo "Stopping Qdrant..."
	docker-compose down

start-backend:
	@echo "Starting FastAPI backend..."
	@./start_backend.sh

start-frontend:
	@echo "Starting Streamlit frontend..."
	@./start_frontend.sh

format:
	@echo "Formatting code..."
	black backend/ frontend/
	isort backend/ frontend/

lint:
	@echo "Running linting checks..."
	flake8 backend/ frontend/ --max-line-length=100 || true
	mypy backend/ --ignore-missing-imports || true

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	@echo "Cleaned!"
