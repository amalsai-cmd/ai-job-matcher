from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

import bcrypt
import os
import uuid
import random
import smtplib
import requests
import re

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

import models
from database import engine, SessionLocal
from resume_parser import analyze_resume


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

models.Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Job Matcher API",
    description="AI Job Matcher backend with resume analysis and real-time job matching",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str


class LoginRequest(BaseModel):
    email: str
    password: str


class JobRequest(BaseModel):
    title: str
    company: str
    location: str
    description: str
    required_skills: str
    experience: str | None = None
    job_type: str | None = None
    salary: str | None = None
    job_url: str | None = None


# ============================================================
# BASIC ROUTES
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Job Matcher API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/test")
def test_api():
    return {
        "message": "API is working successfully!"
    }


@app.get("/api/db-test")
def db_test(db: Session = Depends(get_db)):

    try:
        db.execute(models.text("SELECT 1"))

        return {
            "message": "Database connection successful!"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SEND OTP EMAIL
# ============================================================

def send_otp_email(email: str, otp: str):

    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("Gmail credentials are missing in .env")
        print("OTP for testing:", otp)
        return

    message = MIMEMultipart()

    message["From"] = GMAIL_EMAIL
    message["To"] = email
    message["Subject"] = "AI Job Matcher - Email Verification OTP"

    body = f"""
Hello,

Your AI Job Matcher verification OTP is:

{otp}

This OTP will expire in 10 minutes.

If you did not request this OTP, please ignore this email.

Regards,
AI Job Matcher
"""

    message.attach(
        MIMEText(body, "plain")
    )

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            GMAIL_EMAIL,
            GMAIL_APP_PASSWORD
        )

        server.sendmail(
            GMAIL_EMAIL,
            email,
            message.as_string()
        )

        server.quit()

    except Exception as e:

        print("Email sending failed:", e)
        print("OTP for testing:", otp)


# ============================================================
# REGISTER
# ============================================================

@app.post("/api/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == request.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    # Check existing OTP record

    existing_otp = db.query(
        models.OTPVerification
    ).filter(
        models.OTPVerification.email == request.email
    ).first()


    # Generate OTP

    otp = str(
        random.randint(
            100000,
            999999
        )
    )


    # Hash password

    password_hash = bcrypt.hashpw(
        request.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


    expires_at = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=10
    )


    if existing_otp:

        existing_otp.otp = otp
        existing_otp.full_name = request.full_name
        existing_otp.password_hash = password_hash
        existing_otp.expires_at = expires_at
        existing_otp.verified = False

    else:

        new_otp = models.OTPVerification(
            email=request.email,
            otp=otp,
            full_name=request.full_name,
            password_hash=password_hash,
            expires_at=expires_at,
            verified=False
        )

        db.add(new_otp)


    db.commit()


    send_otp_email(
        request.email,
        otp
    )


    return {
        "message": "OTP sent successfully",
        "email": request.email
    }


# ============================================================
# VERIFY OTP
# ============================================================

@app.post("/api/verify-otp")
def verify_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    otp_record = db.query(
        models.OTPVerification
    ).filter(
        models.OTPVerification.email == request.email
    ).first()


    if not otp_record:

        raise HTTPException(
            status_code=404,
            detail="OTP not found"
        )


    if otp_record.otp != request.otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )


    current_time = datetime.now(
        timezone.utc
    )


    expires_at = otp_record.expires_at

    if expires_at.tzinfo is None:

        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )


    if current_time > expires_at:

        raise HTTPException(
            status_code=400,
            detail="OTP has expired"
        )


    existing_user = db.query(
        models.User
    ).filter(
        models.User.email == request.email
    ).first()


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )


    new_user = models.User(
        full_name=otp_record.full_name,
        email=otp_record.email,
        password_hash=otp_record.password_hash
    )


    db.add(new_user)

    otp_record.verified = True

    db.commit()

    db.refresh(new_user)


    return {
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email
        }
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/api/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(
        models.User
    ).filter(
        models.User.email == request.email
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    password_correct = bcrypt.checkpw(
        request.password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )


    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }


# ============================================================
# RESUME UPLOAD
# ============================================================

