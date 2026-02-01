# modules/gemini_core.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiAssistant:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_gemini = True
        else:
            self.use_gemini = False
            print("⚠️ Gemini API key not found. Using mock responses.")
    
    def ask_question(self, question):
        if self.use_gemini:
            try:
                response = self.model.generate_content(
                    f"As a student tutor, explain: {question}"
                )
                return response.text
            except Exception as e:
                return f"Error: {e}"
        return f"Mock response to: {question}"
