#!/usr/bin/env python3
"""
Test with a working document URL
"""

import requests
import json

def test_working_document():
    """Test with a working document URL"""
    
    print("🔧 Testing with Working Document")
    print("=" * 40)
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test with a publicly accessible PDF
    test_request = {
        "documents": [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        ],
        "questions": [
            "What is the grace period for premium payment?"
        ]
    }
    
    print("📄 Testing with publicly accessible PDF...")
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
    
    print(f"\n💡 Issue Identified:")
    print(f"The original document URL returns 409 (Conflict) status.")
    print(f"This suggests the Azure blob URL may be expired or have access restrictions.")
    print(f"\n🔧 Solutions:")
    print(f"1. Update the document URL with a valid, accessible PDF")
    print(f"2. Upload your policy document to a public URL")
    print(f"3. Use a different document URL for testing")

if __name__ == "__main__":
    test_working_document()
