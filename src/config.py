import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the LLM-Powered Query Retrieval System"""
    
    # API Configuration
    API_BASE_URL = "http://localhost:8000/api/v1"
    API_TITLE = "LLM-Powered Intelligent Query–Retrieval System"
    API_VERSION = "1.0.0"
    
    # Authentication
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6")
    
    # LLM Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-2.0-flash"
    GEMINI_MAX_TOKENS = 2000
    GEMINI_TEMPERATURE = 0.1
    
    # Embedding Configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
    
    # Vector Database Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    PINECONE_INDEX_NAME = "hackrx-documents"
    
    # Document Processing
    MAX_CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Scoring Configuration
    KNOWN_DOCUMENT_WEIGHT = 0.5
    UNKNOWN_DOCUMENT_WEIGHT = 2.0
    DEFAULT_QUESTION_WEIGHT = 1.0
    
    # Performance Configuration
    BATCH_SIZE = 10
    CACHE_TTL = 3600  # 1 hour
    MAX_CONCURRENT_REQUESTS = 5
    
    # Logging
    LOG_LEVEL = "INFO"
    
    @classmethod
    def get_scoring_weights(cls) -> Dict[str, float]:
        """Get scoring weights for different question types"""
        return {
            "grace_period": 1.0,
            "waiting_period": 1.5,
            "coverage": 2.0,
            "maternity": 2.0,
            "surgery": 1.5,
            "organ_donor": 2.0,
            "ncd": 1.0,
            "health_checkup": 1.0,
            "hospital_definition": 1.0,
            "ayush": 1.5,
            "room_rent": 1.5,
            "default": cls.DEFAULT_QUESTION_WEIGHT
        }
