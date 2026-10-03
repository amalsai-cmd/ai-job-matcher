from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import bcrypt

from database import engine, Base, SessionLocal
import models


# Create FastAPI application
app = FastAPI()


# Create database tables
Base.metadata.create_all(bind=engine)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Job Matcher API is running!"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Test React → FastAPI connection
@app.get("/api/test")
def api_test():
    return {
        "message": "React can connect to FastAPI!"
    }


# Test FastAPI → PostgreSQL connection
@app.get("/api/db-test")
def database_test():
    try:
        with engine.connect() as connection:
            return {
                "status": "success",
                "message": "FastAPI connected to PostgreSQL!"
            }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }


# Register new user
@app.post("/api/register")
def register_user(
    full_name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Convert password to bytes
    password_bytes = password.encode("utf-8")

    # bcrypt supports passwords up to 72 bytes
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 bytes or fewer"
        )

    # Hash password
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create new user
    new_user = models.User(
        full_name=full_name,
        email=email,
        password_hash=hashed_password
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email
        }
    }
    # Login user
@app.post("/api/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Find user by email
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Convert password to bytes
    password_bytes = password.encode("utf-8")

    # Check password
    password_correct = bcrypt.checkpw(
        password_bytes,
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