import os
import requests
import json
from dotenv import load_dotenv
from backend.remainder_service import ReminderService
from backend.health_service import HealthService
from backend.safety_service import SafetyService
# 
# Load API Key from .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set in the .env file")

class AIService:
    def __init__(self):
        self.reminder_service = ReminderService()
        self.health_service = HealthService()
        self.safety_service = SafetyService()
        self.model_endpoint = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

    def query_huggingface(self, prompt):
        """Send a query to Hugging Face FLAN-T5 XL API."""
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}

        try:
            response = requests.post(self.model_endpoint, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                # FLAN models usually return a 'generated_text' key
                result = response.json()
                return result[0].get("generated_text", result[0].get("output", result))
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"

    def generate_response(self, user_query, user_id):
        """Generate an AI response based on user data and query."""
        reminders = self.reminder_service.get_reminders(user_id)
        health_status = self.health_service.get_health_status(user_id)
        safety_alerts = self.safety_service.get_safety_alerts(user_id)

        prompt = f"""
        You are an AI assistant helping an elderly person. Below is their latest information:

        - Reminders: {reminders}
        - Health Status: {health_status}
        - Safety Alerts: {safety_alerts}

        User's question: "{user_query}"

        Provide a helpful and supportive response.
        """

        return self.query_huggingface(prompt)


# import os
# from dotenv import load_dotenv
# from langchain.llms import HuggingFaceHub
# from backend.remainder_service import ReminderService
# from backend.health_service import HealthService
# from backend.safety_service import SafetyService

# # Load API Key from .env
# load_dotenv()
# HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# if not HF_API_KEY:
#     raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the .env file")

# # Set the API token environment variable
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_API_KEY

# class AIService:
#     def __init__(self):
#         self.reminder_service = ReminderService()
#         self.health_service = HealthService()
#         self.safety_service = SafetyService()
#         self.llm = HuggingFaceHub(
#             repo_id="google/flan-t5-xl",
#             model_kwargs={
#                 "temperature": 0.7,
#                 "max_new_tokens": 256
#             }
#         )

#     def generate_response(self, user_query, user_id):
#         """Generate an AI response based on user data and query."""
#         reminders = self.reminder_service.get_reminders(user_id)
#         health_status = self.health_service.get_health_status(user_id)
#         safety_alerts = self.safety_service.get_safety_alerts(user_id)

#         prompt = f"""
#         You are an AI assistant helping an elderly person. Below is their latest information:

#         - Reminders: {reminders}
#         - Health Status: {health_status}
#         - Safety Alerts: {safety_alerts}

#         User's question: "{user_query}"

#         Provide a helpful and supportive response.
#         """

#         return self.llm(prompt)
