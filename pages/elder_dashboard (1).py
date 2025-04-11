import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from backend.ai_service import AIService
from backend.user_service import UserService
from frontend.chatbot_component import launch_chatbot
from ai_agents import execute_multi_agent_summary  # ✅ Import Crew agent

st.set_page_config(
    page_title="Elder Dashboard",
    page_icon="👵",
    layout="centered"
)

ai_service = AIService()
user_service = UserService(ai_service)

st.title("👵 Elder Dashboard")

elder_name = st.selectbox("Select Your Name", ["Elder1", "Elder2", "Elder3"])

st.header("🧠 Chat with AI for Emotional Support")
launch_chatbot(user_service, elder_name)

st.header("⏰ Set Reminders")
reminder_type = st.selectbox("Reminder For", ["Exercise", "Medication", "Appointment"])
reminder_text = st.text_input("Reminder Message")
if st.button("Set Reminder"):
    ai_service.reminder_service.set_reminder(elder_name, reminder_type, reminder_text)
    st.success("Reminder Set Successfully")

st.header("📊 Health Summary")
health = ai_service.health_service.get_health_status(elder_name)
if isinstance(health, dict):
    st.dataframe(pd.DataFrame([health]))

# -------------------------------
# 🧠 FAISS Integration + Crew Agent Summary
# -------------------------------
@st.cache_resource
def load_faiss_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [
        "Take medicine at 8 AM",
        "Drink water every hour",
        "You had a fall last week",
        "Sleep monitoring shows improvement"
    ]
    embeddings = model.encode(texts)
    # index = faiss.IndexFlatL2(384)
    # index.add(np.array(embeddings))
    index = faiss.IndexFlatIP(384)  # ✅ Use Inner Product (cosine similarity)
    faiss.normalize_L2(embeddings)
    return index, texts, model

st.header("🧠 Ask about your care records")
query = st.text_input("Ask a health-related or reminder-related question")

if query:
    index, texts, model = load_faiss_index()
    query_embedding = model.encode([query])
    _, I = index.search(np.array(query_embedding), k=2)
    context = "\n".join([texts[i] for i in I[0]])

    st.subheader("🔍 Context Matches")
    for i in I[0]:
        st.write(f"- {texts[i]}")

    st.subheader("🤖 AI Agent Response")
    response = execute_multi_agent_summary(query)
    st.success(response)
    

# # elder_dashboard.py
# import streamlit as st
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer

# @st.cache_resource
# def load_elder_faiss():
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     texts = [
#         "Take medicine at 8 AM", 
#         "Drink water every hour",
#         "Your blood pressure is normal",
#         "Sleep monitoring shows improvement"
#     ]
#     embeddings = model.encode(texts)
#     index = faiss.IndexFlatL2(384)
#     index.add(np.array(embeddings))
#     return index, texts, model

# st.title("👵 Elder Dashboard")

# query = st.text_input("Ask something about your health or schedule")

# if query:
#     index, texts, model = load_elder_faiss()
#     query_embedding = model.encode([query])
#     _, I = index.search(np.array(query_embedding), k=2)
#     st.subheader("🧠 Matches")
#     for i in I[0]:
#         st.write(f"- {texts[i]}")

