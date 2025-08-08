#!/usr/bin/env python3
"""
Deploy to Vercel helper script
"""

import os
import subprocess
import sys

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if vercel CLI is installed
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Vercel CLI is installed")
        else:
            print("❌ Vercel CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI not found. Install with: npm i -g vercel")
        return False
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found. Make sure to set environment variables in Vercel dashboard")
    
    # Check if all required files exist
    required_files = [
        "vercel.json",
        "api/index.py",
        "requirements-vercel.txt",
        "src/api_serverless.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    return True

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("🚀 Deploying to Vercel...")
    
    try:
        # Check if user is logged in
        result = subprocess.run(["vercel", "whoami"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not logged in to Vercel. Please run: vercel login")
            return False
        
        print("✅ Logged in to Vercel")
        
        # Deploy
        print("📤 Deploying...")
        result = subprocess.run(["vercel", "--prod"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(result.stdout)
            return True
        else:
            print("❌ Deployment failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Vercel Deployment Helper")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        return
    
    print("\n✅ All prerequisites met!")
    
    # Ask user if they want to deploy
    response = input("\n🤔 Do you want to deploy to Vercel? (y/n): ")
    if response.lower() != 'y':
        print("👋 Deployment cancelled.")
        return
    
    # Deploy
    if deploy_to_vercel():
        print("\n🎉 Deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. Set environment variables in Vercel dashboard")
        print("2. Test your deployment with: python test_vercel_deployment.py")
        print("3. Share your API URL with others!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")

if __name__ == "__main__":
    main()
