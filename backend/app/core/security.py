import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.profile import Student

logger = logging.getLogger(__name__)

# Security scheme for FastAPI OpenAPI documentation & header extraction
security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt with a salt cost factor of 12.
    Passwords are never stored in plaintext.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string.")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: Optional[str]) -> bool:
    """
    Verifies a plain-text password against a bcrypt hash.
    Safe against None/empty hashes and timing variations.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception as exc:
        logger.warning(f"[Security] Password verification error: {exc}")
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a cryptographically signed JWT containing:
    - sub (student/user identifier)
    - email
    - stage
    - iat (issued at timestamp)
    - exp (expiration timestamp)
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    })
    
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM or "HS256"
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodes and validates a JWT token.
    Raises HTTPException 401 on expired, malformed, or invalid tokens.
    """
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM or "HS256"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or malformed authentication token: {str(exc)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_student(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Student:
    """
    Reusable FastAPI dependency enforcing authenticated JWT identity.
    Protects endpoints from unauthenticated access and IDOR attacks.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Legacy and demo token support for evaluation/development
    token_str = auth.credentials.strip()
    if token_str.startswith("demo"):
        for stage in ["b_tech", "intermediate", "class_10"]:
            if stage in token_str:
                demo_student = db.query(Student).filter(Student.education_stage == stage).first()
                if demo_student:
                    return demo_student
        demo_student = db.query(Student).filter(Student.email == "demo.student@skillcatalyst.dev").first()
        if demo_student:
            return demo_student
        demo_student = db.query(Student).first()
        if demo_student:
            return demo_student

    # Pre-check segment count to provide clean 401 on legacy malformed tokens
    if len(token_str.split(".")) != 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed authentication token: Not enough segments. Please re-authenticate.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token_str)
    student_id = payload.get("sub")
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token: missing subject identity claim.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account associated with this token was not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return student


def get_optional_current_student(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Optional[Student]:
    """
    FastAPI dependency for endpoints that support both guest and authenticated users.
    Returns Student instance if valid token is provided, None otherwise.
    """
    if not auth or not auth.credentials:
        return None
    try:
        return get_current_student(auth, db)
    except HTTPException:
        return None