@app.post("/api/resume/upload")
def upload_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Check user

    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    # Check PDF

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    # Read file

    contents = file.file.read()


    # Maximum 5 MB

    if len(contents) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="Resume file must be smaller than 5 MB"
        )


    # Create upload directory

    upload_directory = "uploads/resumes"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )


    # Unique filename

    unique_filename = (
        str(uuid.uuid4())
        + "_"
        + file.filename
    )


    file_path = os.path.join(
        upload_directory,
        unique_filename
    )


    # Save file

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)


    # Save resume information

    new_resume = models.Resume(
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path
    )


    db.add(new_resume)

    db.commit()

    db.refresh(new_resume)


    # Analyze resume

    try:

        analysis = analyze_resume(
            file_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )


    return {
        "message": "Resume uploaded and analyzed successfully",

        "resume": {
            "id": new_resume.id,
            "file_name": new_resume.file_name,
            "user_id": new_resume.user_id,
            "uploaded_at": new_resume.uploaded_at
        },

        "analysis": analysis
    }


# ============================================================
# ALIAS FOR OLD FRONTEND
# ============================================================

@app.post("/api/upload-resume")
def upload_resume_alias(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    return upload_resume(
        user_id=user_id,
        file=file,
        db=db
    )


# ============================================================
# CREATE MANUAL JOB
# ============================================================

@app.post("/api/jobs")
def create_job(
    request: JobRequest,
    db: Session = Depends(get_db)
):

    new_job = models.Job(
        title=request.title,
        company=request.company,
        location=request.location,
        description=request.description,
        required_skills=request.required_skills,
        experience=request.experience,
        job_type=request.job_type,
        salary=request.salary,
        job_url=request.job_url
    )


    db.add(new_job)

    db.commit()

    db.refresh(new_job)


    return {
        "message": "Job created successfully",
        "job": {
            "id": new_job.id,
            "title": new_job.title,
            "company": new_job.company,
            "location": new_job.location,
            "description": new_job.description,
            "required_skills": new_job.required_skills,
            "experience": new_job.experience,
            "job_type": new_job.job_type,
            "salary": new_job.salary,
            "job_url": new_job.job_url
        }
    }


# ============================================================
# GET DATABASE JOBS
# ============================================================

@app.get("/api/jobs")
def get_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(
        models.Job
    ).order_by(
        models.Job.created_at.desc()
    ).all()


    return {
        "count": len(jobs),

        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "required_skills": job.required_skills,
                "experience": job.experience,
                "job_type": job.job_type,
                "salary": job.salary,
                "job_url": job.job_url
            }

            for job in jobs
        ]
    }


# ============================================================
# ADZUNA REAL-TIME JOBS
# ============================================================

@app.get("/api/jobs/realtime")
def get_realtime_jobs(
    what: str = "software developer",
    where: str = "India",
    page: int = 1
):

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:

        raise HTTPException(
            status_code=500,
            detail="Adzuna API credentials are missing in .env file"
        )


    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
    )


    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 20,
        "what": what,
        "where": where,
        "content-type": "application/json"
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

    except requests.RequestException as e:

        raise HTTPException(
            status_code=500,
            detail=f"Adzuna connection failed: {str(e)}"
        )


    if response.status_code != 200:

        raise HTTPException(
            status_code=response.status_code,
            detail=f"Adzuna API request failed: {response.text}"
        )


    data = response.json()


    jobs = []


    for job in data.get("results", []):

        jobs.append({

            "id": job.get("id"),

            "title": job.get("title"),

            "company": job.get(
                "company",
                {}
            ).get(
                "display_name"
            ),

            "location": job.get(
                "location",
                {}
            ).get(
                "display_name"
            ),

            "description": job.get(
                "description"
            ),

            "salary_min": job.get(
                "salary_min"
            ),

            "salary_max": job.get(
                "salary_max"
            ),

            "job_url": job.get(
                "redirect_url"
            ),

            "created": job.get(
                "created"
            )
        })


    return {

        "source": "Adzuna",

        "search": {
            "keyword": what,
            "location": where,
            "page": page
        },

        "count": len(jobs),

        "jobs": jobs
    }


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_LIST = [

    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",

    "html",
    "css",
    "bootstrap",

    "react",
    "react.js",
    "angular",
    "vue",

    "node.js",
    "nodejs",
    "express",
    "express.js",

    "django",
    "flask",
    "fastapi",

    "spring",
    "spring boot",

    "php",
    "laravel",

    "git",
    "github",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "rest api",
    "rest apis",
    "api",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",

    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",

    "power bi",
    "tableau",

    "linux",

    "jenkins",
    "ci/cd",

    "redis",

    "firebase",

    "figma"
]


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill: str):

    skill = skill.lower().strip()

    replacements = {
        "react.js": "react",
        "reactjs": "react",
        "node.js": "node.js",
        "nodejs": "node.js",
        "express.js": "express",
        "expressjs": "express",
        "postgres": "postgresql",
        "postgre sql": "postgresql",
        "mongo db": "mongodb",
        "ms sql": "sql",
        "javascript": "javascript",
        "java script": "javascript",
    }


    return replacements.get(
        skill,
        skill
    )


