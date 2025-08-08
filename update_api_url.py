#!/usr/bin/env python3
"""
Update API URL Script
"""

import re

def update_api_url(new_url):
    """Update the API URL in api_config.py"""
    
    # Read the current config file
    with open('api_config.py', 'r') as f:
        content = f.read()
    
    # Update the API_BASE_URL
    updated_content = re.sub(
        r'API_BASE_URL = ".*?"',
        f'API_BASE_URL = "{new_url}"',
        content
    )
    
    # Write the updated content
    with open('api_config.py', 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated API URL to: {new_url}")
    print("📝 You can now run: python test_vercel_deployment.py")

def main():
    """Main function"""
    print("🔧 API URL Updater")
    print("=" * 30)
    
    # Get the new URL from user
    new_url = input("Enter your Vercel deployment URL (e.g., https://your-project.vercel.app): ").strip()
    
    if not new_url:
        print("❌ URL cannot be empty")
        return
    
    if not new_url.startswith(('http://', 'https://')):
        new_url = f"https://{new_url}"
    
    # Update the URL
    update_api_url(new_url)

if __name__ == "__main__":
    main()
