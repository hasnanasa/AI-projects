# modules/free_ai_core.py
import json
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

class FreeStudentAI:
    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
        
        # Try to initialize available services
        self.available_services = []
        
        if self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.available_services.append("gemini")
                print("✅ Gemini AI: Ready")
            except:
                print("⚠️ Gemini: Failed to initialize")
        
        if self.deepseek_key:
            self.available_services.append("deepseek")
            print("✅ DeepSeek: Ready")
        
        if not self.available_services:
            print("⚠️ No free AI APIs configured. Using enhanced knowledge base.")
            print("   Get free keys:")
            print("   - Gemini: https://makersuite.google.com/app/apikey")
            print("   - DeepSeek: https://platform.deepseek.com/api_keys")
    
    def ask_question(self, question, subject=None):
        """Ask question using available free AI"""
        
        # Try Gemini first
        if "gemini" in self.available_services:
            response = self._ask_gemini(question, subject)
            if response and "Error" not in response:
                return response
        
        # Try DeepSeek second
        if "deepseek" in self.available_services:
            response = self._ask_deepseek(question)
            if response and "Error" not in response:
                return response
        
        # Fallback to enhanced knowledge base
        return self._enhanced_knowledge_response(question, subject)
    
    def _ask_gemini(self, question, subject=None):
        """Use Google Gemini AI (free)"""
        try:
            import google.generativeai as genai
            
            prompt = f"""You are a helpful, patient student tutor.
            Explain this in simple, step-by-step manner: {question}
            
            If relevant to subject ({subject}), focus on that.
            Use examples and analogies students can understand."""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Gemini Error: {str(e)[:100]}"
    
    def _ask_deepseek(self, question):
        """Use DeepSeek AI (free)"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a helpful student tutor. Explain concepts simply and step-by-step."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            return f"DeepSeek Error: {str(e)[:100]}"
    
    def _enhanced_knowledge_response(self, question, subject=None):
        """Enhanced local knowledge base when no AI is available"""
        knowledge_base = {
            # Science
            "photosynthesis": """🌿 **PHOTOSYNTHESIS**
Plants convert sunlight, water, and CO₂ into food (glucose) and oxygen.

**Process:**
1. Sunlight absorbed by chlorophyll (green pigment)
2. Water absorbed by roots (H₂O)
3. Carbon dioxide from air (CO₂)
4. Produces: Glucose (C₆H₁₂O₆) + Oxygen (O₂)

**Equation:** 6CO₂ + 6H₂O + sunlight → C₆H₁₂O₆ + 6O₂

**Importance:**
• Produces oxygen we breathe
• Base of food chain
• Removes CO₂ from air""",
            
            "mitochondria": """🔬 **MITOCHONDRIA - Cell Powerhouse**
Produces ATP (energy) through cellular respiration.

**Structure:**
- Double membrane
- Inner folds = cristae
- Matrix inside

**ATP Production:** ~36 ATP per glucose molecule""",
            
            # Math
            "algebra": """🧮 **ALGEBRA BASICS**
Solving equations: Isolate the variable.

**Example:** 3x + 5 = 14
1. Subtract 5: 3x = 9
2. Divide by 3: x = 3

**Check:** 3(3) + 5 = 9 + 5 = 14 ✓""",
            
            "geometry": """📐 **GEOMETRY FORMULAS**
• Circle Area = πr²
• Circle Circumference = 2πr
• Triangle Area = ½ × base × height
• Rectangle Area = length × width
• Volume of cube = side³""",
            
            # History
            "world war": """📜 **WORLD WAR II (1939-1945)**
**Allies:** USA, UK, USSR, France, China
**Axis:** Germany, Italy, Japan

**Key Events:**
• 1939: Germany invades Poland
• 1941: Pearl Harbor attack
• 1944: D-Day invasion
• 1945: Atomic bombs, war ends

**Aftermath:** UN formed, Cold War began""",
            
            # Programming
            "python": """🐍 **PYTHON PROGRAMMING**
