#!/usr/bin/env python3
"""
Simple API Test to debug document processing
"""

import requests
import json

def test_simple_api():
    """Test with a simple request to debug issues"""
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Simple test request
    test_request = {
        "documents": [
            "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
        ],
        "questions": [
            "What is the grace period for premium payment?"
        ]
    }
    
    print("🔍 Testing Simple API Request")
    print("=" * 40)
    
    try:
        print("📤 Sending request...")
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_request,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_simple_api()
