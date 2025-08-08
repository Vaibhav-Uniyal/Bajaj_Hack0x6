#!/usr/bin/env python3
"""
Test with local document processing
"""

import requests
import json
import tempfile
import os

def test_local_document():
    """Test with a local document to bypass URL issues"""
    
    print("🔧 Testing with Local Document")
    print("=" * 40)
    
    # Create a simple test document
    test_content = """
    National Parivar Mediclaim Plus Policy
    
    Section 3.2 Grace Period
    A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.
    
    Section 4.1 Waiting Period
    There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.
    
    Section 5.3 Maternity Coverage
    Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months.
    """
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file_path = f.name
    
    print(f"📄 Created test document: {temp_file_path}")
    print(f"📄 Document content length: {len(test_content)} characters")
    
    # Note: The current system expects URLs, not local files
    # This is just to show what the document content should look like
    print(f"\n📝 Test Document Content:")
    print(f"{test_content[:200]}...")
    
    # Clean up
    os.unlink(temp_file_path)
    
    print(f"\n💡 Recommendations:")
    print(f"1. Upload your policy document to a public URL (Google Drive, Dropbox, etc.)")
    print(f"2. Use a different Azure blob URL with proper access permissions")
    print(f"3. Test with a simple insurance policy document")
    print(f"4. Check server logs for specific error messages")

if __name__ == "__main__":
    test_local_document()
