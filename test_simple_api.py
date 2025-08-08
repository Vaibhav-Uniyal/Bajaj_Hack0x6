#!/usr/bin/env python3
"""
Simple API Test
"""

import requests

def test_simple_api():
    """Test the simplified API"""
    
    base_url = "https://bajaj-hack0x6.vercel.app"
    
    print("🧪 Testing Simple API")
    print("=" * 30)
    
    # Test root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test health endpoint
    print("\n2️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_api()
