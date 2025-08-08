#!/usr/bin/env python3
"""
Test with local policy.pdf file
"""

import requests
import json
import subprocess
import time
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

def find_free_port():
    """Find a free port to use for the local server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def start_local_server(port):
    """Start a simple HTTP server to serve the policy.pdf file"""
    os.chdir('.')  # Serve from current directory
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def test_local_policy():
    """Test with local policy.pdf file"""
    
    print("🔧 Testing with Local Policy Document")
    print("=" * 50)
    
    # Check if policy.pdf exists
    if not os.path.exists('policy.pdf'):
        print("❌ policy.pdf not found in current directory")
        print("💡 Please make sure policy.pdf is in the same directory as this script")
        return
    
    print(f"✅ Found policy.pdf ({os.path.getsize('policy.pdf')} bytes)")
    
    # Start local server
    port = find_free_port()
    server = start_local_server(port)
    local_url = f"http://localhost:{port}/policy.pdf"
    
    print(f"🚀 Started local server on port {port}")
    print(f"📄 Document URL: {local_url}")
    
    # Wait a moment for server to start
    time.sleep(1)
    
    # Test URL accessibility
    print(f"\n🔍 Testing local document accessibility...")
    try:
        response = requests.head(local_url, timeout=10)
        print(f"✅ Local URL Status: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"✅ Content-Length: {response.headers.get('content-length', 'unknown')}")
    except Exception as e:
        print(f"❌ Local URL not accessible: {e}")
        server.shutdown()
        return
    
    # Test the API
    print(f"\n🚀 Testing API with local policy document...")
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    test_request = {
        "documents": [
            local_url
        ],
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_request,
            timeout=60  # Longer timeout for document processing
        )
        
        print(f"📥 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Response: {json.dumps(result, indent=2)}")
            
            if result.get('answers'):
                print(f"\n📝 Sample Answers:")
                for i, (question, answer) in enumerate(zip(test_request['questions'], result['answers'])):
                    print(f"   Q{i+1}: {question}")
                    print(f"   A{i+1}: {answer[:150]}...")
                    print()
                    
            print(f"\n🎉 SUCCESS! Your API is working with local documents!")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    finally:
        # Shutdown local server
        server.shutdown()
        print(f"\n🛑 Local server stopped")

if __name__ == "__main__":
    test_local_policy()
