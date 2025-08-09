#!/usr/bin/env python3
"""
Setup script for ColDToNs development environment.
This script helps new developers get started quickly.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            cwd=cwd,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_frontend():
    """Set up the frontend development environment."""
    print("\n🎨 Setting up Frontend...")
    
    if not os.path.exists("frontend/node_modules"):
        print("Installing frontend dependencies...")
        if not run_command("npm install", cwd="frontend"):
            return False
        print("✅ Frontend dependencies installed")
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def setup_backend():
    """Set up the backend development environment."""
    print("\n🐍 Setting up Backend...")
    
    print("Installing backend dependencies...")
    if not run_command("pip install -r requirements.txt", cwd="backend"):
        return False
    print("✅ Backend dependencies installed")
    
    return True

def build_frontend():
    """Build the frontend for production."""
    print("\n🏗️  Building Frontend...")
    
    if not run_command("npm run build", cwd="frontend"):
        return False
    print("✅ Frontend built successfully")
    
    return True

def main():
    """Main setup function."""
    print("🚀 ColDToNs Development Setup")
    print("=" * 40)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Error: backend/main.py not found. Are you in the ColDToNs root directory?")
        return 1
    
    # Setup steps
    steps = [
        ("Frontend Setup", setup_frontend),
        ("Backend Setup", setup_backend),
        ("Frontend Build", build_frontend),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"❌ {step_name} failed!")
            return 1
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\n📋 What's next?")
    print("1. Start development backend: python backend/main.py")
    print("2. Start development frontend: cd frontend && npm run dev")
    print("3. Or run both with: npm run dev (after npm install in root)")
    print("4. Visit http://localhost:3000 for development")
    print("5. Visit http://localhost:5000 for production build")
    print("\n📚 See DEPLOYMENT.md for deployment instructions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())