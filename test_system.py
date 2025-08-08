#!/usr/bin/env python3
"""
Simple test script to verify the LLM-Powered Query Retrieval System components
"""

import asyncio
import logging
from src.orchestrator import QueryRetrievalOrchestrator
from src.models import QueryRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_system():
    """Test the system with a sample request"""
    
    # Sample request matching the API specification
    request = QueryRequest(
        documents=[
            "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
        ],
        questions=[
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases (PED)?",
            "Does the policy cover maternity expenses and what are the conditions?"
        ]
    )
    
    try:
        logger.info("Initializing system components...")
        orchestrator = QueryRetrievalOrchestrator()
        
        logger.info("Testing system status...")
        status = orchestrator.get_system_status()
        logger.info(f"System status: {status['status']}")
        
        logger.info("Processing test request...")
        response = await orchestrator.process_query(request)
        
        logger.info("Test completed successfully!")
        logger.info(f"Generated {len(response.answers)} answers")
        logger.info(f"Processing time: {response.processing_time:.2f}s")
        
        # Print results
        print("\n" + "="*50)
        print("TEST RESULTS")
        print("="*50)
        
        for i, (question, answer) in enumerate(zip(request.questions, response.answers)):
            print(f"\nQuestion {i+1}: {question}")
            print(f"Answer: {answer}")
            if response.confidence_scores:
                print(f"Confidence: {response.confidence_scores[i]:.2f}")
            if response.source_clauses:
                print(f"Source: {response.source_clauses[i]}")
        
        print(f"\nTotal processing time: {response.processing_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    print("LLM-Powered Intelligent Query–Retrieval System Test")
    print("="*60)
    
    try:
        asyncio.run(test_system())
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Set up your OpenAI API key in .env file")
        print("3. Internet connection for downloading documents")
