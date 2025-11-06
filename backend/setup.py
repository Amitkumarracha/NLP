#!/usr/bin/env python3
"""
Setup script for Beyond Words Backend
Initializes database, checks dependencies, and validates configuration
"""
import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_virtual_env():
    """Check if running in virtual environment"""
    print_header("Checking Virtual Environment")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("   Recommendation: Create and activate venv")
        print("   python -m venv venv")
        print("   Windows: venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        return False

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    print_header("Checking Environment Configuration")
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        if os.path.exists('.env.example'):
            print("   Creating .env from .env.example...")
            with open('.env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✅ .env file created")
            print("   ⚠️  Please update .env with your configuration")
            return True
        else:
            print("   ❌ .env.example not found")
            return False

def check_model_files():
    """Check if model files exist"""
    print_header("Checking Model Files")
    models_dir = Path("finetuned_models")
    
    if not models_dir.exists():
        print("⚠️  finetuned_models directory not found")
        models_dir.mkdir(exist_ok=True)
        print("✅ Created finetuned_models directory")
    
    required_files = [
        "xgboost_finetuned.json",
        "ensemble_meta.pkl"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = models_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  {len(missing_files)} model file(s) missing")
        print("   Models need to be trained or downloaded")
        return False
    
    return True

def test_imports():
    """Test if key packages can be imported"""
    print_header("Testing Package Imports")
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("librosa", "Librosa"),
        ("xgboost", "XGBoost"),
        ("sklearn", "Scikit-learn"),
        ("numpy", "NumPy"),
        ("pydub", "PyDub"),
    ]
    
    all_ok = True
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def test_database_connection():
    """Test database connection"""
    print_header("Testing Database Connection")
    try:
        from database.connection import test_connection, DB_TYPE
        print(f"   Database type: {DB_TYPE}")
        
        if test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            print("   Check your DATABASE_URL or MONGODB_URL in .env")
            return False
    except Exception as e:
        print(f"⚠️  Could not test database: {e}")
        print("   Database configuration may need to be set up")
        return False

def initialize_database():
    """Initialize database tables/collections"""
    print_header("Initializing Database")
    try:
        from database.connection import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    directories = [
        "logs",
        "data",
        "data/spectrograms",
        "finetuned_models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def print_summary(results):
    """Print setup summary"""
    print_header("Setup Summary")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nCompleted: {passed}/{total} checks passed\n")
    
    for check, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {check}")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to run the application.")
        print("\n   Start the server:")
        print("   python app.py")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main setup function"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          Beyond Words - Backend Setup Script             ║
║     Emotion Detection & Mental Health Support System     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Run all checks
    results["Python Version"] = check_python_version()
    results["Virtual Environment"] = check_virtual_env()
    results["Environment File"] = check_env_file()
    results["Directories"] = create_directories()
    
    # Ask before installing
    if results["Virtual Environment"]:
        response = input("\nInstall dependencies? (y/n): ").strip().lower()
        if response == 'y':
            results["Dependencies"] = install_dependencies()
        else:
            print("⏭️  Skipping dependency installation")
            results["Dependencies"] = None
    else:
        print("\n⚠️  Skipping dependency installation (not in venv)")
        results["Dependencies"] = None
    
    if results.get("Dependencies"):
        results["Package Imports"] = test_imports()
        results["Model Files"] = check_model_files()
        
        # Database setup
        response = input("\nSetup database? (y/n): ").strip().lower()
        if response == 'y':
            results["Database Connection"] = test_database_connection()
            if results["Database Connection"]:
                results["Database Initialization"] = initialize_database()
        else:
            print("⏭️  Skipping database setup")
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)
