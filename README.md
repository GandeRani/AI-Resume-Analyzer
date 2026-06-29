# 🚀 AI Resume Analyzer (Flask + ATS System)

An AI-powered Resume Analyzer web application built using Flask that extracts text from PDF resumes, detects skills, calculates ATS score, and predicts job roles.

---

## 📌 Features

- 📄 Upload PDF Resume  
- 🤖 Extract text automatically from resume  
- 🧠 Skill detection using keyword matching  
- 📊 ATS Resume Score (0–100)  
- 🎯 Job Role Prediction:
  - VLSI / Digital Design Engineer  
  - AI / Data Science Engineer  
  - Embedded Systems Engineer  
  - General Profile  

- 📈 Score Breakdown:
  - Skills (40)
  - Projects (25)
  - Education (15)
  - Keywords (20)

- 🎨 Clean Bootstrap UI  
- ⚡ Flask Backend  

---

## 🛠 Tech Stack

- Python 🐍  
- Flask 🌐  
- PyPDF2 📄  
- HTML5  
- CSS3  
- Bootstrap 5  
- Regex (Text Processing)  

---

## 🧠 How It Works

1. User uploads a PDF resume  
2. Flask saves file securely  
3. PyPDF2 extracts text  
4. Text is cleaned and processed  
5. Skills are detected using keywords  
6. Resume is evaluated using scoring system  
7. ATS score is generated  
8. Job role is predicted  
9. Result is displayed in UI  

---

## 📊 ATS Scoring System

| Component | Marks |
|----------|------|
| Skills   | 40   |
| Projects | 25   |
| Education| 15   |
| Keywords | 20   |

**Total = 100**

---
## 📁 Project Structure

```bash
AI-Resume-Analyzer/
│
├── app.py
├── README.md
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   └── result.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       ├── home.png
│       ├── upload.png
│       └── result.png
│
└── uploads/
```

---


## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Flask app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

## 🏠 Home Page
![Home](./static/images/screenshots/home.png)

## 📄 Upload Page
![Upload](./static/images/screenshots/upload.png)

## 📊 Result Page
![Result](./static/images/screenshots/result.png)

## 👨‍💻 Author

- **Name:** Gande Rani  
- **Project:** AI Resume Analyzer  
- **Tech Stack:** Flask + AI Web Application  
