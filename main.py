# main.py - FIXED VERSION
#!/usr/bin/env python3
"""
Main Student Chatbot Application
Run with: python main.py
"""

import os
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))

# Define paths directly here (no config import needed)
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FLASHCARDS_DIR = DATA_DIR / "flashcards"
HOMEWORK_DIR = DATA_DIR / "homework_scans"
USER_DATA_DIR = DATA_DIR / "user_data"

from modules.free_ai_core import FreeStudentAI
from modules.flashcard_generator import FlashcardSystem
from modules.module_verifier import check_installation

class StudentChatbotApp:
    def __init__(self):
        self.ai = FreeStudentAI()
        self.flashcard_sys = FlashcardSystem()
        
        print("\n" + "="*60)
        print("           🎓 STUDENT AI CHATBOT SYSTEM           ")
        print("="*60)
        print("Loading modules...")
        
        # Check installation
        if not check_installation():
            print("\n⚠️  Some dependencies might be missing.")
            print("Run: pip install -r requirements.txt")
    
    def display_menu(self):
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. 🤖 Ask AI Tutor a Question")
        print("2. 📚 Generate Study Flashcards")
        print("3. 🎯 Take Flashcard Quiz")
        print("4. 📄 Export Flashcards to PDF")
        print("5. 🔍 Check System Status")
        print("6. ❓ Help & Instructions")
        print("7. 🚪 Exit")
        print("="*60)
        
        try:
            choice = input("\nSelect an option (1-7): ").strip()
            return choice
        except KeyboardInterrupt:
            return '7'
    
    def ask_ai_tutor(self):
        print("\n" + "="*60)
        print("🤖 AI TUTOR MODE")
        print("="*60)
        print("Ask any academic question. Type 'back' to return.")
        print("-"*60)
        
        while True:
            try:
                question = input("\n📝 Your question: ").strip()
                
                if question.lower() in ['back', 'exit', 'quit']:
                    break
                
                if not question:
                    continue
                
                print("\n🤖 AI Tutor: ", end="")
                
                # Get AI response
                response = self.ai.ask_question(question)
                
                # Print with typewriter effect
                import time
                for char in response:
                    print(char, end="", flush=True)
                    time.sleep(0.01)
                print()
                
                print("-"*40)
                
            except KeyboardInterrupt:
                break
    
    def generate_flashcards_menu(self):
        print("\n" + "="*60)
        print("📚 FLASHCARD GENERATOR")
        print("="*60)
        
        topic = input("Enter topic (e.g., 'Python Loops', 'Biology Cells'): ").strip()
        if not topic:
            print("Topic cannot be empty!")
            return
        
        try:
            count = int(input("Number of flashcards (default 10): ") or "10")
        except ValueError:
            count = 10
        
        print(f"\nGenerating {count} flashcards about '{topic}'...")
        
        flashcards = self.flashcard_sys.generate(topic, count)
        
        print(f"\n✅ Generated {len(flashcards)} flashcards!")
        
        # Check if export_pdf method exists
        if hasattr(self.flashcard_sys, 'export_pdf'):
            export = input("\nExport to PDF? (y/n): ").lower()
            if export == 'y':
                filename = input("PDF filename (default: flashcards.pdf): ") or "flashcards.pdf"
                try:
                    self.flashcard_sys.export_pdf(flashcards, filename)
                except Exception as e:
                    print(f"❌ PDF export failed: {e}")
        else:
            print("\nℹ️ PDF export not available (install fpdf: pip install fpdf)")
    
    def run_quiz(self):
        print("\n" + "="*60)
        print("🎯 FLASHCARD QUIZ MODE")
        print("="*60)
        
        if not self.flashcard_sys.flashcards:
            print("No flashcards available. Generate some first!")
            return
        
        self.flashcard_sys.quiz_mode()
    
    def export_flashcards(self):
        print("\n" + "="*60)
        print("📄 EXPORT FLASHCARDS")
        print("="*60)
        
        if not self.flashcard_sys.flashcards:
            print("No flashcards to export. Generate some first!")
            return
        
        # Check if export_pdf method exists
        if not hasattr(self.flashcard_sys, 'export_pdf'):
            print("❌ PDF export not available. Install fpdf: pip install fpdf")
            return
        
        filename = input("PDF filename (default: flashcards.pdf): ") or "flashcards.pdf"
        try:
            self.flashcard_sys.export_pdf(filename=filename)
        except Exception as e:
            print(f"❌ PDF export failed: {e}")
    
    def system_status(self):
        from modules.module_verifier import check_installation, check_api_keys
        
        print("\n" + "="*60)
        print("🔍 SYSTEM STATUS")
        print("="*60)
        
        check_installation(verbose=True)
        check_api_keys()
        
        # Count flashcards
        flashcard_files = list(FLASHCARDS_DIR.glob("*.json"))
        print(f"\n📊 Statistics:")
        print(f"  • Flashcard sets: {len(flashcard_files)}")
        print(f"  • Total flashcards in memory: {len(self.flashcard_sys.flashcards)}")
        
        # Show saved sets
        if hasattr(self.flashcard_sys, 'list_saved_sets'):
            saved_sets = self.flashcard_sys.list_saved_sets()
            if saved_sets:
                print(f"\n📁 Saved flashcard sets:")
                for s in saved_sets[:5]:  # Show first 5
                    print(f"  • {s['filename']} - {s['count']} cards ({s['topic']})")
                if len(saved_sets) > 5:
                    print(f"  ... and {len(saved_sets) - 5} more")
    
    def show_help(self):
        print("\n" + "="*60)
        print("❓ HELP & INSTRUCTIONS")
        print("="*60)
        print("""
        HOW TO USE THIS SYSTEM:
        
        1. 🤖 ASK AI TUTOR:
           - Ask any academic question
           - Get step-by-step explanations
           - Uses free AI (Gemini/DeepSeek) or local knowledge
        
        2. 📚 GENERATE FLASHCARDS:
           - Enter any topic
           - Creates study questions
           - Save for later review
        
        3. 🎯 QUIZ MODE:
           - Test your knowledge
           - Track your score
           - Learn through repetition
        
        4. 📄 EXPORT:
           - Save flashcards as PDF (requires fpdf)
           - Share with classmates
           - Print for offline study
        
        FREE AI SETUP:
        1. Get Gemini API key: https://makersuite.google.com/app/apikey
        2. Get DeepSeek API key: https://platform.deepseek.com/api_keys
        3. Add to .env file:
           GEMINI_API_KEY=your_key
           DEEPSEEK_API_KEY=your_key
        
        INSTALLATION:
        1. pip install -r requirements.txt
        2. python main.py
        
        SHORTCUTS:
        - Ctrl+C to cancel any operation
        - Type 'back' to return to menu
        """)
    
    def run(self):
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.ask_ai_tutor()
            elif choice == '2':
                self.generate_flashcards_menu()
            elif choice == '3':
                self.run_quiz()
            elif choice == '4':
                self.export_flashcards()
            elif choice == '5':
                self.system_status()
            elif choice == '6':
                self.show_help()
            elif choice == '7':
                print("\n👋 Goodbye! Keep learning!")
                print("="*60)
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    # Ensure data directories exist
    for directory in [DATA_DIR, FLASHCARDS_DIR, HOMEWORK_DIR, USER_DATA_DIR]:
        directory.mkdir(exist_ok=True)
    
    # Run the application
    app = StudentChatbotApp()
    app.run()