# ============================================================
# EXTRACT SKILLS FROM TEXT
# ============================================================

def extract_skills_from_text(text: str):

    if not text:

        return []


    text = text.lower()

    detected_skills = []


    for skill in SKILL_LIST:

        # Escape special characters
        pattern = re.escape(skill.lower())


        # Word boundary where possible
        if re.search(
            r"(?<!\w)" + pattern + r"(?!\w)",
            text
        ):

            normalized = normalize_skill(
                skill
            )

            if normalized not in detected_skills:

                detected_skills.append(
                    normalized
                )


    return detected_skills


# ============================================================
# GET RESUME SKILLS
# ============================================================

def get_resume_skills(resume_analysis):

    skills = resume_analysis.get(
        "skills",
        []
    )


    if isinstance(skills, list):

        result = []

        for skill in skills:

            normalized = normalize_skill(
                str(skill)
            )

            if normalized not in result:

                result.append(
                    normalized
                )

        return result


    if isinstance(skills, str):

        return extract_skills_from_text(
            skills
        )


    return []


# ============================================================
# CALCULATE JOB MATCH
# ============================================================

def calculate_job_match(
    resume_skills,
    job_title,
    job_description
):

    resume_skills = [
        normalize_skill(skill)
        for skill in resume_skills
    ]


    # Combine title + description

    job_text = (
        str(job_title or "")
        + " "
        + str(job_description or "")
    )


    # Extract job skills

    job_skills = extract_skills_from_text(
        job_text
    )


    # Find matched skills

    matched_skills = []

    for skill in resume_skills:

        if skill in job_skills:

            matched_skills.append(
                skill
            )


    # Missing skills

    missing_skills = []

    for skill in job_skills:

        if skill not in resume_skills:

            missing_skills.append(
                skill
            )


    # Calculate percentage

    if len(job_skills) == 0:

        match_percentage = 0

    else:

        match_percentage = round(
            (
                len(matched_skills)
                /
                len(job_skills)
            )
            * 100
        )


    return {

        "match_percentage":
            match_percentage,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "job_required_skills":
            job_skills
    }


# ============================================================
# RECOMMENDED JOBS
# ============================================================
# IMPORTANT:
# This route MUST come before:
# /api/jobs/{job_id}
#
# Otherwise FastAPI may treat "recommended"
# as a job_id.
# ============================================================

