# Quick Start Guide

This guide will help you get the Event-Driven RAG Document Assistant up and running in minutes.

## Prerequisites

Before starting, ensure you have:
- ✅ Python 3.13 or higher installed
- ✅ Docker and Docker Compose installed
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Steps

### 1. Install Dependencies

```bash
# Run the automated setup script
./setup.sh
```

This script will:
- Create a virtual environment
- Install all Python dependencies
- Start Qdrant with Docker
- Create configuration files

### 2. Configure Environment

Edit the `.env` file and add your OpenAI API key:

```bash
nano .env  # or use your preferred editor
```

**Required:**
```env
OPENAI_API_KEY=sk-your-key-here
```

**Optional (for production Inngest):**
```env
INNGEST_EVENT_KEY=your_inngest_event_key
INNGEST_SIGNING_KEY=your_inngest_signing_key
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### 4. Access the Application

Open your browser and navigate to:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## First Steps

### Upload a Document

1. Go to the **"Upload Documents"** tab
2. Click **"Choose a PDF file"**
3. Select a PDF document
4. Click **"Upload & Process"**
5. Wait for processing (status will show "processing" or "completed")

### Query Your Documents

1. Go to the **"Query Documents"** tab
2. Type your question in the text area
3. (Optional) Adjust the number of sources
4. Click **"Search"**
5. View the AI-generated answer and source documents

## Example Queries

Try these example questions:
- "What is the main topic of this document?"
- "Summarize the key points"
- "What are the conclusions?"
- "Explain the methodology used"
- "List the key findings"

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify your `.env` file has valid OpenAI API key
- Check if Qdrant is running: `docker ps | grep qdrant`

### Qdrant connection errors
```bash
# Restart Qdrant
docker-compose restart

# Check Qdrant logs
docker logs qdrant
```

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check if firewall is blocking connections
- Verify backend URL in frontend/app.py

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Explore the API documentation at http://localhost:8000/docs
- Check out the [API examples](#api-examples) below

## API Examples

### Upload via cURL
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

### Query via cURL
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the main topic?","top_k":5}'
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Tips

- 📄 **Upload multiple documents** to build a larger knowledge base
- 🔍 **Be specific** in your queries for better results
- 📊 **Check sources** to verify the information
- ⚡ **Process time** depends on document size and complexity
- 🔄 **Async mode** (with Inngest) keeps UI responsive during processing

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in your terminal
3. Open an issue on GitHub

Happy querying! 🚀
