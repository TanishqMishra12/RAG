"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI
    openai_api_key: str
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"
    
    # Inngest
    inngest_event_key: str = ""
    inngest_signing_key: str = ""
    
    # FastAPI
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    
    # Application
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4-turbo-preview"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
