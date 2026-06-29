from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import os
import PyPDF2
import re

app = Flask(__name__)

# =========================
# CONFIG
# =========================

app.secret_key = "resume_analyzer_secret_key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# PDF TEXT EXTRACTION
# =========================

def extract_text_from_pdf(filepath):

    text = ""

    try:
        with open(filepath, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

    except Exception:
        return ""

    return text.lower().strip()


# =========================
# SKILL EXTRACTION
# =========================

def extract_skills(text):

    text = text.lower()

    skills = [

        # Programming
        "python","java","c","c++","c#","go","rust","php","r","matlab",

        # Web
        "html","css","javascript","typescript",
        "react","react.js","angular","vue",
        "node.js","express","express.js",
        "bootstrap","tailwind","flask","django","spring",

        # Database
        "sql","mysql","postgresql","mongodb",
        "sqlite","redis","firebase",

        # Cloud
        "aws","azure","gcp",
        "docker","kubernetes","jenkins",
        "linux","bash","git","github","gitlab",

        # AI
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "ai",
        "data science",
        "tensorflow",
        "keras",
        "pytorch",
        "opencv",
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",

        # VLSI
        "verilog",
        "systemverilog",
        "vhdl",
        "rtl",
        "fpga",
        "asic",
        "vlsi",
        "vivado",
        "modelsim",
        "gtkwave",
        "spice",

        # Embedded
        "embedded",
        "arduino",
        "stm32",
        "raspberry pi",
        "microcontroller",
        "iot",

        # Mobile
        "android",
        "flutter",
        "dart",
        "kotlin",

        # Misc
        "rest api",
        "jwt",
        "graphql",
        "postman",
        "socket",
        "networking"
    ]

    found = []

    for skill in skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))
# =========================
# ATS SCORING ENGINE
# =========================

def calculate_score(skills, text):

    text = text.lower()

    # =========================
    # 1. Skills Score (40)
    # =========================

    skills_score = min(len(skills) * 2, 40)

    # =========================
    # 2. Projects Score (20)
    # =========================

    project_keywords = [
        "project",
        "developed",
        "implemented",
        "designed",
        "built",
        "created",
        "application",
        "system",
        "platform",
        "simulation",
        "api",
        "dashboard",
        "automation"
    ]

    project_score = 0

    for word in project_keywords:
        if word in text:
            project_score += 2

    project_score = min(project_score, 20)

    # =========================
    # 3. Education Score (15)
    # =========================

    education_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "master",
        "m.tech",
        "phd",
        "university",
        "college",
        "cgpa",
        "percentage",
        "marks"
    ]

    education_score = 0

    for word in education_keywords:
        if word in text:
            education_score += 2

    education_score = min(education_score, 15)

    # =========================
    # 4. Resume Quality Score (25)
    # =========================

    quality_keywords = [

        # Experience
        "experience",
        "internship",
        "intern",
        "worked",

        # Certifications
        "certificate",
        "certification",
        "coursera",
        "udemy",
        "nptel",

        # Soft Skills
        "leadership",
        "teamwork",
        "communication",
        "problem solving",

        # Achievements
        "award",
        "achievement",
        "responsibility"
    ]

    keyword_score = 0

    for word in quality_keywords:
        if word in text:
            keyword_score += 2

    # Resume Length Bonus

    words = len(text.split())

    if words >= 600:
        keyword_score += 5

    elif words >= 400:
        keyword_score += 3

    elif words >= 250:
        keyword_score += 2

    keyword_score = min(keyword_score, 25)

    # =========================
    # Final ATS Score
    # =========================

    total = (
        skills_score +
        project_score +
        education_score +
        keyword_score
    )

    total = min(total, 100)

    return {

        "total": total,

        "skills_score": skills_score,

        "project_score": project_score,

        "education_score": education_score,

        "keyword_score": keyword_score
    }
# =========================
# JOB DESCRIPTION MATCHING
# =========================

