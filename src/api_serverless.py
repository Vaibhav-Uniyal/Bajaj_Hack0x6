from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from typing import Dict, Any

from .models import QueryRequest, QueryResponse
from .orchestrator import QueryRetrievalOrchestrator
from .config import Config

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

# Global orchestrator instance (for serverless optimization)
_orchestrator = None

def get_orchestrator() -> QueryRetrievalOrchestrator:
    """Get or create orchestrator instance (optimized for serverless)"""
    global _orchestrator
    if _orchestrator is None:
        logger.info("Initializing orchestrator...")
        _orchestrator = QueryRetrievalOrchestrator()
        logger.info("Orchestrator initialized successfully")
    return _orchestrator

def verify_token(request: Request):
    """Verify Bearer token authentication"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    token = auth_header.split(" ")[1]
    if token != Config.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LLM-Powered Intelligent Query–Retrieval System", "status": "operational"}

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    try:
        orchestrator = get_orchestrator()
        status = orchestrator.get_system_status()
        return status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@app.post("/api/v1/hackrx/run")
async def process_query(request: QueryRequest, token: str = Depends(verify_token)):
    """Process query request"""
    try:
        logger.info(f"Processing query with {len(request.questions)} questions")
        orchestrator = get_orchestrator()
        response = await orchestrator.process_query(request)
        return response
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        # Return structured error response
        error_response = QueryResponse(
            answers=["Unable to process request due to system error."] * len(request.questions),
            confidence_scores=[0.0] * len(request.questions),
            source_clauses=["Error occurred during processing"] * len(request.questions),
            processing_time=0.0
        )
        return error_response

@app.post("/api/v1/hackrx/run/detailed")
async def process_query_detailed(request: QueryRequest, token: str = Depends(verify_token)):
    """Process query with detailed response including scoring"""
    try:
        logger.info(f"Processing detailed query with {len(request.questions)} questions")
        orchestrator = get_orchestrator()
        response = await orchestrator.process_query_with_details(request)
        return response
    except Exception as e:
        logger.error(f"Detailed query processing failed: {e}")
        # Return structured error response
        return {
            "total_score": 0.0,
            "correct_answers": 0,
            "accuracy_percentage": 0.0,
            "score_breakdown": [],
            "answers": ["Unable to process request due to system error."] * len(request.questions),
            "confidence_scores": [0.0] * len(request.questions),
            "source_clauses": ["Error occurred during processing"] * len(request.questions),
            "processing_time": 0.0,
            "explanation_summary": "System error occurred during processing"
        }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
