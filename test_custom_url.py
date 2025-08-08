#!/usr/bin/env python3
"""
Test with custom document URL
"""

import requests
import json

def test_custom_url():
    """Test with a custom document URL"""
    
    print("🔧 Testing with Custom Document URL")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # UPDATE THIS URL WITH YOUR NEW DOCUMENT URL
    custom_document_url = "YOUR_NEW_DOCUMENT_URL_HERE"
    
    # Test request with custom URL
    test_request = {
        "documents": [
            custom_document_url
        ],
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?"
        ]
    }
    
    print(f"📄 Testing with URL: {custom_document_url}")
    
    # First, test if the URL is accessible
    print(f"\n🔍 Checking URL accessibility...")
    try:
        response = requests.head(custom_document_url, timeout=10)
        print(f"✅ URL Status: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"✅ Content-Length: {response.headers.get('content-length', 'unknown')}")
    except Exception as e:
        print(f"❌ URL not accessible: {e}")
        return
    
    # Test the API
    print(f"\n🚀 Testing API with custom URL...")
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_request,
            timeout=30
        )
        
        print(f"📥 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Response: {json.dumps(result, indent=2)}")
            
            if result.get('answers'):
                print(f"\n📝 Sample Answers:")
                for i, (question, answer) in enumerate(zip(test_request['questions'], result['answers'])):
                    print(f"   Q{i+1}: {question}")
                    print(f"   A{i+1}: {answer[:100]}...")
                    print()
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    print("⚠️  IMPORTANT: Update the 'custom_document_url' variable with your new URL!")
    print("=" * 70)
    test_custom_url()
