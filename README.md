# Matchify-AI-Resume-Screening-System
AI Resume Screening System: An intelligent hiring tool that uses NLP and Large Language Models to automatically parse resumes, extract skills, and rank candidates against a job description with detailed insights on strengths, weaknesses, and improvement suggestions.

👨‍💻 Author

Muhammad Arham Kakar

Embedded System | IoT | AI & AUTOMATION

📧 muhammadarhamkakar27@gmail.com

# Github | LinkedIn

# 🚀 Tech Stack

Backend: FastAPI

Frontend: Streamlit

NLP & Embeddings: Sentence Transformers (all-MiniLM-L6-v2)

Similarity: Cosine Similarity

LLM: Llama3-70B via Huggingface API

PDF Parsing: PyMuPDF

Language: Python 3.12

# 📌 Problem Statement

Traditional resume screening is:

⏳ Time-consuming

❌ Keyword-based and inaccurate

⚠️ Biased and inefficient

🔍 Unable to capture semantic meaning

This system solves these problems using semantic search + LLM analysis, enabling intelligent and fair candidate evaluation.

🎯 Key Features

📄 Upload resume (PDF)

🧠 Semantic job matching (not keyword-based)

📊 Match score (0–100%) with color coding

🤖 AI-powered resume analysis

💡 Skill extraction & strengths detection

🎯 Suggested job roles

⚠️ Improvement recommendations

🎤 Interview tips

⭐ Candidate rating (out of 100)

# 🏗️ System Architecture

User (Browser - Streamlit)

        ↓
Frontend (Streamlit)

        ↓
FastAPI Backend

        ↓
1. PDF Extraction ( PyMuPDF)

2. NLP Preprocessing

3. Sentence Embeddings

4. Cosine Similarity Matching

5. LLM Analysis (Groq - Llama3-70B)
        ↓
JSON Response
        ↓
Frontend Display

# 📁 Project Structure

ai-resume-system/

│

├── backend/

│   ├── main.py

│   ├── utils.py

│   └── llm.py

│
├── frontend/

│   └── app.py
│
└── requirements.txt

# ⚙️ How It Works
1. PDF Upload

2. Extracts text using  PyMuPDF.

3. Text Preprocessing

4. Cleans and normalizes text.

5. Semantic Embeddings

6. Uses all-MiniLM-L6-v2 to create vectors.

7. Similarity Matching

8. Uses cosine similarity to compare resume vs job description.

LLM Analysis

Uses Llama3-70B via Groq API to generate:

. Skills

. Strengths

. Job roles

. Improvements

. Interview tips

. Rating

# 📦 Installation

git clone https://github.com/tuahazaheen/ai-resume-screening-system.git

cd ai-resume-screening-system

pip install fastapi uvicorn streamlit  PyMuPDF sentence-transformers scikit-learn numpy groq requests

# ▶️ Run the Project

Start Backend

cd backend
uvicorn main:app --reload

Start Frontend

cd frontend
streamlit run app.py

Example Results

<img width="964" height="663" alt="Screenshot 2026-04-06 164800" src="https://github.com/user-attachments/assets/e1b32b3d-6929-4f82-a530-03291759fb99" />

# 🌟 Why This Project is Unique

. 🧠 Semantic AI Matching

. ⚡ LLM-powered analysis

. 💸 Fully free & open source

. 🏗️ Production-ready architecture

. 🔌 Easily extensible

# 📈 Future Enhancements

. Multi-resume ranking

. ATS scoring

. Skill gap detection


. Database integration

. Azure OpenAI deployment

. Chrome extension

. Email reports
