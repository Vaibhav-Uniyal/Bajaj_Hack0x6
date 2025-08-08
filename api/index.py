from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Simple health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "LLM-Powered Intelligent Query–Retrieval System", "status": "operational"}

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "System is operational"}

# Import the full API only if needed
try:
    from src.api_serverless import app as full_app
    
    # Add routes from the full API
    for route in full_app.routes:
        app.routes.append(route)
    
    logger.info("Successfully loaded full API")
except Exception as e:
    logger.error(f"Failed to load full API: {e}")
    
    @app.post("/api/v1/hackrx/run")
    async def process_query_fallback():
        """Fallback endpoint"""
        return {"error": "System temporarily unavailable", "message": str(e)}

# Export the app for Vercel
handler = app
