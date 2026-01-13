# 🚨 CodeSentinel AI

**AI-Powered Code Smell Detection & Refactoring Assistant**

CodeSentinel AI is a smart developer assistant that analyzes your code to detect code smells, suggest improvements, explain complexity, and support multi-turn follow-up queries. It uses **AST analysis + Machine Learning + LLMs** to provide accurate insights.

---

## 🌐 Live Demo

### 🔹 Frontend (Streamlit)

👉 [https://codesentinel.streamlit.app/](https://codesentinel.streamlit.app/)

### 🔹 Backend (FastAPI)

👉 [https://codesentinel-ai.onrender.com/](https://codesentinel-ai.onrender.com/)

---

## ✨ Features

✔ Upload code files for analysis
✔ Detect common code smells
✔ Time & Space complexity explanation
✔ AI-based refactoring suggestions
✔ Multi-turn follow-up chat
✔ Download full discussion as PDF
✔ Hybrid AST + ML based analysis
✔ Clean UI with Streamlit

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* Python
* OpenRouter LLM API
* AST Parser
* Machine Learning model
* ReportLab (PDF generation)

### Frontend

* Streamlit
* Python
* REST API integration

### Deployment

* Backend → Render
* Frontend → Streamlit Cloud

---

## 🧠 How It Works

1. User uploads code file
2. Backend parses code using AST
3. ML model detects smells
4. LLM explains issues & improvements
5. User asks follow-up questions
6. Chat history stored per session
7. Discussion can be downloaded as PDF

---

**🧠 Architecture**

User
  │
  ▼
Streamlit UI
  │
  ▼
FastAPI Backend
  ├── AST Analyzer
  ├── ML Model
  └── LLM Engine

---

## 🚀 API Endpoints

### 🔹 Analyze Code

```
POST /analyze
```

**Form-data**

* user_query
* file

### 🔹 Follow-up Query

```
POST /followup
```

**Form-data**

* user_query
* session_id

### 🔹 Download Discussion

```
POST /download-pdf
```

**JSON**

```json
{
  "text": "full conversation"
}
```

---

## 📁 Project Structure

```
code-smell-agent/
│
├── backend/
│   ├── main.py
│   ├── agent_logic.py
│   ├── ast_analyzer.py
│   ├── session_store.py
│   ├── model/
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── utils.py
│
└── README.md
```

---

## ⚙️ Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 🔐 Environment Variables

Create `.env` file in backend:

```
OPENROUTER_API_KEY=your_api_key
OPENROUTER_MODEL=xiaomi/mimo-v2-flash
```

---

## 📄 PDF Export Feature

Users can download their complete conversation as a **PDF file** using the "Download Discussion" button.

---

## 🎯 Use Cases

* Code reviews
* Interview preparation
* Learning clean coding practices
* Academic projects
* Refactoring legacy code

---

## 🧑‍💻 Author

**Saurabh Yadav**
B.Tech Student | AI & Backend Developer

---

## ⭐ Future Enhancements

* GitHub repo analysis
* Code auto-fix feature
* More ML models
* User authentication
* History dashboard

---

## 📜 License

This project is licensed under MIT License.

---


Just say 😎
