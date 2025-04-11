import streamlit as st
import pandas as pd
import speech_recognition as sr
import pyttsx3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from backend.ai_service import AIService
from backend.user_service import UserService
from ai_agents import execute_multi_agent_summary  # ✅ Multi-agent execution

import os
os.environ["STREAMLIT_WATCHED_MODULES"] = "streamlit"

# -------------------------------
# ⚙️ Initial Setup
# -------------------------------
st.set_page_config(
    page_title="Elderly Care Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🧠 Elderly AI Assistant with Voice Support")

ai_service = AIService()
user_service = UserService(ai_service)

col1, col2 = st.columns(2)

with col1:
    if st.button("👵 I am an Elder"):
        st.switch_page("pages/elder_dashboard (1).py")

with col2:
    if st.button("🧑‍⚕️ I am a Caretaker"):
        st.switch_page("pages/caretaker_dashboard.py")

# -------------------------------
# 🎤 Voice & TTS Utilities
# -------------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("⚠️ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ API unavailable or no internet.")
    return ""

# -------------------------------
# ✅ FAISS SETUP
# -------------------------------
@st.cache_resource
def load_faiss_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [
        "Take medicine at 8 AM", 
        "Doctor appointment at 5 PM", 
        "Drink water every hour",
        "Your blood pressure is normal",
        "You had a fall last week"
    ]
    embeddings = model.encode(texts, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(384)
    index.add(embeddings)
    return index, texts, model

# -------------------------------
# 🧠 Main Interaction
# -------------------------------
user_id = st.text_input("Enter your User ID")

if user_id:
    use_voice = st.checkbox("🎙️ Use voice input")

    if use_voice and st.button("🎧 Start Voice Input"):
        user_query = recognize_speech()
    else:
        user_query = st.text_area("Ask your question", height=100)

    if st.button("🚀 Submit") and user_query:
        # Load FAISS only on query
        index, stored_texts, embedder = load_faiss_index()

        # 🔍 FAISS Search
        user_vector = embedder.encode([user_query], convert_to_numpy=True)
        faiss.normalize_L2(user_vector)
        _, I = index.search(user_vector, k=2)
        context = "\n".join([stored_texts[i] for i in I[0]])

        # 🤖 Run Multi-Agent AI
        response = execute_multi_agent_summary(user_query)

        # 🔎 Retrieve Dynamic Data
        reminders = ai_service.reminder_service.get_reminders(user_id)
        health_status = ai_service.health_service.get_health_status(user_id)
        safety_alerts = ai_service.safety_service.get_safety_alerts(user_id)

        # 📊 Display Results
        st.subheader("📌 Reminders")
        st.dataframe(pd.DataFrame(reminders) if isinstance(reminders, list) else reminders)

        st.subheader("❤️ Health Status")
        st.dataframe(pd.DataFrame([health_status]) if isinstance(health_status, dict) else health_status)

        st.subheader("🛡️ Safety Alerts")
        st.dataframe(pd.DataFrame([safety_alerts]) if isinstance(safety_alerts, dict) else safety_alerts)

        st.subheader("🧠 Top Semantic Matches (FAISS)")
        st.write(context)

        st.subheader("🤖 AI Response")
        st.success(response)
        speak(response)
