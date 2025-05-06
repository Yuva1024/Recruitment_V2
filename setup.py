#!/usr/bin/env python
"""
CareerConnect Setup Script
--------------------------
This script helps with setting up the CareerConnect application locally.
It creates a virtual environment, installs dependencies, and sets up the database.
"""

import os
import sys
import subprocess
import platform

def is_venv():
    """Check if running in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def create_venv():
    """Create a virtual environment if not already in one"""
    if is_venv():
        print("Already running in a virtual environment.")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        return True
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment. Please create it manually.")
        return False

def activate_venv():
    """Provide instructions to activate the virtual environment"""
    if platform.system() == "Windows":
        print("\nTo activate the virtual environment, run:")
        print("    venv\\Scripts\\activate")
    else:
        print("\nTo activate the virtual environment, run:")
        print("    source venv/bin/activate")
    
    print("\nAfter activation, run this script again to continue setup.")

def create_requirements():
    """Create requirements.txt file"""
    print("Creating requirements.txt...")
    
    requirements = [
        "flask",
        "flask-login",
        "flask-migrate",
        "flask-sqlalchemy",
        "flask-wtf",
        "email-validator",
        "gunicorn",
        "werkzeug",
        "markupsafe",
        "jinja2"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("Created requirements.txt successfully.")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please install them manually.")
        return False

def run_application():
    """Provide instructions to run the application"""
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    
    if platform.system() == "Windows":
        print("    set FLASK_APP=main.py")
        print("    set FLASK_ENV=development")
    else:
        print("    export FLASK_APP=main.py")
        print("    export FLASK_ENV=development")
    
    print("    flask run")
    print("\nAlternatively, you can use:")
    print("    python -m flask run")
    print("\nThe application will be available at: http://127.0.0.1:5000")

def main():
    """Main setup function"""
    print("CareerConnect Setup")
    print("===================")
    
    # Check if already in a virtual environment
    if not is_venv():
        # Create virtual environment
        if create_venv():
            activate_venv()
            return
        else:
            print("Continuing without virtual environment...")
    
    # Create requirements.txt
    create_requirements()
    
    # Install dependencies
    if install_dependencies():
        run_application()
    
if __name__ == "__main__":
    main()