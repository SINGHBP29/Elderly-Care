# Elderly-Care

---

## 🧠 Elderly AI Assistant

> A smart, voice-enabled health monitoring and reminder system designed to empower elderly individuals with proactive care and real-time safety alerts.

---
![image](https://github.com/user-attachments/assets/eaa7b6c7-0300-43ea-8d66-f17ee1936374) -->
![image](https://github.com/user-attachments/assets/137a9302-b3f4-4e2c-a5ae-9a4ad8d4aaf2)

![image](https://github.com/user-attachments/assets/0c05f1aa-7a17-4e8a-9bba-e26af15f3308)




---

## 🩺 Problem Statement

Elderly individuals often face:

- ❌ Forgetfulness (e.g., missing medication or appointments)
- ❌ Lack of immediate assistance during emergencies or falls
- ❌ Isolation without emotional support or daily check-ins
- ❌ Complex or expensive monitoring systems

---

## 🌟 Our Solution

An easy-to-use **AI-powered assistant** that:

- ✅ Responds to voice or text
- ✅ Provides emotional support and smart summaries
- ✅ Detects inactivity and fall patterns (via dataset simulation)
- ✅ Sends real-time alerts to caregivers
- ✅ Displays health, reminders, and safety data in tables
- ✅ Uses multi-agent LLMs to generate contextual responses

---

## 🔍 Key Features

| Feature                          | Description |
|----------------------------------|-------------|
| 🗣️ **Voice Support**             | Speech recognition + text-to-speech |
| ⏰ **Smart Reminders**           | Medication, appointments, exercise |
| 📊 **Health Monitoring**        | Live status from dataset or user input |
| 🛡️ **Safety Alerts**           | Fall detection, inactivity alerts |
| 🧠 **Multi-Agent LLM AI**       | Context-aware responses using CrewAI |
| 🔎 **Semantic Search (FAISS)**  | Match user queries to past logs or notes |
| 👵 **Elder-Friendly Interface** | Clean UI with large buttons and voice |

---

## 🛠 Tech Stack

| Technology        | Purpose                            |
|-------------------|-------------------------------------|
| Python            | Core backend logic                  |
| Streamlit         | Interactive web UI                  |
| FAISS             | Fast semantic vector search         |
| SentenceTransformer | Embedding user and stored inputs |
| CrewAI + LLMs     | Multi-agent AI reasoning            |
| HuggingFace/Together | LLM APIs for response generation |
| SpeechRecognition | Voice input                         |
| pyttsx3           | Voice output                        |
| Pandas / NumPy    | Health/reminder data handling       |

---

## 📁 Folder Structure

```
Elderly_AI_Assistant/
├── main.py                        # Entry point with user selection
├── pages/
│   ├── elder_dashboard (1).py     # Elder interface
│   └── caretaker_dashboard.py     # Caretaker dashboard
├── backend/
│   ├── ai_service.py              # Reminder, health, safety services
│   └── user_service.py            # Query dispatcher
├── ai_agents.py                   # CrewAI-based agent logic
├── data/
│   ├── health_data.csv
│   ├── reminder_data.csv
│   ├── monitoring_data.csv
├── requirements.txt
├── README.md
```

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/your-repo/elderly-care-assistant.git
cd elderly-care-assistant

python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
streamlit run main.py
```

---

## 🧠 AI Capabilities

- Natural conversations powered by LLMs (LLaMA 3.3, Mistral, etc.)
- Contextual awareness via vector matching (FAISS + SentenceTransformer)
- CrewAI multi-agent response coordination for:
  - Emotional support
  - Safety monitoring
  - Reminder management

**Example Queries:**
- “Did I take my medicine today?”
- “How is my health?”
- “Was there a fall this week?”
- “Tell me about my activities yesterday.”

---

## 🎯 Use Case Scenarios

- 👵 *"Remind grandma to take her pills at 10 AM."*
- 🛠 *"Alert the caregiver if an elder falls in the kitchen."*
- 📈 *"Monitor heart rate and movement patterns."*
- 💬 *"Chat with an AI that understands how I feel."*

---

## 🏆 Achievements

- ✅ Real-time voice interaction
- ✅ Elder-centric usability
- ✅ Smart AI summaries with CrewAI agents
- ✅ FAISS-powered query recall
- ✅ Safety & health alerts integrated

---



## 🙌 Special Thanks

- HuggingFace Inference API
- Streamlit Community
- CrewAI Open Source Devs

---


### Demo Video
  [video](https://youtu.be/gAc2lLf4XGI)

### Contributor
  [Nikita Verma](https://github.com/Nikitav0608)

### 📜 License

This project is under the MIT License. Feel free to use or improve!

