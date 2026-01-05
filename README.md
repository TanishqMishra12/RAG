Event-Driven RAG Document Assistant


A robust, local Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interactively ask questions about their content. Built with a focus on reliability and scalability, the project leverages Inngest for event-driven workflow orchestration, Qdrant (via Docker) for vector storage, and OpenAI for intelligent response generation.

2. Key Features
📄 PDF Ingestion: Seamlessly upload and process PDF documents through a user-friendly frontend.

🧠 Intelligent Q&A: Ask natural language questions and receive accurate answers based strictly on the document's context.

⚡ Event-Driven Architecture: Uses Inngest to orchestrate background flows (chunking, embedding, and upserting), ensuring the main application remains responsive even during heavy processing.

🔍 Vector Search: Utilizes Qdrant (running locally in Docker) for high-performance vector similarity search.

🛡️ Flow Control: Implements throttling and rate limiting (via Inngest) to manage API usage and prevent system overload.

🖥️ Interactive UI: A clean, minimal frontend built with Streamlit for easy interaction.

3. Tech Stack
Language: Python 3.13

Frontend: Streamlit

Orchestration & Queuing: Inngest (Serverless queues & workflows)

Vector Database: Qdrant (Containerized via Docker)

LLM Integration: OpenAI API

Backend Framework: FastAPI (handling the webhooks/events)

DevOps: Docker

4. How It Works (Technical Deep Dive)
The project follows a modern "Asynchronous RAG" pipeline:

Upload & Trigger: When a user uploads a file via the Streamlit UI, the file is saved locally, and an event (rag/ingest_pdf) is sent to Inngest.

Ingestion Workflow: Inngest picks up the event and executes a multi-step workflow:

Load & Chunk: The PDF is parsed and split into manageable text chunks.

Embed & Upsert: Text chunks are converted into vector embeddings using OpenAI's embedding model and stored in the Qdrant vector database.

Retrieval & Answer:

When the user asks a question, the system embeds the query and performs a similarity search in Qdrant to find the most relevant chunks.

These chunks are passed as context to the OpenAI model to generate a precise answer.

5. Code Highlights (For your Portfolio/Interview)
Reliability: Implemented Inngest "Step Functions" to ensure that if the embedding step fails, it retries automatically without restarting the whole process.

Optimization: Configured throttling (period=1m, count=2) to manage API rate limits efficiently.

Infrastructure: Deployed Qdrant inside a Docker container to isolate the database environment and ensure consistent performance across machines.
