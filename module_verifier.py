# modules/module_verifier.py
import importlib
import sys
import os
from dotenv import load_dotenv

# STEP 1: Load environment variables from .env file
load_dotenv()

# STEP 2: Get the values (don't use "import" for this!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


def check_installation(verbose=False):
    """Check if all required modules are installed"""
    required = [
        "streamlit",
        "openai",
        "telegram",
        "flask",
        "PIL",
        "pytesseract",
        "pandas",
        "numpy",
        "fpdf",
        "dotenv",
        "transformers",
        "torch"
    ]
    
    print("🔍 Checking Python modules...")
    print("-" * 40)
    
    missing = []
    for module in required:
        try:
            importlib.import_module(module if module != "PIL" else "PIL.Image")
            if verbose:
                print(f"✅ {module}")
        except ImportError:
            if verbose:
                print(f"❌ {module}")
            missing.append(module)
    
    if verbose:
        print("-" * 40)
    
    if missing:
        print(f"⚠️  Missing {len(missing)} modules")
        return False
    
    print("✅ All Python modules are installed!")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API keys...")
    print("-" * 40)
    
    if OPENAI_API_KEY:
        print("✅ OpenAI API key: Configured")
    else:
        print("❌ OpenAI API key: Missing (add to .env file)")
    
    if TELEGRAM_BOT_TOKEN:
        print("✅ Telegram Bot Token: Configured")
    else:
        print("❌ Telegram Bot Token: Missing (optional)")
    
    print("-" * 40)

def check_system():
    """Complete system check"""
    print("\n" + "="*50)
    print("SYSTEM DIAGNOSTICS")
    print("="*50)
    
    # Python version
    print(f"Python: {sys.version}")
    
    # Check installation
    modules_ok = check_installation(verbose=True)
    
    # Check API keys
    check_api_keys()
    
    # Check directories
    print("\n📁 Checking directories...")
    for dir_name in ["data", "data/flashcards", "data/homework_scans", "data/user_data"]:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (will be created)")
    
    print("\n" + "="*50)
    return modules_ok

if __name__ == "__main__":
    check_system()
    
