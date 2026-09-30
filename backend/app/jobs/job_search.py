from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from backend.app.services.jooble_service import jooble_service, FALLBACK_JOBS
from backend.app.core.database import SessionLocal


class JobSearchService:
    """
    Domain service for querying job opportunities with explicit distinction
    between live API results and verified cached/fallback entries.
    """

    def __init__(self):
        self.service = jooble_service
        self.fallback_jobs = FALLBACK_JOBS

    def search_jobs(
        self,
        keywords: str,
        location: str = "India",
        page: int = 1,
        result_count: int = 10,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Executes job search. Returns jobs with metadata indicating data source:
        'live_jooble_api' vs 'curated_database_fallback'.
        """
        close_db = False
        active_db = db
        if active_db is None:
            active_db = SessionLocal()
            close_db = True

        try:
            raw_res = self.service.search_jobs(
                db=active_db,
                keyword=keywords,
                location=location,
                page=page,
                limit=result_count
            )
        except Exception:
            raw_res = {
                "total_count": len(self.fallback_jobs),
                "is_live_jooble": False,
                "jobs": self.fallback_jobs[:result_count]
            }
        finally:
            if close_db and active_db:
                active_db.close()

        raw_jobs = raw_res.get("jobs", [])
        is_live = bool(raw_res.get("is_live_jooble", False))

        formatted_jobs = []
        for job in raw_jobs:
            formatted_jobs.append({
                "id": str(job.get("id")),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "salary": job.get("salary"),
                "snippet": job.get("snippet") or job.get("description", ""),
                "link": job.get("apply_link") or job.get("link", "https://jooble.org"),
                "source": job.get("source", "Jooble Live API"),
                "required_skills": job.get("required_skills", []),
                "is_live": is_live,
                "provenance": "live_jooble_api" if is_live else "curated_database_fallback"
            })

        return {
            "query": keywords,
            "location": location,
            "total_found": len(formatted_jobs),
            "data_mode": "live_api" if is_live else "fallback_cache",
            "jobs": formatted_jobs
        }


job_search_service = JobSearchService()
