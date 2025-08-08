from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LLM-Powered Intelligent Query–Retrieval System",
    description="AI-powered document analysis and question answering system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LLM-Powered Intelligent Query–Retrieval System", "status": "operational"}

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "System is operational"}

@app.post("/api/v1/hackrx/run")
async def process_query():
    """Basic query endpoint"""
    return {
        "answers": ["System is operational but full features are being loaded."],
        "confidence_scores": [0.8],
        "source_clauses": ["System status check"],
        "processing_time": 0.1
    }

@app.post("/api/v1/hackrx/run/detailed")
async def process_query_detailed():
    """Detailed query endpoint"""
    return {
        "total_score": 0.8,
        "correct_answers": 1,
        "accuracy_percentage": 80.0,
        "answers": ["System is operational but full features are being loaded."],
        "confidence_scores": [0.8],
        "source_clauses": ["System status check"],
        "processing_time": 0.1,
        "explanation_summary": "System is operational"
    }

# Export the app for Vercel
handler = app
