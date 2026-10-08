# 🤖 AI Job Matcher

AI Job Matcher is a full-stack web application that helps job seekers find relevant job opportunities based on their resume skills.

The application analyzes an uploaded resume, extracts technical skills, fetches real-time job listings, and calculates a match percentage between the candidate's skills and each job's requirements.

---

## 🚀 Features

- 🔐 User Registration and Login
- 📧 Email OTP Verification
- 📄 Resume Upload and Analysis
- 🧠 Automatic Resume Skill Extraction
- 🔎 Real-Time Job Search
- 🎯 Resume-to-Job Skill Matching
- 📊 Job Match Percentage
- ✅ Matched Skills Detection
- ❌ Missing Skills Detection
- 💾 Save Jobs
- 🔗 Direct Job Application Links
- 📱 Responsive Dashboard
- 🗄️ PostgreSQL Database
- 🔒 Password Hashing with Bcrypt
- 🌐 REST API Backend

---

## 🛠️ Technologies Used

### Frontend

- React.js
- JavaScript
- HTML5
- CSS3
- Vite
- React Router

### Backend

- Python
- FastAPI
- SQLAlchemy
- REST APIs
- Bcrypt
- Python-dotenv

### Database

- PostgreSQL

### Job API

- Adzuna Jobs API

### Development Tools

- Git
- GitHub
- VS Code
- Postman
- Swagger UI

---

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
🎯 Job Matching

The application compares the skills detected in the user's resume with skills identified from job descriptions.

For example:

Resume Skills:
Python
Java
React
SQL
PostgreSQL

Job Requirements:
Python
SQL
React
Docker
AWS

Matched Skills:
✓ Python
✓ SQL
✓ React

Missing Skills:
✗ Docker
✗ AWS

Match:
60%

This helps users understand which jobs are a good match and which skills they may need to improve.

📄 Resume Analysis

The resume parser extracts information such as:

Name
Skills
Education
Experience
Projects
Certifications

The extracted information is then used by the job matching system.

🔎 Real-Time Jobs

The application uses the Adzuna Jobs API to retrieve current job listings.

Users can search using:

Job keyword
Location
Minimum match percentage

Example:

Keyword: Software Developer
Location: India
Minimum Match: 60%
🔐 Authentication

The application includes:

User registration
Secure password hashing
Email OTP verification
Login authentication
Protected dashboard access

Passwords are hashed using Bcrypt before being stored in the database.

🗄️ Database

The application uses PostgreSQL.

Main tables include:

users
otp_verifications
resumes
jobs
saved_jobs
⚙️ Installation
1. Clone the Repository
git clone https://github.com/amalsai-cmd/ai-job-matcher.git
cd ai-job-matcher
2. Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv

Activate it on Windows:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

GMAIL_EMAIL=your_gmail_address
GMAIL_APP_PASSWORD=your_gmail_app_password

⚠️ Never upload .env to GitHub.

Start the backend:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
3. Frontend Setup

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend:

http://localhost:5173
🔑 Environment Variables

The following environment variables are required:

Variable	Description
ADZUNA_APP_ID	Adzuna application ID
ADZUNA_APP_KEY	Adzuna API key
GMAIL_EMAIL	Gmail sender address
GMAIL_APP_PASSWORD	Gmail app password

Never commit real credentials to GitHub.

📸 Screenshots
Login

Add your login page screenshot here.

docs/screenshots/login.png
Dashboard

Add your dashboard screenshot here.

docs/screenshots/dashboard.png
Resume Analysis

Add your resume analysis screenshot here.

docs/screenshots/resume-analysis.png
Job Matching

Add your job matching screenshot here.

docs/screenshots/job-matching.png
📌 Future Improvements
🤖 AI-powered resume recommendations
📈 Skill gap analysis
🎯 Personalized career recommendations
📝 AI resume improvement suggestions
📊 Application tracking
🔔 Job alerts
⭐ Advanced job ranking
🧠 Improved semantic skill matching
☁️ Cloud deployment
📱 Mobile-friendly improvements
👨‍💻 Developer

Murari Venkata Amal Sai

B.Tech – Computer Science & Information Technology

KL University

📄 License

This project is developed for educational and portfolio purposes.

<img width="1830" height="848" alt="Screenshot 2026-10-08 120808" src="https://github.com/user-attachments/assets/6f051ca7-faa5-45f7-8e7e-d1dada7b635d" />
<img width="1876" height="883" alt="Screenshot 2026-10-08 120752" src="https://github.com/user-attachments/assets/821daf6d-beec-405f-b129-40c6914015c7" />
<img width="1912" height="890" alt="Screenshot 2026-10-08 120544" src="https://github.com/user-attachments/assets/47d4af12-4b4a-4761-812b-2f6f9c08cb4f" />
<img width="1321" height="542" alt="Screenshot 2026-10-08 120431" src="https://github.com/user-attachments/assets/3462811b-0e1c-4ce8-8389-2dc75adef41f" />
<img width="1912" height="903" alt="Screenshot 2026-10-08 115742" src="https://github.com/user-attachments/assets/619a4526-0fc0-41aa-95ef-6f0448334fa1" />
<img width="1839" height="875" alt="Screenshot 2026-10-08 115726" src="https://github.com/user-attachments/assets/7023b069-71a5-408a-9886-ea348bf66b62" />
<img width="1888" height="887" alt="Screenshot 2026-10-08 115716" src="https://github.com/user-attachments/assets/e570cac2-4ac9-4e3f-8baa-9b4c0f0ac202" />
<img width="1918" height="794" alt="Screenshot 2026-10-08 115704" src="https://github.com/user-attachments/assets/9c0326ad-561a-49a8-97b5-50b0eafac301" />
<img width="1895" height="899" alt="Screenshot 2026-10-08 115638" src="https://github.com/user-attachments/assets/e3b0f327-ee69-4f70-98ef-81128981626e" />
<img width="1918" height="903" alt="Screenshot 2026-10-08 115504" src="https://github.com/user-attachments/assets/fd19d2bd-a1fe-4bac-a6e8-413b31749e38" />
<img width="1918" height="903" alt="Screenshot 2026-10-08 115204" src="https://github.com/user-attachments/assets/d92e4078-2ec8-4666-aec1-13f822f6dd20" />
<img width="1914" height="1116" alt="Screenshot 2026-10-08 115128" src="https://github.com/user-attachments/assets/187a4cd3-9e6c-4b97-8825-72d12174bbed" />
