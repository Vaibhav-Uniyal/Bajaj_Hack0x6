#!/usr/bin/env python3
"""
Test script to verify Gemini integration
"""

import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

async def test_gemini():
    """Test Gemini API connection"""
    try:
        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment variables")
            print("Please add your Gemini API key to the .env file")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Test simple generation
        print("🧪 Testing Gemini API...")
        response = await model.generate_content_async(
            "Hello! Please respond with 'Gemini is working!' if you can see this message."
        )
        
        print(f"✅ Gemini Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        return False

async def test_system_components():
    """Test system components with Gemini"""
    try:
        from src.orchestrator import QueryRetrievalOrchestrator
        
        print("🧪 Testing system components...")
        orchestrator = QueryRetrievalOrchestrator()
        
        # Test system status
        status = orchestrator.get_system_status()
        print(f"✅ System Status: {status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Gemini Integration")
    print("=" * 50)
    
    # Test 1: Direct Gemini API
    print("\n1. Testing direct Gemini API...")
    gemini_ok = asyncio.run(test_gemini())
    
    # Test 2: System components
    print("\n2. Testing system components...")
    system_ok = asyncio.run(test_system_components())
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Gemini API: {'✅ PASS' if gemini_ok else '❌ FAIL'}")
    print(f"System Components: {'✅ PASS' if system_ok else '❌ FAIL'}")
    
    if gemini_ok and system_ok:
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("\nNext steps:")
        print("1. Add your Gemini API key to .env file")
        print("2. Test with real documents using the API")
        print("3. Access the interactive docs at http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