def match_resume_with_jd(resume_text, jd_text):

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(list(resume_skills & jd_skills))
    missing = sorted(list(jd_skills - resume_skills))

    if len(jd_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = round(
            (len(matched) / len(jd_skills)) * 100
        )

    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": match_percentage
    }


# =========================
# SMART DOMAIN DETECTION
# =========================

def detect_domain(text):

    text = text.lower()

    domains = {

        "AI / Data Science Engineer": [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "keras",
            "pytorch",
            "opencv",
            "numpy",
            "pandas",
            "scikit-learn",
            "data science"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "typescript",
            "react",
            "angular",
            "vue",
            "node.js",
            "express",
            "mongodb",
            "postgresql",
            "flask",
            "django"
        ],

        "Cloud / DevOps Engineer": [
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "jenkins",
            "linux",
            "git"
        ],

        "VLSI / Digital Design Engineer": [
            "verilog",
            "systemverilog",
            "vhdl",
            "rtl",
            "fpga",
            "asic",
            "vlsi",
            "vivado",
            "modelsim",
            "gtkwave",
            "spice"
        ],

        "Embedded Systems Engineer": [
            "embedded",
            "arduino",
            "stm32",
            "raspberry pi",
            "microcontroller",
            "iot"
        ],

        "Mobile App Developer": [
            "android",
            "flutter",
            "dart",
            "kotlin"
        ]
    }

    scores = {}

    for domain, keywords in domains.items():

        score = 0

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                score += 1

        scores[domain] = score

    if max(scores.values()) == 0:
        return "General Software Engineer"

    return max(scores, key=scores.get)

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("resume")
        job_description = request.form.get("job_description", "").lower()

        if file and file.filename:

            # Save uploaded resume
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # =========================
            # Resume Processing
            # =========================

            text = extract_text_from_pdf(filepath)

            skills = extract_skills(text)

            score_data = calculate_score(skills, text)

            domain = detect_domain(text)

            # =========================
            # JD Matching
            # =========================

            jd_result = match_resume_with_jd(
                text,
                job_description
            )

            # =========================
            # Store in Session
            # =========================

            session["filename"] = filename
            session["text"] = text
            session["skills"] = skills
            session["score"] = score_data["total"]
            session["domain"] = domain

            session["skills_score"] = score_data["skills_score"]
            session["project_score"] = score_data["project_score"]
            session["education_score"] = score_data["education_score"]
            session["keyword_score"] = score_data["keyword_score"]

            session["match_percentage"] = jd_result["match_percentage"]
            session["matched_skills"] = jd_result["matched"]
            session["missing_skills"] = jd_result["missing"]
            session["has_jd"] = bool(job_description.strip())

            # =========================
            # Show Result Page
            # =========================

            return render_template(

                "result.html",

                filename=filename,

                text=text[:1000],

                skills=skills,

                score=score_data["total"],

                skills_score=score_data["skills_score"],

                project_score=score_data["project_score"],

                education_score=score_data["education_score"],

                keyword_score=score_data["keyword_score"],

                domain=domain,

                match_percentage=jd_result["match_percentage"],

                matched_skills=jd_result["matched"],

                missing_skills=jd_result["missing"],

                has_jd=bool(job_description.strip())

            )

    return render_template("upload.html")
# =========================
# RESULT PAGE
# =========================

@app.route("/result")
def result():

    return render_template(

        "result.html",

        filename=session.get("filename", ""),

        text=session.get("text", "")[:1000],

        skills=session.get("skills", []),

        score=session.get("score", 0),

        domain=session.get("domain", ""),

        # Score Breakdown
        skills_score=session.get("skills_score", 0),

        project_score=session.get("project_score", 0),

        education_score=session.get("education_score", 0),

        keyword_score=session.get("keyword_score", 0),

        # Job Description Matching
        match_percentage=session.get("match_percentage", 0),

        matched_skills=session.get("matched_skills", []),

        missing_skills=session.get("missing_skills", []),

        has_jd=session.get("has_jd", False)

    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)