```python
# Variables
name = "Student"
age = 16

# Functions
def greet(name):
    return f"Hello, {name}!"

# Lists
numbers = [1, 2, 3, 4, 5]

# Loops
for i in range(5):
    print(i)
```"""
        }
        
        # Search for keywords
        question_lower = question.lower()
        for keyword, answer in knowledge_base.items():
            if keyword in question_lower:
                return answer
        
        # Subject-based responses
        subject_responses = {
            "math": """🧮 **Math Study Strategy:**
1. Understand formulas
2. Practice with examples
3. Show all steps
4. Check your work
5. Learn from mistakes""",
            
            "science": """🔬 **Scientific Method:**
1. Observe
2. Question
3. Hypothesize
4. Experiment
5. Analyze
6. Conclude""",
            
            "history": """📜 **Historical Analysis:**
• When did it happen?
• Why did it happen?
• What occurred?
• What were effects?
• Why does it matter?""",
            
            "english": """📖 **Writing Guide:**
Introduction → Body → Conclusion
Use clear thesis, evidence, analysis.
Check grammar and spelling."""
        }
        
        if subject and subject.lower() in subject_responses:
            return subject_responses[subject.lower()]
        
        # Smart generic response
        tips = [
            f"**Approach to '{question}':**\n1. Break into smaller parts\n2. Research each part\n3. Connect concepts\n4. Practice application",
            f"**Understanding {question}:**\nStart with fundamentals, build up gradually, use examples.",
            f"**Study Strategy:**\nDefine terms → Understand relationships → Apply knowledge → Review regularly",
            f"**For {question}, consider:**\n• What's being asked?\n• What do you know?\n• What do you need?\n• How to connect them?"
        ]
        
        return random.choice(tips)
    
    def generate_flashcards(self, topic, count=5):
        """Generate flashcards using available AI"""
        prompt = f"""Create {count} study flashcards about '{topic}' for students.
        Each flashcard should have:
        - A clear question
        - A detailed answer
        - Difficulty level (easy/medium/hard)
        - Category
        
        Format as JSON array with these keys: question, answer, difficulty, category"""
        
        # Try Gemini
        if "gemini" in self.available_services:
            try:
                import google.generativeai as genai
                response = self.gemini_model.generate_content(prompt)
                return json.loads(response.text)
            except:
                pass
        
        # Try DeepSeek
        if "deepseek" in self.available_services:
            try:
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.deepseek_key}"}
                data = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000
                }
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                return json.loads(result['choices'][0]['message']['content'])
            except:
                pass
        
        # Fallback to local generation
        return self._local_flashcards(topic, count)
    
    def _local_flashcards(self, topic, count):
        """Generate local flashcards without AI"""
        flashcards = []
        
        templates = [
            (f"What is {topic}?", f"{topic} is a fundamental concept with many applications.", "easy"),
            (f"Why study {topic}?", f"Understanding {topic} helps with related concepts and real-world problems.", "medium"),
            (f"Key principle of {topic}:", f"The main principle involves...", "medium"),
            (f"Example of {topic} in real life:", f"Used in...", "easy"),
            (f"Common mistake in {topic}:", f"Students often confuse...", "hard"),
            (f"How to solve {topic} problems:", f"Step 1:... Step 2:...", "medium"),
            (f"History of {topic}:", f"Developed by... in year...", "hard")
        ]
        
        for i in range(count):
            idx = i % len(templates)
            question, answer, difficulty = templates[idx]
            
            flashcards.append({
                "question": question,
                "answer": answer,
                "difficulty": difficulty,
                "category": topic
            })
        
        return flashcards

# Test the module
if __name__ == "__main__":
    ai = FreeStudentAI()
    
    # Test with and without API keys
    questions = [
        "What is photosynthesis?",
        "How to solve 2x + 5 = 15?",
        "Explain Python functions"
    ]
    
    for q in questions:
        print(f"\n{'='*50}")
        print(f"❓ Question: {q}")
        print(f"{'='*50}")
        answer = ai.ask_question(q)
        print(f"🤖 Answer:\n{answer}")