@app.get("/api/jobs/recommended")
def get_recommended_jobs(
    user_id: int,
    what: str = "software developer",
    where: str = "India",
    page: int = 1,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check Adzuna credentials
    # --------------------------------------------------------

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:

        raise HTTPException(
            status_code=500,
            detail="Adzuna API credentials are missing in .env file"
        )


    # --------------------------------------------------------
    # Check user
    # --------------------------------------------------------

    user = db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    # --------------------------------------------------------
    # Get latest resume
    # --------------------------------------------------------

    resume = db.query(
        models.Resume
    ).filter(
        models.Resume.user_id == user_id
    ).order_by(
        models.Resume.uploaded_at.desc()
    ).first()


    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Please upload your resume first"
        )


    # --------------------------------------------------------
    # Analyze latest resume
    # --------------------------------------------------------

    try:

        resume_analysis = analyze_resume(
            resume.file_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )


    # --------------------------------------------------------
    # Get resume skills
    # --------------------------------------------------------

    resume_skills = get_resume_skills(
        resume_analysis
    )


    # --------------------------------------------------------
    # Get real-time Adzuna jobs
    # --------------------------------------------------------

    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
    )


    params = {

        "app_id":
            ADZUNA_APP_ID,

        "app_key":
            ADZUNA_APP_KEY,

        "results_per_page":
            20,

        "what":
            what,

        "where":
            where,

        "content-type":
            "application/json"
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

    except requests.RequestException as e:

        raise HTTPException(
            status_code=500,
            detail=f"Adzuna connection failed: {str(e)}"
        )


    if response.status_code != 200:

        raise HTTPException(
            status_code=response.status_code,
            detail=f"Adzuna API request failed: {response.text}"
        )


    data = response.json()


    # --------------------------------------------------------
    # Match jobs
    # --------------------------------------------------------

    recommended_jobs = []


    for job in data.get(
        "results",
        []
    ):

        title = job.get(
            "title"
        )

        company = job.get(
            "company",
            {}
        ).get(
            "display_name"
        )

        location = job.get(
            "location",
            {}
        ).get(
            "display_name"
        )

        description = job.get(
            "description"
        )

        job_url = job.get(
            "redirect_url"
        )

        created = job.get(
            "created"
        )

        salary_min = job.get(
            "salary_min"
        )

        salary_max = job.get(
            "salary_max"
        )


        # Calculate match

        match = calculate_job_match(

            resume_skills,

            title,

            description
        )


        recommended_jobs.append({

            "id":
                job.get("id"),

            "title":
                title,

            "company":
                company,

            "location":
                location,

            "description":
                description,

            "salary_min":
                salary_min,

            "salary_max":
                salary_max,

            "job_url":
                job_url,

            "created":
                created,

            "match_percentage":
                match["match_percentage"],

            "matched_skills":
                match["matched_skills"],

            "missing_skills":
                match["missing_skills"],

            "job_required_skills":
                match["job_required_skills"]
        })


    # --------------------------------------------------------
    # Sort highest match first
    # --------------------------------------------------------

    recommended_jobs.sort(

        key=lambda job:
            job["match_percentage"],

        reverse=True
    )


    # --------------------------------------------------------
    # Return results
    # --------------------------------------------------------

    return {

        "message":
            "Jobs matched successfully",

        "source":
            "Adzuna",

        "user": {

            "id":
                user.id,

            "name":
                user.full_name,

            "email":
                user.email
        },

        "resume": {

            "id":
                resume.id,

            "file_name":
                resume.file_name,

            "skills":
                resume_skills
        },

        "search": {

            "keyword":
                what,

            "location":
                where,

            "page":
                page
        },

        "count":
            len(recommended_jobs),

        "jobs":
            recommended_jobs
    }


# ============================================================
# GET SINGLE DATABASE JOB
# ============================================================
# KEEP THIS ROUTE AFTER /realtime AND /recommended
# ============================================================

@app.get("/api/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(
        models.Job
    ).filter(
        models.Job.id == job_id
    ).first()


    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )


    return {

        "id":
            job.id,

        "title":
            job.title,

        "company":
            job.company,

        "location":
            job.location,

        "description":
            job.description,

        "required_skills":
            job.required_skills,

        "experience":
            job.experience,

        "job_type":
            job.job_type,

        "salary":
            job.salary,

        "job_url":
            job.job_url
    }

    @app.post("/api/jobs/save")
    def save_job(
    user_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if job exists
    job = db.query(models.Job).filter(
        models.Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Check if already saved
    existing_saved_job = db.query(models.SavedJob).filter(
        models.SavedJob.user_id == user_id,
        models.SavedJob.job_id == job_id
    ).first()

    if existing_saved_job:
        return {
            "message": "Job already saved",
            "saved": True,
            "job_id": job_id
        }

    # Save the job
    saved_job = models.SavedJob(
        user_id=user_id,
        job_id=job_id
    )

    db.add(saved_job)
    db.commit()
    db.refresh(saved_job)

    return {
        "message": "Job saved successfully",
        "saved": True,
        "saved_job_id": saved_job.id,
        "job_id": job_id
    }