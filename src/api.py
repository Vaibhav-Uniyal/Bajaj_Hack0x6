from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio

from .models import QueryRequest, QueryResponse
from .orchestrator import QueryRetrievalOrchestrator
from .config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    version=Config.API_VERSION,
    description="LLM-Powered Intelligent Query–Retrieval System for insurance, legal, HR, and compliance domains"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize security
security = HTTPBearer()

# Initialize orchestrator
orchestrator = QueryRetrievalOrchestrator()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authentication token"""
    if credentials.credentials != Config.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM-Powered Intelligent Query–Retrieval System",
        "version": Config.API_VERSION,
        "status": "operational"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": orchestrator.get_system_status()["components"]
    }

@app.get("/api/v1/status")
async def system_status():
    """Get system status and configuration"""
    return orchestrator.get_system_status()

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_submissions(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """
    Run Submissions - Process documents and answer questions
    
    This endpoint processes insurance policy documents and answers natural language questions
    about coverage, waiting periods, grace periods, and other policy details.
    """
    try:
        logger.info(f"Processing request with {len(request.documents)} documents and {len(request.questions)} questions")
        
        # Process the query through all 6 components
        response = await orchestrator.process_query(request)
        
        logger.info(f"Successfully processed request. Processing time: {response.processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process request: {str(e)}"
        )

@app.post("/api/v1/hackrx/run/detailed")
async def run_submissions_detailed(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """
    Run Submissions with Detailed Response - Process documents and answer questions with scoring details
    
    This endpoint provides detailed response including scoring breakdown, confidence scores,
    and explanation of decisions.
    """
    try:
        logger.info(f"Processing detailed request with {len(request.documents)} documents and {len(request.questions)} questions")
        
        # Process the query with detailed response
        response = await orchestrator.process_query_with_details(request)
        
        logger.info(f"Successfully processed detailed request. Processing time: {response.get('processing_time', 0):.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing detailed request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process detailed request: {str(e)}"
        )

@app.get("/api/v1/docs")
async def get_documentation():
    """Get API documentation"""
    return {
        "title": Config.API_TITLE,
        "version": Config.API_VERSION,
        "endpoints": {
            "POST /api/v1/hackrx/run": "Process documents and answer questions",
            "POST /api/v1/hackrx/run/detailed": "Process with detailed scoring response",
            "GET /api/v1/health": "Health check",
            "GET /api/v1/status": "System status",
            "GET /api/v1/docs": "This documentation"
        },
        "authentication": "Bearer token required",
        "example_request": {
            "documents": [
                "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
            ],
            "questions": [
                "What is the grace period for premium payment?",
                "What is the waiting period for pre-existing diseases (PED)?",
                "Does the policy cover maternity expenses and what are the conditions?"
            ]
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "status_code": 500,
        "timestamp": asyncio.get_event_loop().time()
    }
