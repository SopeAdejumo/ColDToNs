#!/usr/bin/env python3
"""
Test script to verify the ColDToNs build and deployment setup.
Run this script to check if everything is configured correctly.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minutes timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    print("\n🔍 Checking Dependencies...")
    
    # Check Python
    success, stdout, stderr = run_command("python --version")
    if success:
        print(f"✅ Python: {stdout.strip()}")
    else:
        print(f"❌ Python: Not found or not working")
        return False
    
    # Check Node.js
    success, stdout, stderr = run_command("node --version")
    if success:
        print(f"✅ Node.js: {stdout.strip()}")
    else:
        print(f"❌ Node.js: Not found or not working")
        return False
    
    # Check npm
    success, stdout, stderr = run_command("npm --version")
    if success:
        print(f"✅ npm: {stdout.strip()}")
    else:
        print(f"❌ npm: Not found or not working")
        return False
    
    return True

def check_project_structure():
    """Check if the project structure is correct."""
    print("\n📁 Checking Project Structure...")
    
    required_files = [
        ("package.json", "Root package.json"),
        ("build.sh", "Build script (Unix)"),
        ("start.sh", "Start script (Unix)"),
        ("build.bat", "Build script (Windows)"),
        ("start.bat", "Start script (Windows)"),
        ("Procfile", "Procfile for deployment"),
        ("DEPLOYMENT.md", "Deployment documentation"),
        ("backend/main.py", "Flask backend"),
        ("backend/requirements.txt", "Python requirements"),
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/vite.config.js", "Vite configuration"),
        ("frontend/src/App.jsx", "React App component"),
    ]
    
    all_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def test_frontend_build():
    """Test if the frontend can be built."""
    print("\n🏗️  Testing Frontend Build...")
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    success, stdout, stderr = run_command("npm install", cwd="frontend")
    if not success:
        print(f"❌ Failed to install frontend dependencies: {stderr}")
        return False
    print("✅ Frontend dependencies installed")
    
    # Build frontend
    print("Building frontend...")
    success, stdout, stderr = run_command("npm run build", cwd="frontend")
    if not success:
        print(f"❌ Failed to build frontend: {stderr}")
        return False
    print("✅ Frontend built successfully")
    
    # Check if dist folder was created
    if os.path.exists("frontend/dist"):
        print("✅ Frontend dist folder created")
        
        # Check for key files
        key_files = ["frontend/dist/index.html", "frontend/dist/assets"]
        for file_path in key_files:
            if os.path.exists(file_path):
                print(f"✅ Found: {file_path}")
            else:
                print(f"⚠️  Missing: {file_path}")
        
        return True
    else:
        print("❌ Frontend dist folder not created")
        return False

def test_backend_setup():
    """Test if the backend can be set up."""
    print("\n🐍 Testing Backend Setup...")
    
    # Install backend dependencies
    print("Installing backend dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements.txt", cwd="backend")
    if not success:
        print(f"❌ Failed to install backend dependencies: {stderr}")
        return False
    print("✅ Backend dependencies installed")
    
    # Test import of main modules
    print("Testing backend imports...")
    test_import_code = """
import sys
sys.path.append('backend')
try:
    from main import app
    print("✅ Flask app imports successfully")
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")
    sys.exit(1)
"""
    
    success, stdout, stderr = run_command(f"python -c \"{test_import_code}\"")
    if success:
        print(stdout.strip())
        return True
    else:
        print(f"❌ Backend import test failed: {stderr}")
        return False

def main():
    """Main test function."""
    print("🧪 ColDToNs Build Test")
    print("=" * 50)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Run all tests
    tests = [
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Frontend Build", test_frontend_build),
        ("Backend Setup", test_backend_setup),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your ColDToNs setup is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Commit your changes to git")
        print("2. Push to your GitHub repository")
        print("3. Follow the deployment instructions in DEPLOYMENT.md")
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        print("\n🔧 Common fixes:")
        print("- Install missing dependencies (Node.js, Python, npm)")
        print("- Check file paths and project structure")
        print("- Review error messages above for specific issues")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())