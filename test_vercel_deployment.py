#!/usr/bin/env python3
"""
Test Vercel deployment
"""

import requests
import json
import os
from api_config import API_BASE_URL, API_HEADERS, HEALTH_ENDPOINT, BASIC_QUERY_ENDPOINT, DETAILED_QUERY_ENDPOINT

def test_vercel_deployment():
    """Test Vercel deployment"""
    
    print("🚀 Testing Vercel Deployment")
    print("=" * 50)
    print(f"📡 Base URL: {API_BASE_URL}")
    
    # Test 1: Health Check
    print(f"\n1️⃣ Testing health endpoint...")
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=30)
        print(f"✅ Health Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ System Status: {health_data.get('status', 'unknown')}")
            print(f"✅ Components: {len(health_data.get('components', {}))} initialized")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Basic Query
    print(f"\n2️⃣ Testing basic query endpoint...")
    test_request = {
        "documents": [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        ],
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?"
        ]
    }
    
    try:
        response = requests.post(
            BASIC_QUERY_ENDPOINT,
            headers=API_HEADERS,
            json=test_request,
            timeout=60
        )
        
        print(f"✅ Query Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answers Generated: {len(result.get('answers', []))}")
            print(f"✅ Processing Time: {result.get('processing_time', 0):.2f}s")
            
            # Show sample answer
            if result.get('answers'):
                print(f"📝 Sample Answer: {result['answers'][0][:100]}...")
        else:
            print(f"❌ Query failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Query error: {e}")
    
    # Test 3: Detailed Query
    print(f"\n3️⃣ Testing detailed query endpoint...")
    try:
        response = requests.post(
            DETAILED_QUERY_ENDPOINT,
            headers=API_HEADERS,
            json=test_request,
            timeout=60
        )
        
        print(f"✅ Detailed Query Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Total Score: {result.get('total_score', 0):.2f}")
            print(f"✅ Accuracy: {result.get('accuracy_percentage', 0):.1f}%")
            print(f"✅ Processing Time: {result.get('processing_time', 0):.2f}s")
        else:
            print(f"❌ Detailed query failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Detailed query error: {e}")
    
    # Test 4: Authentication
    print(f"\n4️⃣ Testing authentication...")
    try:
        # Test without token
        response = requests.post(
            BASIC_QUERY_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=test_request,
            timeout=30
        )
        
        if response.status_code == 401:
            print("✅ Authentication working correctly")
        else:
            print(f"⚠️  Authentication may not be working: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
    
    print(f"\n🎯 Deployment Test Summary")
    print("=" * 50)
    print(f"✅ Your API is deployed at: {API_BASE_URL}")
    print(f"✅ Health endpoint: {HEALTH_ENDPOINT}")
    print(f"✅ Basic query: {BASIC_QUERY_ENDPOINT}")
    print(f"✅ Detailed query: {DETAILED_QUERY_ENDPOINT}")
    print(f"\n📝 Usage Example:")
    print(f"curl -X POST '{BASIC_QUERY_ENDPOINT}' \\")
    print(f"  -H 'Authorization: Bearer {API_HEADERS['Authorization'].split(' ')[1]}' \\")
    print(f"  -H 'Content-Type: application/json' \\")
    print(f"  -d '{{\"documents\": [\"https://example.com/policy.pdf\"], \"questions\": [\"What is the grace period?\"]}}'")

if __name__ == "__main__":
    test_vercel_deployment()
