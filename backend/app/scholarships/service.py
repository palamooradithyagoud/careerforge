from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.profile import Student, Scholarship
from backend.app.scholarships.eligibility_engine import ScholarshipEligibilityEngine
from backend.app.scholarships.matching_service import scholarship_matching_service


class ScholarshipService:
    """
    Facade for all scholarship-related domain operations.
    """
    def __init__(self):
        self.engine = ScholarshipEligibilityEngine()
        self.matcher = scholarship_matching_service

    def check_eligibility(self, student: Any, scholarship: Any) -> Dict[str, Any]:
        return self.engine.check_eligibility(student, scholarship)

    def find_eligible_scholarships(self, student: Student, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        return self.matcher.find_matches(student, db, limit=limit)

    def get_preview(self, db: Session, stage: Optional[str] = None, limit: int = 50) -> List[Scholarship]:
        query = db.query(Scholarship)
        if stage:
            target_stage = stage.strip().lower()
            query = query.filter(Scholarship.eligible_stages.ilike(f"%{target_stage}%"))
        return query.limit(limit).all()


scholarship_service = ScholarshipService()
