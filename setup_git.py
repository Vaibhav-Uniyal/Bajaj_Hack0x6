#!/usr/bin/env python3
"""
Git Setup Helper Script
"""

import os
import subprocess
import sys

def check_git_installed():
    """Check if Git is installed"""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is installed")
            return True
        else:
            print("❌ Git not found")
            return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def check_github_cli():
    """Check if GitHub CLI is installed"""
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI is installed")
            return True
        else:
            print("⚠️  GitHub CLI not found (optional)")
            return False
    except FileNotFoundError:
        print("⚠️  GitHub CLI not found (optional)")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "README.md",
        "DEPLOYMENT.md",
        "QUICK_START.md",
        "GIT_DEPLOYMENT.md",
        ".gitignore",
        "requirements.txt",
        "requirements-vercel.txt",
        "vercel.json",
        "main.py",
        "src/api_serverless.py",
        "api/index.py",
        "env_example.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_env_file():
    """Check if .env file exists and warn about it"""
    if os.path.exists(".env"):
        print("⚠️  .env file found - Make sure it's in .gitignore")
        return True
    else:
        print("✅ .env file not found (good - should not be committed)")
        return True

def initialize_git():
    """Initialize Git repository"""
    print("\n🚀 Initializing Git repository...")
    
    try:
        # Check if already a Git repository
        if os.path.exists(".git"):
            print("⚠️  Git repository already exists")
            return True
        
        # Initialize Git
        result = subprocess.run(["git", "init"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            return True
        else:
            print(f"❌ Failed to initialize Git: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing Git: {e}")
        return False

def add_files_to_git():
    """Add files to Git"""
    print("\n📁 Adding files to Git...")
    
    try:
        # Add all files (excluding those in .gitignore)
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Files added to Git")
            return True
        else:
            print(f"❌ Failed to add files: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding files: {e}")
        return False

def make_initial_commit():
    """Make initial commit"""
    print("\n💾 Making initial commit...")
    
    try:
        result = subprocess.run([
            "git", "commit", "-m", 
            "Initial commit: LLM-Powered Intelligent Query–Retrieval System"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Initial commit created")
            return True
        else:
            print(f"❌ Failed to create commit: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating commit: {e}")
        return False

def show_next_steps():
    """Show next steps for GitHub deployment"""
    print("\n🎯 Next Steps for GitHub Deployment:")
    print("=" * 50)
    print("1. Create GitHub repository:")
    print("   - Go to https://github.com")
    print("   - Click 'New repository'")
    print("   - Name it 'hackr6-llm-system'")
    print("   - Make it public")
    print("   - Don't initialize with README")
    print()
    print("2. Add remote origin:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/hackr6-llm-system.git")
    print()
    print("3. Push to GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("4. Verify repository:")
    print("   - Check all files are uploaded")
    print("   - Ensure .env is NOT in repository")
    print("   - Test the README displays correctly")
    print()
    print("5. Deploy to Vercel:")
    print("   - Follow DEPLOYMENT.md guide")
    print("   - Set environment variables in Vercel dashboard")

def main():
    """Main setup function"""
    print("🚀 Git Setup Helper for LLM-Powered Intelligent Query–Retrieval System")
    print("=" * 70)
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    git_ok = check_git_installed()
    github_cli_ok = check_github_cli()
    
    if not git_ok:
        print("\n❌ Git is required. Please install Git first.")
        print("   Windows: https://git-scm.com/download/win")
        print("   macOS: brew install git")
        print("   Linux: sudo apt install git")
        return
    
    # Check files
    print("\n📁 Checking required files...")
    files_ok = check_required_files()
    env_ok = check_env_file()
    
    if not files_ok:
        print("\n❌ Some required files are missing. Please ensure all files are present.")
        return
    
    # Initialize Git
    print("\n🔧 Setting up Git repository...")
    git_init_ok = initialize_git()
    
    if not git_init_ok:
        print("\n❌ Failed to initialize Git repository.")
        return
    
    # Add files
    add_ok = add_files_to_git()
    
    if not add_ok:
        print("\n❌ Failed to add files to Git.")
        return
    
    # Make commit
    commit_ok = make_initial_commit()
    
    if not commit_ok:
        print("\n❌ Failed to create initial commit.")
        return
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Git setup completed successfully!")
    print("📝 Follow the next steps above to deploy to GitHub and Vercel.")

if __name__ == "__main__":
    main()
