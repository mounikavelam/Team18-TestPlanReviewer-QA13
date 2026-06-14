from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file
)

from docx import Document

from dotenv import load_dotenv

import google.generativeai as genai

import sqlite3
import json
import os
import uuid

from datetime import datetime

from report_export import (
    generate_pdf_report,
    generate_docx_report
)

# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

app = Flask(__name__)

# ==========================================
# GEMINI CONFIGURATION
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# DATABASE
# ==========================================

DATABASE = "reviews.db"

# ==========================================
# QA RUBRIC
# ==========================================

RUBRIC = [
    "Functional Coverage",
    "Boundary Conditions",
    "Negative Test Cases",
    "Risk Areas",
    "Test Data Coverage",
    "Performance Considerations",
    "Security Considerations",
    "Clarity and Completeness"
]

# ==========================================
# DATABASE FUNCTIONS
# ==========================================

def get_db():

    conn = sqlite3.connect(
        DATABASE
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS reviews(

        id TEXT PRIMARY KEY,

        filename TEXT,

        score INTEGER,

        coverage INTEGER,

        risk_level TEXT,

        review_json TEXT,

        created_at TEXT

    )
    """
    )

    conn.commit()

    conn.close()


init_db()

# ==========================================
# FILE READER
# ==========================================

def read_uploaded_file(
        uploaded_file
):

    text = ""

    if uploaded_file.filename.endswith(
        ".txt"
    ):

        text = uploaded_file.read().decode(
            "utf-8"
        )

    elif uploaded_file.filename.endswith(
        ".md"
    ):

        text = uploaded_file.read().decode(
            "utf-8"
        )

    elif uploaded_file.filename.endswith(
        ".docx"
    ):

        doc = Document(
            uploaded_file
        )

        for para in doc.paragraphs:

            text += (
                para.text + "\n"
            )

    return text

# ==========================================
# JSON CLEANER
# ==========================================

def clean_json_response(
        text
):

    text = text.strip()

    if text.startswith(
        "```json"
    ):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

    elif text.startswith(
        "```"
    ):

        text = text.replace(
            "```",
            ""
        )

    return text.strip()

# ==========================================
# GEMINI REVIEW
# ==========================================

def generate_review(test_plan):

    prompt = f"""

You are a Senior QA Architect.

Analyze the following Test Plan.

IMPORTANT:

- Return ONLY valid JSON.
- Do NOT return markdown.
- Do NOT return explanations.
- Every score must be between 0 and 10.
- Never return scores above 10.

Return EXACTLY in this format:

{{
"scores": {{
"Functional Coverage": 0,
"Boundary Conditions": 0,
"Negative Test Cases": 0,
"Risk Areas": 0,
"Test Data Coverage": 0,
"Performance Considerations": 0,
"Security Considerations": 0,
"Clarity and Completeness": 0
}},
"missing_scenarios": [],
"coverage_gaps": [],
"risks": [],
"suggestions": [],
"improved_test_plan": ""
}}

Rubric:

{json.dumps(RUBRIC, indent=2)}

Test Plan:

{test_plan}
"""

    try:

        response = model.generate_content(prompt)

        print("\n===== GEMINI RESPONSE =====")
        print(response.text)
        print("===========================\n")

        response_text = clean_json_response(
            response.text
        )

        data = json.loads(
            response_text
        )

        scores = data.get(
            "scores",
            {}
        )

        fixed_scores = {}

        total_score = 0

        for category in RUBRIC:

            value = scores.get(
                category,
                0
            )

            try:
                value = int(value)
            except:
                value = 0

            if value > 10:

                if value <= 100:
                    value = round(
                        value / 10
                    )
                else:
                    value = 10

            value = max(
                0,
                min(value, 10)
            )

            fixed_scores[
                category
            ] = value

            total_score += value

        data["scores"] = fixed_scores

        data["overall_score"] = (
            total_score
        )

        data["coverage_percentage"] = round(
            (total_score / 80) * 100
        )

        if total_score >= 60:
            risk = "Low"

        elif total_score >= 40:
            risk = "Medium"

        else:
            risk = "High"

        data["risk_level"] = risk

        if "missing_scenarios" not in data:
            data["missing_scenarios"] = []

        if "coverage_gaps" not in data:
            data["coverage_gaps"] = []

        if "risks" not in data:
            data["risks"] = []

        if "suggestions" not in data:
            data["suggestions"] = []

        if "improved_test_plan" not in data:
            data["improved_test_plan"] = ""

        return data

    except Exception as e:

        print("ERROR:", str(e))

        return {

            "scores": {
                category: 0
                for category in RUBRIC
            },

            "overall_score": 0,

            "coverage_percentage": 0,

            "risk_level": "Error",

            "missing_scenarios": [],

            "coverage_gaps": [],

            "risks": [],

            "suggestions": [
                str(e)
            ],

            "improved_test_plan":
            "Unable to generate."
        }


# ==========================================
# SAVE REVIEW
# ==========================================

def save_review(
        filename,
        review_data
):

    conn = get_db()

    review_id = str(
        uuid.uuid4()
    )

    conn.execute(
    """
    INSERT INTO reviews
    (
        id,
        filename,
        score,
        coverage,
        risk_level,
        review_json,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        review_id,
        filename,
        review_data.get(
            "overall_score",
            0
        ),
        review_data.get(
            "coverage_percentage",
            0
        ),
        review_data.get(
            "risk_level",
            "Low"
        ),
        json.dumps(
            review_data
        ),
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    )

    conn.commit()

    conn.close()

    return review_id

# ==========================================
# REVIEW HISTORY
# ==========================================

@app.route(
    "/api/reviews"
)
def review_history():

    conn = get_db()

    rows = conn.execute(
    """
    SELECT *
    FROM reviews
    ORDER BY created_at DESC
    """
    ).fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({

            "id":
            row["id"],

            "filename":
            row["filename"],

            "score":
            row["score"],

            "coverage":
            row["coverage"],

            "risk_level":
            row["risk_level"],

            "created_at":
            row["created_at"]

        })

    return jsonify(
        data
    )

# ==========================================
# REVIEW DETAILS
# ==========================================

@app.route(
    "/api/review/<review_id>"
)
def review_details(
        review_id
):

    conn = get_db()

    row = conn.execute(
    """
    SELECT *
    FROM reviews
    WHERE id = ?
    """,
    (review_id,)
    ).fetchone()

    conn.close()

    if not row:

        return jsonify({
            "error":
            "Review Not Found"
        }), 404

    return jsonify(
        json.loads(
            row["review_json"]
        )
    )

# ==========================================
# DASHBOARD API
# ==========================================

@app.route(
    "/api/dashboard"
)
def dashboard():

    conn = get_db()

    rows = conn.execute(
    """
    SELECT *
    FROM reviews
    """
    ).fetchall()

    conn.close()

    if len(rows) == 0:

        return jsonify({

            "total_reviews":
            0,

            "average_score":
            0,

            "average_coverage":
            0

        })

    total_score = sum(
        row["score"]
        for row in rows
    )

    total_coverage = sum(
        row["coverage"]
        for row in rows
    )

    return jsonify({

        "total_reviews":
        len(rows),

        "average_score":
        round(
            total_score /
            len(rows),
            2
        ),

        "average_coverage":
        round(
            total_coverage /
            len(rows),
            2
        )

    })

# ==========================================
# PDF EXPORT
# ==========================================

@app.route(
    "/export/pdf/<review_id>"
)
def export_pdf(
        review_id
):

    conn = get_db()

    row = conn.execute(
    """
    SELECT *
    FROM reviews
    WHERE id = ?
    """,
    (review_id,)
    ).fetchone()

    conn.close()

    if not row:

        return (
            "Review Not Found",
            404
        )

    review_data = json.loads(
        row["review_json"]
    )

    os.makedirs(
        "exports",
        exist_ok=True
    )

    pdf_path = (
        f"exports/"
        f"{review_id}.pdf"
    )

    generate_pdf_report(
        review_data,
        pdf_path
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )

# ==========================================
# DOCX EXPORT
# ==========================================

@app.route(
    "/export/docx/<review_id>"
)
def export_docx(
        review_id
):

    conn = get_db()

    row = conn.execute(
    """
    SELECT *
    FROM reviews
    WHERE id = ?
    """,
    (review_id,)
    ).fetchone()

    conn.close()

    if not row:

        return (
            "Review Not Found",
            404
        )

    review_data = json.loads(
        row["review_json"]
    )

    os.makedirs(
        "exports",
        exist_ok=True
    )

    docx_path = (
        f"exports/"
        f"{review_id}.docx"
    )

    generate_docx_report(
        review_data,
        docx_path
    )

    return send_file(
        docx_path,
        as_attachment=True
    )

# ==========================================
# HOME PAGE
# ==========================================

@app.route(
    "/",
    methods=[
        "GET",
        "POST"
    ]
)
def index():

    result = None

    if request.method == "POST":

        text = request.form.get(
            "test_plan",
            ""
        )

        uploaded_file = request.files.get(
            "test_file"
        )

        filename = (
            "Pasted Test Plan"
        )

        if (
            uploaded_file
            and
            uploaded_file.filename
        ):

            filename = (
                uploaded_file.filename
            )

            text = (
                read_uploaded_file(
                    uploaded_file
                )
            )

        if text.strip():

            result = (
                generate_review(
                    text
                )
            )

            review_id = (
                save_review(
                    filename,
                    result
                )
            )

            result[
                "review_id"
            ] = review_id

    return render_template(
        "index.html",
        result=result
    )

# ==========================================
# HEALTH CHECK
# ==========================================

@app.route(
    "/health"
)
def health():

    return jsonify({

        "status":
        "running",

        "service":
        "TestLens AI"

    })

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )