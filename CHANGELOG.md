# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-17

### Added
- Initial release of Event-Driven RAG Document Assistant
- FastAPI backend with RESTful API endpoints
- Streamlit frontend for document upload and querying
- Inngest integration for event-driven document processing
- Qdrant vector database integration for semantic search
- OpenAI GPT-4 and embeddings integration
- PDF document processing and chunking
- Asynchronous document processing workflow
- Docker Compose configuration for Qdrant
- Comprehensive documentation (README, QUICKSTART, CONTRIBUTING)
- Setup and validation scripts
- Health check endpoints
- Source citation in answers

### Features
- 📄 PDF document upload and processing
- 🔍 Semantic search with Qdrant vector database
- 🤖 AI-powered answer generation with GPT-4
- ⚡ Event-driven asynchronous processing
- 🎨 Clean and intuitive Streamlit UI
- 📊 Document source display with relevance scores
- 🔧 Configurable chunk size and overlap
- 🐳 Docker-based Qdrant deployment
- 🔄 Automatic fallback to synchronous processing
- ✅ Health check and system status monitoring

### Documentation
- Comprehensive README with architecture diagrams
- Quick start guide
- API documentation
- Setup instructions
- Troubleshooting guide
- Contributing guidelines
- Example queries and API usage

### Technical Stack
- Python 3.13
- FastAPI for backend API
- Streamlit for frontend UI
- Inngest for event orchestration
- Qdrant as vector database
- OpenAI GPT-4 and text-embedding-3-small
- LangChain for document processing
- Docker for Qdrant deployment

[1.0.0]: https://github.com/TanishqMishra12/RAG/releases/tag/v1.0.0
