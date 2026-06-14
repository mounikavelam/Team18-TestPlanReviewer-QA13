AI Test Plan Review Platform

Project Overview

AI Test Plan Review Platform is an intelligent web-based application that automates the review of software test plans using Generative AI. The system evaluates uploaded test plans against predefined quality rubrics and provides detailed feedback, scoring, strengths, weaknesses, and improvement suggestions.

The platform helps QA teams, testers, and project managers improve the quality and completeness of test plans while reducing manual review effort.

---

Problem Statement

Manual review of software test plans is time-consuming, inconsistent, and dependent on reviewer expertise. Organizations require a faster and more standardized approach to evaluate test plans and ensure compliance with quality standards.

---

Solution

The AI Test Plan Review Platform uses Google's Gemini AI model to analyze uploaded test plans and generate rubric-based evaluations. The system automatically identifies strengths, gaps, risks, and recommendations, helping teams improve test planning quality.

---

Key Features

- Upload test plan documents
- AI-powered test plan analysis
- Rubric-based scoring system
- Strength and weakness identification
- Actionable improvement recommendations
- Review history management
- Report generation and export
- User-friendly web interface

---

Technology Stack

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- Flask

Database

- SQLite

AI Integration

- Google Gemini API

Report Generation

- Python-docx

---

Demo Video

The project demonstration video is available in:

demo/DEMO_VIDEO_LINK.txt

---

Project Workflow

1. User uploads a test plan.
2. System validates the uploaded file.
3. Gemini AI analyzes the test plan.
4. Rubric-based evaluation is performed.
5. Score and feedback are generated.
6. User views results and exports reports.

---

Installation & Setup

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

Open browser:

http://127.0.0.1:5000

---

Project Structure

project/
│
├── app.py
├── requirements.txt
├── README.md
├── TEST_CASES.md
├── AI_USAGE_NOTE.md
│
├── resumes/
│
├── demo/
│   └── DEMO_VIDEO_LINK.txt
│
├── templates/
├── static/
├── docs/
├── sample_data/
└── uploads/

---

Test Cases

The project includes test cases covering:

- Valid file upload
- Invalid file upload
- AI review generation
- Report export
- Error handling
- Database operations

---

Team Resumes

All team member resumes are available in the "resumes/" folder in PDF format.

---

Future Enhancements

- Multi-format document support
- User authentication
- Dashboard analytics
- Team collaboration features
- Cloud deployment
- Advanced QA metrics

---

Team Members

S.No| Team Member Name
1| VELLAM MOUNIKA
2| VALLU VENKATALAKSHMI
3| KONETI TEJA VENKATA ABHISHEK
4| KURAMDASU SOWJANYA

---

License

This project was developed for academic and placement assessment purposes.