# modules/ai_core.py - UPDATED FOR OPENAI v1.0.0+
import openai
import json
import os
import random
from dotenv import load_dotenv
from openai import OpenAI  # New import for v1.0.0+

# STEP 1: Load environment variables from .env file
load_dotenv()

# STEP 2: Get the values
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# STEP 3: Define MODEL_CONFIG
MODEL_CONFIG = {
    "openai": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

class StudentAIAssistant:
    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY
        if self.openai_api_key:
            # Initialize the OpenAI client for v1.0.0+
            self.client = OpenAI(api_key=self.openai_api_key)
            self.use_openai = True
        else:
            self.client = None
            self.use_openai = False
            print("⚠️ OpenAI API key not found. Using mock responses.")
    
    def ask_question(self, question, subject=None):
        """Main method to answer student questions"""
        
        if self.use_openai:
            return self._ask_openai(question, subject)
        else:
            return self._mock_response(question, subject)
    
    def _ask_openai(self, question, subject=None):
        """Use OpenAI API for real responses (v1.0.0+ syntax)"""
        try:
            system_prompt = f"""You are a helpful, patient, and knowledgeable student tutor.
            You specialize in {subject if subject else 'all subjects'}.
            Always explain concepts step-by-step.
            Encourage critical thinking and ask follow-up questions.
            If you don't know something, admit it and suggest resources."""
            
            # NEW SYNTAX for openai>=1.0.0
            response = self.client.chat.completions.create(
                model=MODEL_CONFIG["openai"]["model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=MODEL_CONFIG["openai"]["temperature"],
                max_tokens=MODEL_CONFIG["openai"]["max_tokens"]
            )
            
            # NEW: Access the content differently
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error: {str(e)}. Using mock response instead.\n\n{self._mock_response(question, subject)}"
    
    def _mock_response(self, question, subject=None):
        """Generate mock responses when API is unavailable"""
        responses = [
            f"I understand you're asking about: '{question}'",
            f"For {subject if subject else 'this topic'}, I'd suggest breaking it down into smaller parts.",
            "Let me explain this concept step by step...",
            "A good approach would be to start with the basics and build up.",
            "Have you tried looking at this from a different perspective?",
            "This is an excellent question! Let me help you understand it better."
        ]
        
        return random.choice(responses)
    
    def generate_flashcards(self, topic, count=5):
        """Generate study flashcards for a topic"""
        prompt = f"""Generate {count} study flashcards about '{topic}'.
        Format each flashcard as JSON with:
        - question: Clear, concise question
        - answer: Detailed, educational answer
        - difficulty: easy/medium/hard
        - category: relevant subject category
        
        Return ONLY valid JSON array."""
        
        if self.use_openai:
            try:
                # NEW SYNTAX for openai>=1.0.0
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"Flashcard generation failed: {e}")
                # Fall back to mock flashcards
        
        # Mock flashcards if API fails or not available
        return self._mock_flashcards(topic, count)
    
    def _mock_flashcards(self, topic, count):
        """Generate mock flashcards"""
        flashcards = []
        for i in range(count):
            flashcards.append({
                "question": f"What is key concept {i+1} about {topic}?",
                "answer": f"This is the detailed explanation for concept {i+1}.",
                "difficulty": ["easy", "medium", "hard"][i % 3],
                "category": topic
            })
        return flashcards
