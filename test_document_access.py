#!/usr/bin/env python3
"""
Test document accessibility and processing
"""

import requests
import json

def test_document_access():
    """Test if the document URL is accessible"""
    
    print("🔍 Testing Document Accessibility")
    print("=" * 40)
    
    # Test 1: Check if document URL is accessible
    document_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
    
    print(f"📄 Testing document URL: {document_url}")
    try:
        response = requests.head(document_url, timeout=10)
        print(f"✅ Document URL Status: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"✅ Content-Length: {response.headers.get('content-length', 'unknown')}")
    except Exception as e:
        print(f"❌ Document URL not accessible: {e}")
    
    # Test 2: Test with a mock document (text instead of PDF)
    print(f"\n🧪 Testing with mock document...")
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test with a simple text document URL (this will fail but helps us understand the error)
    test_request = {
        "documents": [
            "https://httpbin.org/json"  # This will return JSON, not a PDF
        ],
        "questions": [
            "What is the grace period for premium payment?"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_request,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_document_access()
