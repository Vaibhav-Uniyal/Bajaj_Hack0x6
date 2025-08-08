#!/usr/bin/env python3
"""
Test orchestrator directly to see actual errors
"""

import asyncio
import logging
from src.orchestrator import QueryRetrievalOrchestrator
from src.models import QueryRequest

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG)

async def test_orchestrator_direct():
    """Test orchestrator directly"""
    
    print("🔍 Testing Orchestrator Directly")
    print("=" * 40)
    
    # Create orchestrator
    orchestrator = QueryRetrievalOrchestrator()
    
    # Create test request
    request = QueryRequest(
        documents=["http://localhost:57460/policy.pdf"],
        questions=[
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    )
    
    print("🚀 Testing orchestrator directly...")
    try:
        result = await orchestrator.process_query(request)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_orchestrator_direct())
