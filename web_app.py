# web_app.py
import streamlit as st
import sys
import os
from pathlib import Path

# Add project modules to path
sys.path.append(str(Path(__file__).parent))

from modules.free_ai_core import FreeStudentAI
from modules.flashcard_generator import FlashcardSystem

# Configure the page
st.set_page_config(
    page_title="Student AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize AI and flashcard system
@st.cache_resource
def load_ai():
    return FreeStudentAI()

@st.cache_resource
def load_flashcard_system():
    return FlashcardSystem()

ai = load_ai()
flashcard_sys = load_flashcard_system()

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E0F2FE;
        border-left: 5px solid #0EA5E9;
    }
    .bot-message {
        background-color: #F0F9FF;
        border-left: 5px solid #10B981;
    }
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎓 Student AI Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Your personal tutor for all subjects")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=100)
    st.markdown("### 📚 Navigation")
    
    menu = st.radio(
        "Choose a feature:",
        ["🤖 AI Tutor", "📚 Flashcards", "🎯 Quiz", "📊 Statistics", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### 🎓 Subjects")
    subjects = ["Math", "Science", "History", "English", "Programming", "General"]
    selected_subject = st.selectbox("Select subject:", subjects)
    
    st.markdown("---")
    st.markdown("#### 📖 Quick Tips")
    with st.expander("Study Tips"):
        st.write("""
        - Study in 25-minute intervals
        - Teach what you learn to others
        - Use flashcards for memorization
        - Get enough sleep before exams
        """)

# Main content based on menu selection
if menu == "🤖 AI Tutor":
    st.markdown('<h2 class="sub-header">💬 Ask AI Tutor</h2>', unsafe_allow_html=True)
    
    # Chat input
    question = st.text_input("Ask any academic question:", placeholder="e.g., What is photosynthesis?")
    
    if question:
        with st.spinner("Thinking..."):
            response = ai.ask_question(question, selected_subject)
        
        # Display conversation
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
        with col2:
            st.markdown(f'<div class="chat-message user-message"><b>You:</b> {question}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
        with col2:
            st.markdown(f'<div class="chat-message bot-message"><b>AI Tutor:</b> {response}</div>', unsafe_allow_html=True)
    
    # Example questions
    st.markdown("### 💡 Example Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Explain photosynthesis"):
            st.session_state.example_q = "Explain photosynthesis"
    with col2:
        if st.button("Solve 2x+5=15"):
            st.session_state.example_q = "Solve 2x+5=15"
    with col3:
        if st.button("Python functions"):
            st.session_state.example_q = "Explain Python functions"

elif menu == "📚 Flashcards":
    st.markdown('<h2 class="sub-header">📚 Create Study Flashcards</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input("Enter topic:", placeholder="e.g., Python Basics")
        count = st.slider("Number of flashcards:", 1, 20, 5)
        
        if st.button("Generate Flashcards", type="primary"):
            if topic:
                with st.spinner(f"Creating {count} flashcards about {topic}..."):
                    flashcards = flashcard_sys.generate(topic, count, save=True)
                
                st.success(f"✅ Generated {len(flashcards)} flashcards!")
                
                # Display flashcards
                st.markdown("### 📝 Your Flashcards:")
                for i, card in enumerate(flashcards, 1):
                    with st.expander(f"Card {i}: {card['question'][:50]}..."):
                        st.write(f"**Question:** {card['question']}")
                        st.write(f"**Answer:** {card['answer']}")
                        st.write(f"**Difficulty:** {card['difficulty'].upper()}")
            else:
                st.warning("Please enter a topic!")
    
    with col2:
        # Load existing flashcards
        st.markdown("### 📂 Saved Flashcard Sets")
        sets = flashcard_sys.list_saved_sets()
        
        if sets:
            selected_set = st.selectbox(
                "Choose a set:",
                [f"{s['filename']} ({s['count']} cards)" for s in sets]
            )
            
            if st.button("Load Selected Set"):
                # Extract filename from selection
                filename = selected_set.split(" (")[0]
                flashcards = flashcard_sys.load_flashcards(filename)
                st.session_state.loaded_flashcards = flashcards
                st.success(f"Loaded {len(flashcards)} flashcards!")
        else:
            st.info("No saved flashcard sets yet. Generate some first!")

elif menu == "🎯 Quiz":
    st.markdown('<h2 class="sub-header">🎯 Test Your Knowledge</h2>', unsafe_allow_html=True)
    
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
        st.session_state.quiz_index = 0
        st.session_state.show_answer = False
        st.session_state.quiz_complete = False
    
    # Check if we have flashcards
    if not flashcard_sys.flashcards:
        st.warning("No flashcards available. Generate some in the Flashcards section first!")
        
        # Option to generate quick flashcards
        if st.button("Generate Sample Flashcards"):
            with st.spinner("Creating sample flashcards..."):
                flashcard_sys.generate("General Knowledge", 5)
            st.rerun()
    else:
        total = len(flashcard_sys.flashcards)
        current_idx = st.session_state.quiz_index
        
        if current_idx < total and not st.session_state.quiz_complete:
            card = flashcard_sys.flashcards[current_idx]
            
            st.progress((current_idx / total), text=f"Question {current_idx + 1} of {total}")
            
            st.markdown(f"### ❓ Question {current_idx + 1}")
            st.markdown(f"**{card['question']}**")
            st.markdown(f"*Category: {card['category']} • Difficulty: {card['difficulty'].upper()}*")
            
            if not st.session_state.show_answer:
                if st.button("Reveal Answer"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                st.markdown(f"### ✅ Answer")
                st.info(card['answer'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ I Got It Right!"):
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
                with col2:
                    if st.button("❌ I Was Wrong"):
                        st.session_state.quiz_index += 1
                        st.session_state.show_answer = False
                        st.rerun()
        
        elif st.session_state.quiz_complete or current_idx >= total:
            score = st.session_state.quiz_score
            percentage = (score / total) * 100
            
            st.markdown("## 🏁 Quiz Complete!")
            st.markdown(f"### 📊 Your Score: **{score}/{total}** ({percentage:.1f}%)")
            
            if percentage >= 80:
                st.balloons()
                st.success("🎉 Excellent! You're a master!")
            elif percentage >= 60:
                st.success("👍 Good job! Well done!")
            else:
                st.info("📚 Keep studying! You'll do better next time.")
            
            if st.button("Restart Quiz"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_index = 0
                st.session_state.show_answer = False
                st.session_state.quiz_complete = False
                st.rerun()

elif menu == "📊 Statistics":
    st.markdown('<h2 class="sub-header">📊 Learning Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sets = flashcard_sys.list_saved_sets()
        st.metric("Flashcard Sets", len(sets))
    
    with col2:
        total_cards = sum(s['count'] for s in sets) if sets else 0
        st.metric("Total Flashcards", total_cards)
    
    with col3:
        # Mock progress (you can implement real tracking)
        st.metric("Study Streak", "3 days")
    
    # Flashcard sets table
    if sets:
        st.markdown("### 📁 Your Flashcard Sets")
        for s in sets:
            with st.expander(f"{s['filename']} - {s['count']} cards"):
                st.write(f"**Topic:** {s['topic']}")
                st.write(f"**Created:** {s.get('created', 'Unknown')}")
                st.write(f"**Path:** `{s['path']}`")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Load {s['filename']}", key=f"load_{s['filename']}"):
                        flashcard_sys.load_flashcards(s['filename'])
                        st.success(f"Loaded {s['count']} flashcards!")
                        st.rerun()
                with col2:
                    if st.button(f"Delete {s['filename']}", key=f"delete_{s['filename']}"):
                        flashcard_sys.delete_set(s['filename'])
                        st.warning(f"Deleted {s['filename']}")
                        st.rerun()
    else:
        st.info("No flashcard sets yet. Create some in the Flashcards section!")

elif menu == "⚙️ Settings":
    st.markdown('<h2 class="sub-header">⚙️ Settings & Configuration</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Configuration")
    
    with st.form("api_config"):
        gemini_key = st.text_input("Gemini API Key:", type="password", 
                                   help="Get from https://makersuite.google.com/app/apikey")
        deepseek_key = st.text_input("DeepSeek API Key:", type="password",
                                     help="Get from https://platform.deepseek.com/api_keys")
        
        if st.form_submit_button("Save API Keys"):
            # Save to .env file
            env_path = Path(__file__).parent / ".env"
            with open(env_path, 'w') as f:
                if gemini_key:
                    f.write(f"GEMINI_API_KEY={gemini_key}\n")
                if deepseek_key:
                    f.write(f"DEEPSEEK_API_KEY={deepseek_key}\n")
            
            st.success("API keys saved! Restart app to apply changes.")
    
    st.markdown("---")
    st.markdown("### 🛠️ System Information")
    
    import platform
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Python Version:** {platform.python_version()}")
        st.write(f"**Streamlit Version:** {st.__version__}")
    
    with col2:
        st.write(f"**OS:** {platform.system()} {platform.release()}")
        st.write(f"**Available AI Services:** {', '.join(ai.available_services) if ai.available_services else 'Local Knowledge Base'}")
    
    if st.button("Clear Cache & Restart"):
        st.cache_resource.clear()
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>🎓 Student AI Assistant • Built with Python & Streamlit • Free for Educational Use</p>
    <p>💡 Need help? Ask questions in any subject area!</p>
</div>
""", unsafe_allow_html=True)
