# Matchify-AI-Resume-Screening-System

> An AI-powered full-stack recruitment platform that uses NLP, semantic embeddings, and LLMs to intelligently match resumes with job descriptions and provide deep candidate insights.

---

## 👨‍💻 Author

**Muhammad Arham Kakar**  
Embedded | IoT AI & Automation |   
📧 muhammadarhamkakar27@gmail.com 
🔗 [GitHub](https://github.com/ArhamKakar) | [LinkedIn](https://www.linkedin.com/in/muhammad-arham-kakar-6b2318352/)

---

## 🚀 Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **NLP & Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Similarity:** Cosine Similarity  
- **LLM:** Llama3-70B via Huggingface API  
- **PDF Parsing:**  PyMuPDF 
- **Language:** Python 3.12  

---

## 📌 Problem Statement

Traditional resume screening is:

- ⏳ Time-consuming  
- ❌ Keyword-based and inaccurate  
- ⚠️ Biased and inefficient  
- 🔍 Unable to capture semantic meaning  

This system solves these problems using **semantic search + LLM analysis**, enabling intelligent and fair candidate evaluation.

---

## 🎯 Key Features

- 📄 Upload resume (PDF)
- 🧠 Semantic job matching (not keyword-based)
- 📊 Match score (0–100%) with color coding
- 🤖 AI-powered resume analysis
- 💡 Skill extraction & strengths detection
- 🎯 Suggested job roles
- ⚠️ Improvement recommendations
- 🎤 Interview tips
- ⭐ Candidate rating (out of 10)

---

## 🏗️ System Architecture

```
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
```

---

## 📁 Project Structure

```
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
```

---

## ⚙️ How It Works

1. **PDF Upload**  
   Extracts text using ` PyMuPDF`.

2. **Text Preprocessing**  
   Cleans and normalizes text.

3. **Semantic Embeddings**  
   Uses `all-MiniLM-L6-v2` to create vectors.

4. **Similarity Matching**  
   Uses cosine similarity to compare resume vs job description.

5. **LLM Analysis**  
   Uses Llama3-70B via Groq API to generate:
   - Skills
   - Strengths
   - Job roles
   - Improvements
   - Interview tips
   - Rating

---

## 📦 Installation

```bash
git clone https://github.com/ArhamKakar/RecuriterIQ-AI-Resume-Screening-System
cd ai-resume-screening-system
```

```bash
pip install fastapi uvicorn streamlit pdfplumber sentence-transformers scikit-learn numpy groq requests
```

---

## ▶️ Run the Project

### Start Backend

```bash
cd backend
uvicorn main:app --reload
```

### Start Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 🧪 Example Results

| Job Role | Match Score | Result |
|----------|-----------|--------|
| AI Engineer | 64.65% | Moderate |
| Mobile Developer | 23.71% | Weak |
| Software Engineer | 31.32% | Weak |

---

## 🌟 Why This Project is Unique

- 🧠 Semantic AI Matching  
- ⚡ LLM-powered analysis  
- 💸 Fully free & open source  
- 🏗️ Production-ready architecture  
- 🔌 Easily extensible  

---

## 📈 Future Enhancements

- Multi-resume ranking  
- ATS scoring  
- Skill gap detection  
- Database integration  
- Azure OpenAI deployment  
- Chrome extension  
- Email reports  

---
