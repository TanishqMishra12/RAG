# Event-Driven RAG Document Assistant

A robust, local Retrieval-Augmented Generation (RAG) application designed to interactively query PDF documents. This project utilizes an event-driven architecture to handle document processing asynchronously, ensuring the application remains responsive even during heavy workload.

## Features

- 🚀 **Event-Driven Architecture**: Asynchronous document processing with Inngest
- 📄 **PDF Support**: Upload and process PDF documents
- 🔍 **Semantic Search**: Vector similarity search with Qdrant
- 🤖 **AI-Powered Answers**: Generate contextual answers using OpenAI GPT-4
- ⚡ **Responsive**: Non-blocking UI during document processing
- 🎨 **Modern UI**: Clean Streamlit interface for easy interaction

## Tech Stack

- **Python 3.13**
- **Backend Framework**: FastAPI
- **Frontend**: Streamlit
- **Orchestration**: Inngest (event-driven processing)
- **Vector Database**: Qdrant (running via Docker)
- **AI/LLM**: OpenAI API (GPT-4 and embeddings)

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Streamlit  │────────▶│    FastAPI   │────────▶│   Inngest   │
│  Frontend   │         │   Backend    │         │  (Events)   │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                        │
                               │                        ▼
                               │                  ┌─────────────┐
                               │                  │  Document   │
                               │                  │  Processor  │
                               │                  └─────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────┐         ┌─────────────┐
                        │   Qdrant    │◀────────│   OpenAI    │
                        │   Vector    │         │  Embeddings │
                        │     DB      │         └─────────────┘
                        └─────────────┘
```

## Prerequisites

- Python 3.13+
- Docker and Docker Compose
- OpenAI API key
- (Optional) Inngest account for production event processing

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TanishqMishra12/RAG.git
   cd RAG
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   QDRANT_COLLECTION_NAME=documents
   # Optional: Inngest keys for production
   INNGEST_EVENT_KEY=your_inngest_event_key_here
   INNGEST_SIGNING_KEY=your_inngest_signing_key_here
   ```

5. **Start Qdrant with Docker**
   ```bash
   docker-compose up -d
   ```
   
   Verify Qdrant is running:
   ```bash
   curl http://localhost:6333/collections
   ```

## Usage

### Starting the Application

1. **Start the Backend (FastAPI)**
   ```bash
   ./start_backend.sh
   ```
   
   Or manually:
   ```bash
   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   Backend API will be available at: `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

2. **Start the Frontend (Streamlit)**
   
   In a new terminal:
   ```bash
   ./start_frontend.sh
   ```
   
   Or manually:
   ```bash
   streamlit run frontend/app.py
   ```
   
   Frontend will be available at: `http://localhost:8501`

### Using the Application

1. **Upload Documents**
   - Navigate to the "Upload Documents" tab
   - Select a PDF file
   - Click "Upload & Process"
   - The document will be processed asynchronously

2. **Query Documents**
   - Navigate to the "Query Documents" tab
   - Enter your question
   - Select the number of sources to retrieve
   - Click "Search"
   - View the AI-generated answer and source documents

## API Endpoints

### Health Check
```bash
GET /api/health
```

### Upload Document
```bash
POST /api/upload
Content-Type: multipart/form-data
```

### Query Documents
```bash
POST /api/query
Content-Type: application/json

{
  "query": "What is the main topic?",
  "top_k": 5
}
```

## Event-Driven Processing

The application uses Inngest for event-driven document processing:

1. **Document Upload**: User uploads a PDF via the frontend
2. **Event Trigger**: FastAPI emits a `document/uploaded` event
3. **Async Processing**: Inngest processes the event asynchronously
   - Extract text from PDF
   - Split into chunks
   - Generate embeddings
   - Store in Qdrant vector database
4. **Completion**: Document is ready for querying

**Note**: If Inngest is not configured, the application falls back to synchronous processing.

## Project Structure

```
RAG/
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes.py          # API endpoints
│       ├── models/
│       │   └── schemas.py         # Pydantic models
│       ├── services/
│       │   ├── document_processor.py  # PDF processing
│       │   ├── vector_store.py        # Qdrant integration
│       │   ├── rag_service.py         # RAG logic
│       │   └── inngest_service.py     # Event handling
│       ├── config.py              # Configuration
│       └── main.py                # FastAPI app
├── frontend/
│   └── app.py                     # Streamlit UI
├── .env.example                   # Environment template
├── docker-compose.yml             # Qdrant setup
├── requirements.txt               # Python dependencies
├── start_backend.sh               # Backend startup script
└── start_frontend.sh              # Frontend startup script
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `QDRANT_HOST` | Qdrant host | localhost |
| `QDRANT_PORT` | Qdrant port | 6333 |
| `QDRANT_COLLECTION_NAME` | Collection name | documents |
| `INNGEST_EVENT_KEY` | Inngest event key | Optional |
| `INNGEST_SIGNING_KEY` | Inngest signing key | Optional |
| `BACKEND_HOST` | Backend host | 0.0.0.0 |
| `BACKEND_PORT` | Backend port | 8000 |

### Customization

Edit `backend/app/config.py` to customize:
- Chunk size and overlap
- Embedding model
- Chat model
- Other parameters

## Development

### Running Tests
```bash
# Add tests as needed
pytest
```

### Code Style
```bash
# Format code
black .

# Lint
flake8 .
```

## Troubleshooting

### Qdrant Connection Issues
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker-compose restart
```

### Backend Issues
```bash
# Check logs
python -m uvicorn backend.app.main:app --log-level debug
```

### Frontend Issues
```bash
# Check Streamlit logs in terminal
# Ensure backend is running on port 8000
```

## Future Enhancements

- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Multi-user support with authentication
- [ ] Document management (list, delete, update)
- [ ] Advanced search filters
- [ ] Conversation history
- [ ] Batch document processing
- [ ] Custom embedding models
- [ ] Response streaming

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- OpenAI for GPT-4 and embeddings
- Qdrant for vector database
- Inngest for event orchestration
- FastAPI and Streamlit communities