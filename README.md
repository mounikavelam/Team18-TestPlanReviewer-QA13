🚀 TestLens – Intelligent Test Plan Review Platform

Team 18 | QA-13 – Test Plan Reviewer

AI-powered rubric-based Test Plan Review Platform using Google Gemini AI

---
🌐 Live Deployment

Live Application: https://testlens-ai.onrender.com

The application is successfully deployed on Render and can be accessed through the above URL.

Quick Access

- Web App: https://testlens-ai.onrender.com
- Platform: Render
- AI Engine: Google Gemini 2.5 Flash
📌 Project Overview

---

TestLens is an intelligent web-based application that automates the review of software test plans using Generative AI.

The platform evaluates uploaded test plans against predefined QA rubrics and generates:

- Quality Scores
- Coverage Analysis
- Strengths & Weaknesses
- Risk Assessment
- Improvement Suggestions
- Review Reports

This helps QA teams reduce manual review effort while improving test plan quality and consistency.

---

🎯 Problem Statement

Manual test plan reviews are:

- Time-consuming
- Reviewer-dependent
- Inconsistent across teams
- Difficult to standardize

Organizations need a faster and more reliable way to assess test plans and ensure quality compliance.

---

💡 Solution

TestLens leverages Google Gemini AI to automatically analyze software test plans and provide rubric-based evaluations.

The system identifies:

- Missing test scenarios
- Coverage gaps
- Potential risks
- Quality issues
- Improvement recommendations

---

✨ Key Features

✅ Upload Test Plan Documents

✅ AI-Powered Test Plan Analysis

✅ Rubric-Based Quality Scoring

✅ Strength & Weakness Identification

✅ Coverage Assessment

✅ Risk Detection

✅ Improvement Recommendations

✅ Report Export

✅ Review History Management

---

🛠 Technology Stack

Layer| Technology
Frontend| HTML5, CSS3, JavaScript
Backend| Python, Flask
Database| SQLite
AI Model| Google Gemini AI
Report Generation| Python-docx

---

🎥 Demo Video

The project demonstration video link is available in:

demo/DEMO_VIDEO_LINK.txt

---

🔄 Project Workflow

1. User uploads a test plan.
2. System validates the uploaded document.
3. Gemini AI analyzes the content.
4. Rubric-based evaluation is performed.
5. Quality scores and feedback are generated.
6. User reviews results.
7. Reports can be exported for future reference.

---

⚙️ Installation & Setup

Clone Repository

git clone <repository-url>
cd project-folder

Install Dependencies

pip install -r requirements.txt

Configure Environment Variables

Create a ".env" file:

GEMINI_API_KEY=YOUR_API_KEY

Run Application

python app.py

Open the application in your browser:

http://127.0.0.1:5000

«Note: This URL works only on the local machine where the application is running.»

---

## 📁 Project Structure

```text
Team18-TestPlanReviewer-QA13/
│
├── app.py
├── report_export.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
│   ├── AI_USAGE_NOTE.md
│   ├── TEST_CASES.md
│   └── Team18-TEST PLAN REVIEWER.pdf
│
├── resumes/
│   ├── Mounika_Resume.pdf
│   ├── VALLU_VENKATALAKSHMI.pdf
│   ├── K_TEJA_CV.pdf
│   └── 24u45a0227_Resume.pdf
│
├── demo/
│   └── DEMO_VIDEO_LINK.txt
│
├── sample_data/
│   └── sample_test_plan.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── uploads/
```
---

🧪 Test Cases Covered

- Valid File Upload
- Invalid File Upload
- AI Review Generation
- Report Export
- Error Handling
- Database Operations

---

📄 Documentation

Project documentation is available in the "docs/" directory.

Contents include:

- AI Usage Note
- Test Cases
- Project Documentation

---

## 👨‍💻 Team Members

| S.No | Team Member |
|------|-------------|
| 1 | VELLAM MOUNIKA |
| 2 | VALLU VENKATALAKSHMI |
| 3 | KONETI TEJA VENKATA ABHISHEK |
| 4 | KURAMDASU SOWJANYA |

---

📑 Team Resumes

All team member resumes are available in the "resumes/" folder in PDF format.

---

🔮 Future Enhancements

- Multi-format document support
- User Authentication
- Dashboard Analytics
- Team Collaboration Features
- Cloud Deployment
- Advanced QA Metrics

---

📜 License

This project was developed for academic and placement assessment purposes.