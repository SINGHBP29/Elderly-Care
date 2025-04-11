# from crewai import Crew, Task, Agent
# # from litellm import completion
# import os
# from dotenv import load_dotenv
# from litellm import completion
# import requests
# import json
# # Load API Key
# load_dotenv()
# HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# # # Define the completion wrapper using Hugging Face endpoint
# # def query_huggingface_model(prompt):
# #     return completion(
# #         model="huggingface/mistralai/Mistral-7B-Instruct-v0.3",
# #         provider="huggingface",
# #         api_key=HF_API_KEY,
# #         messages=[{"role": "user", "content": prompt}]
# #     )["choices"][0]["message"]["content"]

# TOGETHER_API_KEY = os.getenv("Together_API_KEY")  # or hardcode for local use

# # API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
# # headers = {
# #     "Authorization": f"Bearer {HF_API_KEY}"
# # }

# # def query_huggingface_model(prompt):
# #     payload = {
# #         "inputs": prompt,
# #         "parameters": {"return_full_text": False}
# #     }
# #     response = requests.post(API_URL, headers=headers, json=payload)
# #     response.raise_for_status()
# #     return response.json()[0]["generated_text"]

# # def query_llama_model(prompt: str) -> str:
# #     try:
# #         response = completion(
# #             model="huggingface/meta-llama/Llama-3.3-70B-Instruct",
# #             messages=[{"role": "user", "content": prompt}],
# #             api_base="https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct",  # 🔁 Replace with your endpoint
# #             api_key=HF_API_KEY,  # 🔁 Replace with your HF API key
# #             optional_params={
# #                 "temperature": 0.7,
# #                 "max_tokens": 300
# #             }
# #         )
# #         return response["choices"][0]["message"]["content"].strip()
# #     except Exception as e:
# #         return f"[❌ Error] {str(e)}"
    


# def query_llama_model(prompt: str) -> str:
#     try:
#         response = completion(
#             model="together_ai/meta-llama/Llama-3.3-70B-Instruct",
#             # provider="together_ai",  # ✅ This must match the lowercase provider name
#             api_key=TOGETHER_API_KEY,
#             messages=[{"role": "user", "content": prompt}],
#             optional_params={
#                 "temperature": 0.7,
#                 "max_tokens": 300
#             }
#         )
#         return response["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         return f"[❌ Error] {str(e)}"

# # Define an agent
# elderly_agent = Agent(
#     role='Elderly Assistant',
#     goal='Assist the user with elderly care support by using the provided context and query.',
#     backstory='You are an AI assistant that helps elderly users by using health records, reminders, and alerts.',
#     allow_delegation=False,
#     verbose=True,
#     llm=query_llama_model,
# )

# # Define a task
# def build_task(query, context):
#     return Task(
#         description=f"Use the context to answer the user query: '{query}'.\n\nContext:\n{context}",
#         expected_output='A helpful and context-aware response for the elderly user.',
#         agent=elderly_agent
#     )

# # Run the Crew agent
# def execute_with_context(query, context):
#     task = build_task(query, context)
#     crew = Crew(
#         agents=[elderly_agent],
#         tasks=[task],
#         verbose=True
#     )
#     results = crew.kickoff()
#     return results[0].output


from crewai import Crew, Task, Agent
import os

# from langchain_openai import ChatOpenAI

from crewai import Crew, Task, Agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",  # ✅ Or your chosen model
    api_key = os.getenv("TOGETHER_API_KEY"),          # ✅ Make sure the env var is set
    base_url="https://api.together.xyz/v1",
    temperature=0.7
) # type: ignore


# Step 1: Define Local LLM Simulator (no external model)
def local_llm_simulator(prompt: str) -> str:
    if "medication" in prompt.lower():
        return "Ensure all medications are taken on time as per reminders."
    elif "monitoring" in prompt.lower():
        return "Monitoring shows stable vitals and routine movements."
    elif "health" in prompt.lower():
        return "Health records indicate a normal trend with no critical issues."
    return "Information analyzed. No urgent issues detected."

# Step 2: Load Contexts
def load_health_data():
    with open("Dataset/health_monitoring.csv", "r") as file:
        return file.read()

def load_reminder_data():
    with open("Dataset/daily_reminder.csv", "r") as file:
        return file.read()

def load_monitoring_data():
    with open("Dataset/safety_monitoring.csv", "r") as file:
        return file.read()

# Step 3: Define Agents
health_agent = Agent(
    role="Health Monitoring Agent",
    goal="Analyze elderly health records and identify any potential issues.",
    backstory="Expert in reading and interpreting medical health logs for seniors.",
    allow_delegation=False,
    verbose=True,
    llm=local_llm_simulator
)

reminder_agent = Agent(
    role="Reminder Agent",
    goal="Ensure all daily reminders like medications and tasks are scheduled properly.",
    backstory="Manages and summarizes all important reminders for the elderly.",
    allow_delegation=False,
    verbose=True,
    llm=local_llm_simulator
)

monitoring_agent = Agent(
    role="Activity Monitoring Agent",
    goal="Interpret daily monitoring data to detect abnormal activities or behaviors.",
    backstory="Tracks and reviews movement/activity data to ensure safety.",
    allow_delegation=False,
    verbose=True,
    llm=local_llm_simulator
)

# Step 4: Define Tasks
def build_tasks(query):
    return [
        Task(
            description=f"{query} Analyze the following health info:\n{load_health_data()}",
            expected_output="Summary of any health concerns.",
            agent=health_agent
        ),
        Task(
            description=f"{query} Review the following reminders:\n{load_reminder_data()}",
            expected_output="Summary of today's important reminders.",
            agent=reminder_agent
        ),
        Task(
            description=f"{query} Evaluate the monitoring data:\n{load_monitoring_data()}",
            expected_output="Report on activity and safety alerts.",
            agent=monitoring_agent
        )
    ]

# Step 5: Run Crew
def execute_multi_agent_summary(query: str):
    tasks = build_tasks(query)
    crew = Crew(
        agents=[health_agent, reminder_agent, monitoring_agent],
        tasks=tasks,
        verbose=True
    )
    results = crew.kickoff()
    final_summary = "\n\n".join(task.output for task in results)
    return final_summary
