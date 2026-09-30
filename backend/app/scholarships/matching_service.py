from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.profile import Student, Scholarship
from backend.app.scholarships.eligibility_engine import ScholarshipEligibilityEngine
from backend.app.services.scholarship_matcher import (
    evaluate_scholarship_eligibility,
    find_eligible_scholarships as _find_eligible,
    check_scholarship_eligibility as _check_eligibility,
    calculate_profile_completeness
)

eligibility_engine = ScholarshipEligibilityEngine()


class ScholarshipMatchingService:
    """
    Deterministic domain service for matching students with relevant scholarship grants.
    """

    def __init__(self):
        self.engine = eligibility_engine

    def evaluate_scholarship(self, student: Student, scholarship: Scholarship):
        return evaluate_scholarship_eligibility(scholarship, student)

    def evaluate_detailed_eligibility(self, student: Any, scholarship: Any) -> Dict[str, Any]:
        return self.engine.check_eligibility(student, scholarship)

    def find_matches(self, student: Student, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        return _find_eligible(student, db, limit=limit)

    def compute_completeness(self, student: Student):
        return calculate_profile_completeness(student)


scholarship_matching_service = ScholarshipMatchingService()
