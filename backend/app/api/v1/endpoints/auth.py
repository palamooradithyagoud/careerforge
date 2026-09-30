import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_student,
)
from backend.app.models.profile import Student, AcademicProfile, StudentSkill
from backend.app.schemas.profile import (
    DemoAuthRequest,
    LoginRequest,
    RegisterRequest,
    AuthResponse,
)
from backend.app.services.n8n_service import (
    trigger_student_registration_webhook,
    trigger_scholarship_eligibility_webhook,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dummy hash for constant-time comparison when email is not found (prevents timing attacks)
_DUMMY_BCRYPT_HASH = "$2b$12$e8Y50q7e7rK56X3m9s2sOuq98W8M8zF9J8s3y7k4h1f6x2g5v8n0e"


@router.post("/demo", response_model=AuthResponse)
def demo_login(
    payload: DemoAuthRequest = DemoAuthRequest(),
    db: Session = Depends(get_db)
):
    """
    Standard demo entry point for evaluation and testing.
    Issues a valid cryptographically-signed JWT for the selected educational stage demo student.
    """
    stage = (payload.education_stage or "b_tech").strip().lower()
    email_map = {
        "class_10": "demo.class10@skillcatalyst.dev",
        "intermediate": "demo.intermediate@skillcatalyst.dev",
        "b_tech": "demo.student@skillcatalyst.dev",
    }
    target_email = email_map.get(stage, "demo.student@skillcatalyst.dev")
    student = db.query(Student).filter(Student.email == target_email).first()

    # Fallback to any student with matching stage
    if not student:
        student = db.query(Student).filter(Student.education_stage == stage).first()

    if not student:
        # Create demo student if database was cleared
        student = Student(
            id=f"demo-student-uuid-{stage}",
            name=f"Demo {stage.replace('_', ' ').title()} Student",
            email=target_email,
            education_stage=stage,
            location="Hyderabad, India",
            target_role="Software Engineer" if stage == "b_tech" else "Student",
            password_hash=hash_password("demo123")
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    # Issue real, secure signed JWT token
    token = create_access_token({
        "sub": student.id,
        "email": student.email,
        "stage": student.education_stage,
        "role": "student"
    })

    return AuthResponse(
        token=token,
        student_id=student.id,
        email=student.email,
        name=student.name,
        has_profile=bool(student.academic_profile),
        education_stage=student.education_stage
    )


@router.post("/login", response_model=AuthResponse)
def login(
    credentials: LoginRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Secure email/password login endpoint.
    Retrieves user, verifies bcrypt password hash, and issues authenticated JWT.
    Returns identical failure response to avoid leaking whether an email exists.
    """
    email_clean = str(credentials.email).strip().lower()
    student = db.query(Student).filter(Student.email == email_clean).first()

    if not student or not student.password_hash:
        # Execute dummy verification to preserve constant timing against enumeration
        verify_password("dummy_password_timing_check", _DUMMY_BCRYPT_HASH)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password against stored bcrypt hash
    if not verify_password(credentials.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Issue signed JWT with student claims
    token = create_access_token({
        "sub": student.id,
        "email": student.email,
        "stage": student.education_stage,
        "role": "student"
    })

    # Optional greeting trigger in background
    trigger_student_registration_webhook(student.id, db=db, background_tasks=background_tasks, force=False)

    return AuthResponse(
        token=token,
        student_id=student.id,
        email=student.email,
        name=student.name,
        has_profile=bool(student.academic_profile),
        education_stage=student.education_stage
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Creates a new student account with bcrypt-hashed password and issues authenticated JWT.
    Enforces email uniqueness without leaking information on login.
    """
    email_clean = str(payload.email).strip().lower()
    existing = db.query(Student).filter(Student.email == email_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please log in instead."
        )

    raw_password = payload.password or "password123"
    if len(raw_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 6 characters in length."
        )

    # Hash password with bcrypt before storing
    hashed = hash_password(raw_password)
    stage = payload.education_stage.strip().lower()

    student = Student(
        name=payload.name.strip(),
        email=email_clean,
        education_stage=stage,
        location=payload.location,
        target_role="Software Engineer" if stage == "b_tech" else None,
        password_hash=hashed
    )
    db.add(student)
    db.flush()

    # Academic profile setup
    acad = AcademicProfile(student_id=student.id)
    acad.school_or_college = payload.school_or_college or ("Engineering College" if stage == "b_tech" else "Junior College")
    acad.year = payload.year or ("1st Year" if stage == "b_tech" else "1st Year (11th)")

    if stage == "b_tech":
        acad.branch = payload.branch_or_stream or "Computer Science and Engineering"
        score_val = payload.score or 8.0
        acad.cgpa = float(score_val) if score_val <= 10.0 else round(score_val / 10.0, 2)
        acad.percentage = round(acad.cgpa * 9.5, 2) if acad.cgpa else 76.0
    else:
        acad.stream = payload.branch_or_stream or "MPC"
        acad.percentage = float(payload.score) if payload.score else 80.0

    db.add(acad)

    # Default starter skills for B.Tech students
    if stage == "b_tech":
        for s_name, prof in [("Python", "Advanced"), ("Data Structures", "Intermediate"), ("Web Development", "Intermediate")]:
            db.add(StudentSkill(student_id=student.id, skill_name=s_name, proficiency=prof))

    db.commit()
    db.refresh(student)

    # Issue signed JWT
    token = create_access_token({
        "sub": student.id,
        "email": student.email,
        "stage": student.education_stage,
        "role": "student"
    })

    # Trigger welcome automation webhooks in background
    trigger_student_registration_webhook(student.id, db=db, background_tasks=background_tasks, force=True)
    trigger_scholarship_eligibility_webhook(student.id, db=db, background_tasks=background_tasks, force=True)

    return AuthResponse(
        token=token,
        student_id=student.id,
        email=student.email,
        name=student.name,
        has_profile=True,
        education_stage=student.education_stage
    )


@router.get("/me", response_model=AuthResponse)
def get_current_user_profile(
    current_student: Student = Depends(get_current_student)
):
    """
    Returns the authenticated student identity decoded from JWT.
    Enforces token validity and expiration.
    """
    token = create_access_token({
        "sub": current_student.id,
        "email": current_student.email,
        "stage": current_student.education_stage,
        "role": "student"
    })
    return AuthResponse(
        token=token,
        student_id=current_student.id,
        email=current_student.email,
        name=current_student.name,
        has_profile=bool(current_student.academic_profile),
        education_stage=current_student.education_stage
    )


@router.post("/logout")
def logout(
    current_student: Student = Depends(get_current_student)
):
    """
    Stateless JWT logout endpoint. Informs client to discard stored credentials.
    """
    return {
        "status": "success",
        "message": f"Successfully logged out student {current_student.email}"
    }
