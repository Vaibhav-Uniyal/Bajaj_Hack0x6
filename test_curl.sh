#!/bin/bash
# Manual API Testing with curl commands

echo "🧪 Testing API with curl commands"
echo "=================================="

# Test 1: Health check (no auth required)
echo -e "\n1️⃣ Testing health endpoint..."
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "Content-Type: application/json"

# Test 2: Basic endpoint with authentication
echo -e "\n\n2️⃣ Testing basic endpoint with auth..."
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Authorization: Bearer db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "documents": [
      "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    ],
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
      "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
  }'

# Test 3: Detailed endpoint with authentication
echo -e "\n\n3️⃣ Testing detailed endpoint with auth..."
curl -X POST "http://localhost:8000/api/v1/hackrx/run/detailed" \
  -H "Authorization: Bearer db3d35016048bf11a289b37ed27dcda6b8b647e12051704e4e011501361414a6" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "documents": [
      "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    ],
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
    ]
  }'

echo -e "\n\n✅ API testing completed!"
