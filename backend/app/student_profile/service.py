from typing import Dict, Any, Tuple, List, Optional
from sqlalchemy.orm import Session
from backend.app.models.profile import Student, Scholarship
from backend.app.services.scholarship_matcher import (
    calculate_profile_completeness,
    compute_student_intelligence_summary
)


class StudentProfileService:
    """
    Domain service for student profile intelligence, stage-aware completeness,
    and profile personalization.
    """

    def get_completeness(self, student: Student) -> Tuple[int, List[str]]:
        return calculate_profile_completeness(student)

    def get_intelligence_summary(self, student: Student, scholarships: List[Scholarship]):
        return compute_student_intelligence_summary(student, scholarships)

    def get_student_by_id(self, db: Session, student_id: str) -> Optional[Student]:
        return db.query(Student).filter(Student.id == student_id).first()


student_profile_service = StudentProfileService()
