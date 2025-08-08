#!/usr/bin/env python3
"""
Test script to verify authentication is working
"""

import requests
import json

def test_authentication():
    """Test authentication on protected endpoints"""
    
    base_url = "http://localhost:8000/api/v1"
    token = "db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Health endpoint (should work without auth)
    print("🧪 Testing health endpoint (no auth required)...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test 2: Main endpoint with auth (should work)
    print("\n🧪 Testing main endpoint with authentication...")
    test_request = {
        "documents": [
            "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24"
        ],
        "questions": [
            "What is the grace period for premium payment?"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers=headers,
            json=test_request
        )
        print(f"✅ Main endpoint with auth: {response.status_code}")
        if response.status_code == 200:
            print("✅ Authentication working correctly!")
        else:
            print(f"❌ Authentication failed: {response.text}")
    except Exception as e:
        print(f"❌ Main endpoint failed: {e}")
    
    # Test 3: Main endpoint without auth (should fail)
    print("\n🧪 Testing main endpoint without authentication...")
    try:
        response = requests.post(
            f"{base_url}/hackrx/run",
            headers={"Content-Type": "application/json"},
            json=test_request
        )
        print(f"❌ Should have failed but got: {response.status_code}")
    except Exception as e:
        print(f"✅ Correctly failed without auth: {e}")

if __name__ == "__main__":
    print("🔐 Testing Authentication")
    print("=" * 50)
    test_authentication()
