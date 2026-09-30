from typing import Dict, Any, List, Optional
from backend.app.jobs.skill_gap import SkillGapAnalyzer, skill_gap_analyzer
from backend.app.jobs.job_search import JobSearchService, job_search_service


class JobService:
    """
    Facade for all job search and candidate-job skill matching domain operations.
    """

    def __init__(self):
        self.gap_analyzer = skill_gap_analyzer
        self.job_searcher = job_search_service

    def search_jobs(self, keywords: str, location: str = "India", page: int = 1, result_count: int = 10) -> Dict[str, Any]:
        return self.job_searcher.search_jobs(keywords, location, page, result_count)

    def analyze_job_fit(self, student_skills: List[Any], required_skills: List[Any]) -> Dict[str, Any]:
        return self.gap_analyzer.calculate_gap(student_skills, required_skills)


job_service = JobService()
