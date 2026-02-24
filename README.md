# 🧠 AI-Powered Interview Preparation Platform

A full-stack intelligent interview preparation system that generates personalized interview questions, evaluates answers using AI, and provides detailed feedback — built with **React**, **FastAPI**, and **Google Gemini AI**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [API Reference](#-api-reference)
- [Usage Guide](#-usage-guide)
- [Contributing](#-contributing)

---

## ✨ Features

- 📄 **Resume Parsing** — Upload your resume (PDF) and auto-extract skills, experience, and education
- 🤖 **AI Question Generation** — Generate role-specific interview questions using Google Gemini AI
- 🎤 **Voice-to-Text Answering** — Answer questions via microphone using Web Speech API
- 📝 **Smart Answer Evaluation** — AI evaluates your answers and provides structured feedback
- 📊 **Performance Analytics** — Track scores, strengths, and areas of improvement per session
- 🏢 **Company-Specific Prep** — Target preparation for specific companies and job roles
- 💬 **Real-time Chat Interface** — Conversational UI for a natural interview experience
- 🕐 **Session History** — Review past interview sessions and track progress over time

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT (React)                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  Resume  │  │Interview │  │  Voice   │  │History │  │
│  │  Upload  │  │   Chat   │  │  Input   │  │Viewer  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│                     ▲              │                     │
│              Axios / Fetch API     │ Web Speech API      │
└────────────────────────────────────────────────────────-┘
                       │
                  HTTP / REST
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  SERVER (FastAPI)                        │
│                                                         │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  /upload   │  │  /questions  │  │    /evaluate    │  │
│  │  (Resume)  │  │ (Generation) │  │   (Feedback)    │  │
│  └────────────┘  └──────────────┘  └─────────────────┘  │
│                                                         │
│  ┌────────────┐  ┌──────────────┐                       │
│  │ /sessions  │  │  PDF Parser  │                       │
│  │ (History)  │  │  (PyMuPDF)   │                       │
│  └────────────┘  └──────────────┘                       │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
┌─────────▼──────────┐   ┌─────────▼──────────┐
│   Google Gemini AI  │   │   MongoDB / JSON    │
│  (Question Gen &   │   │   (Session Store)   │
│   Answer Eval)     │   │                     │
└────────────────────┘   └────────────────────┘
```

### Component Breakdown

| Layer | Technology | Responsibility |
|---|---|---|
| **Frontend** | React 18, Tailwind CSS | UI, voice input, session display |
| **Backend** | FastAPI (Python) | REST API, business logic |
| **AI Engine** | Google Gemini 1.5 | Question generation, answer evaluation |
| **PDF Parsing** | PyMuPDF / pdfplumber | Extract resume content |
| **Storage** | JSON / MongoDB | Persist session history |
| **Auth (optional)** | JWT | User authentication |

---

## 🛠 Tech Stack

### Frontend
- **React 18** with Hooks
- **Tailwind CSS** for styling
- **Axios** for HTTP requests
- **Web Speech API** for voice input
- **React Router v6** for navigation

### Backend
- **FastAPI** (Python 3.10+)
- **Google Generative AI SDK** (`google-generativeai`)
- **PyMuPDF / pdfplumber** for PDF parsing
- **Uvicorn** as ASGI server
- **python-dotenv** for environment management
- **Pydantic** for request/response validation

---

## 📁 Project Structure

```
IIT Project/
├── frontend/                        # React application
│   ├── public/
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── ChatInterface.jsx    # Main interview chat UI
│   │   │   ├── ResumeUpload.jsx     # PDF upload component
│   │   │   ├── FeedbackCard.jsx     # Answer feedback display
│   │   │   ├── SessionHistory.jsx   # Past sessions viewer
│   │   │   └── VoiceInput.jsx       # Microphone input handler
│   │   ├── pages/                   # Route-level pages
│   │   │   ├── Home.jsx
│   │   │   ├── Interview.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js               # Axios API service layer
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                         # FastAPI application
│   ├── main.py                      # App entry point & route registration
│   ├── routes/
│   │   ├── upload.py                # Resume upload & parsing
│   │   ├── questions.py             # Question generation
│   │   ├── evaluate.py              # Answer evaluation
│   │   └── sessions.py             # Session CRUD
│   ├── services/
│   │   ├── gemini_service.py        # Google Gemini AI integration
│   │   ├── pdf_parser.py            # Resume text extraction
│   │   └── session_manager.py      # Session persistence
│   ├── models/
│   │   └── schemas.py               # Pydantic models
│   ├── data/                        # JSON session storage
│   ├── requirements.txt
│   └── .env                         # Environment variables (never commit)
│
└── README.md
```

---

## ✅ Prerequisites

Ensure the following are installed on your system:

- **Node.js** v18+ and **npm** v9+ → [Download](https://nodejs.org/)
- **Python** 3.10+ → [Download](https://python.org/)
- **pip** (comes with Python)
- **Google Gemini API Key** → [Get it here](https://makersuite.google.com/app/apikey)
- *(Optional)* **MongoDB** if using database storage

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/iit-interview-prep.git
cd "IIT Project"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

---

## 🔐 Environment Variables

### Backend — `backend/.env`

Create a `.env` file inside the `backend/` directory:

```env
# Google Gemini AI
GEMINI_API_KEY=your_google_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Storage (use 'json' for file-based or 'mongodb' for database)
STORAGE_TYPE=json

# MongoDB (only if STORAGE_TYPE=mongodb)
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=interview_prep
```

### Frontend — `frontend/.env`

Create a `.env` file inside the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

> ⚠️ **Never commit `.env` files to version control.** Add them to `.gitignore`.

---

## ▶️ Running the Application

### Start the Backend Server

```bash
cd backend

# Activate virtual environment (if not already active)
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Run the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

### Start the Frontend Dev Server

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

---

## 📡 API Reference

### Base URL: `http://localhost:8000`

#### 📤 Resume Upload
```
POST /upload
Content-Type: multipart/form-data

Body: file (PDF)

Response: {
  "filename": "resume.pdf",
  "extracted_text": "...",
  "skills": [...],
  "experience": [...],
  "education": [...]
}
```

#### ❓ Generate Questions
```
POST /questions/generate
Content-Type: application/json

Body: {
  "role": "Software Engineer",
  "company": "Google",
  "resume_text": "...",
  "difficulty": "medium",
  "count": 5
}

Response: {
  "questions": [...],
  "session_id": "uuid"
}
```

#### ✅ Evaluate Answer
```
POST /evaluate
Content-Type: application/json

Body: {
  "question": "...",
  "answer": "...",
  "role": "Software Engineer",
  "session_id": "uuid"
}

Response: {
  "score": 8.5,
  "feedback": "...",
  "strengths": [...],
  "improvements": [...],
  "ideal_answer_hints": "..."
}
```

#### 📚 Get Session History
```
GET /sessions

Response: {
  "sessions": [
    {
      "session_id": "uuid",
      "date": "2024-01-15",
      "role": "Software Engineer",
      "company": "Google",
      "average_score": 7.8,
      "questions_answered": 5
    }
  ]
}
```

#### 🔍 Get Session Details
```
GET /sessions/{session_id}

Response: {
  "session_id": "uuid",
  "questions": [...],
  "answers": [...],
  "scores": [...],
  "feedback": [...]
}
```

---

## 📖 Usage Guide

### Step 1 — Upload Your Resume
1. Navigate to the home page
2. Click **Upload Resume** and select your PDF
3. The system will parse your skills, experience, and education

### Step 2 — Configure Your Interview
1. Enter the **Job Role** (e.g., "Backend Engineer")
2. Enter the **Target Company** (e.g., "Amazon")
3. Select **Difficulty Level** (Easy / Medium / Hard)
4. Choose the **number of questions**

### Step 3 — Start the Interview
1. Click **Start Interview**
2. Read each question carefully
3. Click the 🎤 **microphone button** to answer via voice, or type your answer
4. Submit your answer to receive AI feedback

### Step 4 — Review Feedback
- View your **score** (out of 10) for each answer
- Read **strengths** and **areas for improvement**
- Get hints on the **ideal answer**

### Step 5 — Track Progress
- Navigate to **Dashboard** to view session history
- Compare scores across sessions
- Identify weak areas and focus your preparation

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| `GEMINI_API_KEY not found` | Ensure `.env` is in `backend/` and the key is correct |
| CORS errors in browser | Check `ALLOWED_ORIGINS` in backend `.env` matches your frontend URL |
| PDF not parsing correctly | Ensure the PDF is text-based (not scanned/image-only) |
| Voice input not working | Use **Google Chrome** — Web Speech API has limited browser support |
| `Module not found` errors | Re-run `pip install -r requirements.txt` with venv activated |
| Port already in use | Change the port with `--port 8001` in the uvicorn command |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is developed as part of an **IIT academic project**. All rights reserved.

---

## 👥 Authors

- **Team IIT** — *Initial development*

---

> 💡 **Tip:** For the best experience, use **Google Chrome** for voice input features and ensure your microphone permissions are enabled.
