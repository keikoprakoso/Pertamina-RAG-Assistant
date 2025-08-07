"""
Setup script for the Company Knowledge Base Assistant
"""
import os
import subprocess
import sys

def check_python_version():
    """Check if Python 3.8+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8 or higher is required")
        return False
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists")

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
    
    # Upgrade pip first
    subprocess.run([pip_path, "install", "--upgrade", "pip"])
    
    # Install requirements
    result = subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    if result.returncode == 0:
        print("Requirements installed successfully!")
        return True
    else:
        print("ERROR: Failed to install requirements")
        return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    if not os.path.exists(".env"):
        print("Creating .env file...")
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("Please update .env with your actual OpenAI API key")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        if "your_openai_api_key_here" in content:
            print("Please update .env with your actual OpenAI API key")
            return False
    
    return True

def initialize_vector_store():
    """Initialize the FAISS vector store"""
    print("Initializing vector store...")
    try:
        from rag import RAGSystem
        rag_system = RAGSystem()
        rag_system.build_vector_store("pertamina_sop.txt")
        print("Vector store initialized successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Failed to initialize vector store: {e}")
        return False

def main():
    print("Company Knowledge Base Assistant - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check OpenAI key
    if not check_openai_key():
        print("Setup completed with warnings. Please update .env file.")
    else:
        print("OpenAI API key found")
    
    # Initialize vector store
    if not initialize_vector_store():
        print("Setup completed with warnings. You may need to initialize the vector store manually.")
    else:
        print("Setup completed successfully!")
    
    print("\nTo run the application:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("2. Run the application:")
    print("   python app.py")
    print("\nOr use the run script:")
    if os.name == 'nt':  # Windows
        print("   run.bat")
    else:  # Unix/Linux/macOS
        print("   ./run.sh")

if __name__ == "__main__":
    main()