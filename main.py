# from backend.ai_service import AIService
# from backend.user_service import UserService

# if __name__ == "__main__":
#     ai_service = AIService()
#     user_service = UserService(ai_service)
    
#     user_id = input("Enter your User ID: ")  # Get user ID input

#     while True:
#         user_query = input("\nAsk a question (or type 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Goodbye!")
#             break

#         response = user_service.handle_user_query(user_query, user_id)
#         print("\nAI Response:", response)

import streamlit as st
import pandas as pd
import speech_recognition as sr
import pyttsx3

from backend.ai_service import AIService
from backend.user_service import UserService


st.set_page_config(
    page_title="Elderly Care Assistant",  # ✅ Custom title
    page_icon="🤖",                      # ✅ Emoji or path to .ico/.png
    layout="centered",                   # or "wide"
    initial_sidebar_state="auto"         # or "expanded" / "collapsed"
)

# Initialize Services
ai_service = AIService()
user_service = UserService(ai_service)

st.title("🧠 Elderly AI Assistant with Voice Support")

# Text-to-Speech Function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Voice Input Handler
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

# Input: User ID
user_id = st.text_input("Enter your User ID")

if user_id:
    use_voice = st.checkbox("🎙️ Use voice input")

    if use_voice and st.button("🎧 Start Voice Input"):
        user_query = recognize_speech()
    else:
        user_query = st.text_area("Ask your question", height=100)

    if st.button("🚀 Submit"):
        if user_query.lower().strip() == "exit":
            st.info("👋 Goodbye! Please refresh to start again.")
        else:
            # Sample dynamic data
            reminders = ai_service.reminder_service.get_reminders(user_id)
            health_status = ai_service.health_service.get_health_status(user_id)
            safety_alerts = ai_service.safety_service.get_safety_alerts(user_id)

            response = user_service.handle_user_query(user_query, user_id)

            # Display Data
            st.subheader("📌 Reminders")
            st.dataframe(pd.DataFrame(reminders) if isinstance(reminders, list) else reminders)

            st.subheader("❤️ Health Status")
            st.dataframe(pd.DataFrame([health_status]) if isinstance(health_status, dict) else health_status)

            st.subheader("🛡️ Safety Alerts")
            st.dataframe(pd.DataFrame([safety_alerts]) if isinstance(safety_alerts, dict) else safety_alerts)

            st.subheader("🤖 AI Response")
            st.success(response)
            speak(response)
