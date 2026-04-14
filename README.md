# 🧠 Khotwa – Micro-Progress AI Agent (Atomic Tasks)

An AI-powered autonomous agent that helps users overcome procrastination by breaking complex tasks into ultra-small, actionable steps.

---

## 🚀 Project Description

Khotwa is an intelligent AI agent designed to:
- Understand user messages
- Detect blocking situations (stress, confusion, overload)
- Generate micro-actions that are impossible to refuse
- Adapt dynamically based on user feedback ("done" / "too hard")

Instead of giving long advice, the agent focuses on **one tiny actionable step at a time**.

---

## 💡 Key Features

- 🧠 AI-based task analysis (Gemini API)
- ⚡ Micro-task generation (Atomic Tasks)
- 🔁 Adaptive difficulty system
- 💬 Feedback loop ("Done" / "Too hard")
- 🧩 Modular agent architecture
- 🌐 Simple web interface (HTML + JS)

---

## 🏗️ Project Structure
project/
│
├── backend/
│ ├── agent.py
│ ├── gemini_service.py
│
├── frontend/
│ ├── index.html
│ ├── script.js
│ ├── style.css
│
├── requirements.txt
├── README.md
## ⚙️ Installation

### 1️⃣ Install Python
Make sure you have Python 3.9+

Check:  python --version 
### 2️⃣ Install dependencies
pip install google-generativeai python-dotenv
### 3️⃣ Add your API key
Create a .env file:
GEMINI_API_KEY=YOUR_API_KEY_HERE
--> Get your API key here:
https://aistudio.google.com/


▶️ How to Run the Project
1️⃣ Start the backend
cd backend
python agent.py
2️⃣ Open the frontend
You have 2 options:
Open frontend/index.html
