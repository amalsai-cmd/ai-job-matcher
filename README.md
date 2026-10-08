# 🤖 AI Job Matcher

AI Job Matcher is a full-stack web application that helps job seekers discover relevant job opportunities based on their resume skills.

The application analyzes an uploaded resume, extracts technical skills, fetches real-time job listings, and calculates a match percentage between the candidate's skills and each job's requirements.

## 🚀 Features

* 🔐 User Registration and Login
* 📧 Email OTP Verification
* 📄 Resume Upload and Analysis
* 🧠 Automatic Resume Skill Extraction
* 🔎 Real-Time Job Search
* 🎯 Resume-to-Job Skill Matching
* 📊 Job Match Percentage
* ✅ Matched Skills Detection
* ❌ Missing Skills Detection
* 💾 Save Jobs
* 🔗 Direct Job Application Links
* 📱 Responsive Dashboard
* 🗄️ PostgreSQL Database
* 🔒 Password Hashing with Bcrypt
* 🌐 REST API Backend

## 🛠️ Technologies Used

### Frontend

* React.js
* JavaScript
* HTML5
* CSS3
* Vite
* React Router

### Backend

* Python
* FastAPI
* SQLAlchemy
* REST APIs
* Bcrypt
* Python-dotenv

### Database

* PostgreSQL

### Job API

* Adzuna Jobs API

### Development Tools

* Git
* GitHub
* VS Code
* Postman
* Swagger UI

## 🏗️ Project Architecture

```text
AI Job Matcher
│
├── backend
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── resume_parser.py
│   ├── uploads/
│   └── requirements.txt
│
├── frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── VerifyOTP.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
│
├── docs/
│
├── .gitignore
└── README.md
```

## 🎯 How Job Matching Works

The application compares the skills detected in the user's resume with skills identified from job descriptions.

### Example

**Resume Skills**

```text
Python
Java
React
SQL
PostgreSQL
```

**Job Requirements**

```text
Python
SQL
React
Docker
AWS
```

**Matched Skills**

```text
✓ Python
✓ SQL
✓ React
```

**Missing Skills**

```text
✗ Docker
✗ AWS
```

**Match Percentage: 60%**

This helps users understand which jobs are a good match and which skills they may need to improve.

## 📄 Resume Analysis

The resume parser extracts information such as:

* Name
* Skills
* Education
* Experience
* Projects
* Certifications

The extracted information is then used by the job matching system.

## 🔎 Real-Time Job Search

The application uses the **Adzuna Jobs API** to retrieve current job listings.

Users can search using:

* Job keyword
* Location
* Minimum match percentage

### Example

```text
Keyword: Software Developer
Location: India
Minimum Match: 60%
```

## 🔐 Authentication

The application includes:

* User registration
* Secure password hashing
* Email OTP verification
* Login authentication
* Protected dashboard access

Passwords are hashed using Bcrypt before being stored in the database.

## 🗄️ Database

The application uses PostgreSQL.

### Main Tables

```text
users
otp_verifications
resumes
jobs
saved_jobs
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/amalsai-cmd/ai-job-matcher.git
cd ai-job-matcher
```

### 2. Backend Setup

Go to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend` directory:

```env
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

GMAIL_EMAIL=your_gmail_address
GMAIL_APP_PASSWORD=your_gmail_app_password
```

⚠️ **Never upload `.env` or real API credentials to GitHub.**

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🔑 Environment Variables

| Variable             | Description           |
| -------------------- | --------------------- |
| `ADZUNA_APP_ID`      | Adzuna application ID |
| `ADZUNA_APP_KEY`     | Adzuna API key        |
| `GMAIL_EMAIL`        | Gmail sender address  |
| `GMAIL_APP_PASSWORD` | Gmail app password    |

> Never commit real credentials to GitHub.

## 📸 Screenshots

### 🔐 Login

The application provides a secure login interface for registered users.

### 📝 Registration

Users can create an account and verify their email through OTP authentication.

### 📄 Resume Analysis

Users can upload their resume and view extracted information including skills, education, experience, projects, and certifications.

### 🎯 Job Matching

The dashboard displays real-time jobs along with their match percentage, matched skills, and missing skills.

### 🔎 Job Search

Users can search for jobs by keyword and location and filter results based on their desired match percentage.

### 💾 Saved Jobs

Users can save interesting job opportunities and access them later.

## 📌 Future Improvements

* 🤖 AI-powered resume recommendations
* 📈 Skill gap analysis
* 🎯 Personalized career recommendations
* 📝 AI resume improvement suggestions
* 📊 Application tracking
* 🔔 Job alerts
* ⭐ Advanced job ranking
* 🧠 Improved semantic skill matching
* ☁️ Cloud deployment
* 📱 Mobile application

## 👨‍💻 Developer

**Murari Venkata Amal Sai**

B.Tech – Computer Science & Information Technology
KL University

## 📄 License

This project is developed for educational and portfolio purposes.
