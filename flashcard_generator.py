# modules/flashcard_generator.py - FIXED VERSION
import json
import os
from datetime import datetime
from pathlib import Path

# Define paths directly here - NO config import
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
FLASHCARDS_DIR = DATA_DIR / "flashcards"

# Create directories if they don't exist
for directory in [DATA_DIR, FLASHCARDS_DIR]:
    directory.mkdir(exist_ok=True)

class FlashcardSystem:
    def __init__(self):
        self.flashcards = []
        print(f"📚 Flashcard system ready. Data directory: {FLASHCARDS_DIR}")
    
    def generate(self, topic, count=10, save=True):
        """Generate flashcards for a topic"""
        print(f"📝 Generating {count} flashcards about '{topic}'...")
        
        # Simple flashcard generation
        flashcards = self._simple_flashcards(topic, count)
        
        if save:
            self.save_flashcards(flashcards, topic)
        
        self.flashcards.extend(flashcards)
        return flashcards
    
    def _simple_flashcards(self, topic, count):
        """Generate simple flashcards"""
        flashcards = []
        
        # Topic templates
        templates = {
            "python": [
                ("What is a variable in Python?", "A named storage location for data.", "easy"),
                ("How to define a function?", "Use 'def' keyword: def function_name():", "easy"),
                ("What is a list?", "An ordered, mutable collection of items.", "medium"),
                ("How to loop through items?", "Use for loop: for item in collection:", "medium"),
                ("What are Python modules?", "Files containing Python code that can be imported.", "hard"),
            ],
            "math": [
                ("Solve 2x + 5 = 15", "x = 5", "easy"),
                ("Area of a circle?", "πr²", "easy"),
                ("What is 3²?", "9", "easy"),
                ("Solve 3x - 7 = 14", "x = 7", "medium"),
                ("Derivative of x²?", "2x", "medium"),
            ],
            "science": [
                ("What is photosynthesis?", "Plants convert sunlight to food.", "easy"),
                ("What is a cell?", "Basic unit of life.", "easy"),
                ("Define gravity", "Force that attracts objects with mass.", "medium"),
                ("What is H₂O?", "Water", "easy"),
                ("What is DNA?", "Genetic material carrying instructions.", "hard"),
            ],
            "history": [
                ("When was WWII?", "1939-1945", "easy"),
                ("Who was first US president?", "George Washington", "easy"),
                ("What caused French Revolution?", "Social inequality and financial crisis.", "medium"),
                ("When did Titanic sink?", "1912", "medium"),
                ("Who invented telephone?", "Alexander Graham Bell", "medium"),
            ]
        }
        
        # Find matching template
        found_template = None
        topic_lower = topic.lower()
        for key in templates:
            if key in topic_lower:
                found_template = templates[key]
                break
        
        if not found_template:
            # Generic template
            found_template = [
                (f"What is {topic}?", f"{topic} is an important concept worth studying.", "medium"),
                (f"Why study {topic}?", f"Understanding {topic} helps in many real-world applications.", "medium"),
                (f"Key concept in {topic}:", f"A fundamental concept is...", "medium"),
                (f"Example of {topic}:", f"For example...", "easy"),
                (f"Application of {topic}:", f"Used in fields like...", "hard"),
            ]
        
        # Generate flashcards
        for i in range(count):
            idx = i % len(found_template)
            question, answer, difficulty = found_template[idx]
            
            flashcards.append({
                "id": i + 1,
                "question": question,
                "answer": answer,
                "difficulty": difficulty,
                "category": topic,
                "created": datetime.now().isoformat()
            })
        
        return flashcards
    
    def save_flashcards(self, flashcards, topic):
        """Save flashcards to JSON file"""
        filename = f"{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = FLASHCARDS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(flashcards, f, indent=2)
        
        print(f"💾 Saved {len(flashcards)} flashcards to {filepath}")
        return filepath
    
    def load_flashcards(self, filename=None):
        """Load flashcards from JSON file"""
        if filename:
            filepath = FLASHCARDS_DIR / filename
        else:
            # Load most recent file
            files = list(FLASHCARDS_DIR.glob("*.json"))
            if not files:
                return []
            filepath = max(files, key=os.path.getctime)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.flashcards = json.load(f)
            print(f"📂 Loaded {len(self.flashcards)} flashcards from {filepath.name}")
            return self.flashcards
        return []
    
    def quiz_mode(self):
        """Interactive quiz mode"""
        if not self.flashcards:
            print("❌ No flashcards available. Generate or load some first!")
            return
        
        print("\n" + "="*50)
        print("🎯 FLASHCARD QUIZ")
        print("="*50)
        
        score = 0
        total = len(self.flashcards)
        
        for i, card in enumerate(self.flashcards, 1):
            print(f"\n📊 Progress: {i}/{total}")
            print(f"📝 Question: {card['question']}")
            print(f"🏷️  Category: {card['category']}")
            print(f"⚡ Difficulty: {card['difficulty'].upper()}")
            
            input("\nPress Enter to reveal answer...")
            print(f"✅ Answer: {card['answer']}")
            
            correct = input("\nDid you get it right? (y/n): ").lower().strip()
            if correct == 'y':
                score += 1
                print("🎉 Correct! Well done!")
            else:
                print("💡 Keep practicing this one!")
            
            print("-" * 40)
        
        percentage = (score / total) * 100
        print(f"\n{'='*50}")
        print("🏁 QUIZ COMPLETE!")
        print(f"{'='*50}")
        print(f"📊 Your score: {score}/{total} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🎖️  EXCELLENT! You've mastered this topic!")
        elif percentage >= 70:
            print("👍 GOOD JOB! You understand most concepts.")
        elif percentage >= 50:
            print("📚 FAIR. Review the flashcards again.")
        else:
            print("🔁 NEED PRACTICE. Study the material again.")
    
    def list_saved_sets(self):
        """List all saved flashcard sets"""
        if not os.path.exists(FLASHCARDS_DIR):
            return []
        
        flashcard_files = []
        for file in os.listdir(FLASHCARDS_DIR):
            if file.endswith('.json'):
                filepath = FLASHCARDS_DIR / file
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    if data:  # Check if not empty
                        flashcard_files.append({
                            'filename': file,
                            'count': len(data),
                            'topic': data[0].get('category', 'Unknown'),
                            'created': data[0].get('created', 'Unknown'),
                            'path': str(filepath)
                        })
                except:
                    continue
        
        # Sort by creation date (newest first)
        flashcard_files.sort(key=lambda x: x.get('created', ''), reverse=True)
        return flashcard_files
    
    def delete_set(self, filename):
        """Delete a flashcard set"""
        filepath = FLASHCARDS_DIR / filename
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️  Deleted {filename}")
            return True
        else:
            print(f"❌ File {filename} not found")
            return False

# Test function
def test_flashcard_system():
    """Test the flashcard system"""
    print("🧪 Testing Flashcard System...")
    fs = FlashcardSystem()
    
    # Generate test flashcards
    cards = fs.generate("Python Basics", 3)
    
    print(f"\n✅ Generated {len(cards)} flashcards:")
    for i, card in enumerate(cards, 1):
        print(f"\nCard {i}:")
        print(f"  Q: {card['question']}")
        print(f"  A: {card['answer']}")
        print(f"  📊 Difficulty: {card['difficulty']}")
    
    # List saved sets
    sets = fs.list_saved_sets()
    if sets:
        print(f"\n📁 Found {len(sets)} saved flashcard sets")
        for s in sets[:3]:  # Show first 3
            print(f"  • {s['filename']} ({s['count']} cards)")

if __name__ == "__main__":
    test_flashcard_system()
