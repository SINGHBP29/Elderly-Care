import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from backend.ai_service import AIService
from ai_agents import execute_multi_agent_summary

st.set_page_config(
    page_title="Caretaker Dashboard",
    page_icon="🧑‍⚕️",
    layout="centered"
)

ai_service = AIService()

st.title("🧑‍⚕️ Caretaker Dashboard")

elder_name = st.selectbox("Select Elder", ["Elder1", "Elder2", "Elder3"])

st.header("📊 Health Summary")
health = ai_service.health_service.get_health_status(elder_name)
if isinstance(health, dict):
    st.dataframe(pd.DataFrame([health]))

st.header("⏰ Set Reminders for Elder")
reminder_type = st.selectbox("Reminder Type", ["Exercise", "Medication", "Appointment"])
reminder_text = st.text_input("Reminder Text")
if st.button("Set Reminder"):
    ai_service.reminder_service.set_reminder(elder_name, reminder_type, reminder_text)
    st.success("Reminder Set Successfully")

# -------------------------------
# 🧠 FAISS Integration + Crew Agent Summary
# -------------------------------
@st.cache_resource
def load_faiss_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [
        "Caretaker checkup on 8th April",
        "Mood check: feeling anxious",
        "Emergency alert triggered on Monday",
        "Vitals stable this week"
    ]
    embeddings = model.encode(texts)
    # index = faiss.IndexFlatL2(384)
    # index.add(np.array(embeddings))
    index = faiss.IndexFlatIP(384)  # ✅ Use Inner Product (cosine similarity)
    faiss.normalize_L2(embeddings)
    return index, texts, model

st.header("🧠 Ask about care history")
query = st.text_input("Ask a question about caretaker notes or safety alerts")

if query:
    index, texts, model = load_faiss_index()
    query_embedding = model.encode([query])
    _, I = index.search(np.array(query_embedding), k=2)
    context = "\n".join([texts[i] for i in I[0]])

    st.subheader("🔍 Context Matches")
    for i in I[0]:
        st.write(f"- {texts[i]}")

    st.subheader("🧠 AI Agent Response")
    response = execute_multi_agent_summary(query)
    st.success(response)