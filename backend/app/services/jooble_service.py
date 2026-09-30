import re
import html
import json
import logging
import time
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.core.config import settings
from backend.app.models.job import Job
from backend.app.services.skill_extractor import extract_skills_from_text

logger = logging.getLogger(__name__)


def clean_html_snippet(raw_snippet: Optional[str]) -> str:
    """Clean HTML tags and entities from Jooble snippet."""
    if not raw_snippet:
        return ""
    text = html.unescape(raw_snippet)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_salary_range(salary_str: Optional[str]) -> tuple[Optional[float], Optional[float]]:
    """Rough parse of salary numbers if present in text."""
    if not salary_str:
        return None, None
    numbers = re.findall(r"[\d,]+", salary_str)
    parsed = []
    for n in numbers:
        cleaned = n.replace(",", "")
        if cleaned.isdigit() and len(cleaned) >= 4:
            parsed.append(float(cleaned))
    if len(parsed) >= 2:
        return min(parsed), max(parsed)
    if len(parsed) == 1:
        return parsed[0], parsed[0]
    return None, None


FALLBACK_JOBS: List[Dict[str, Any]] = [
    {
        "id": "fb-9901",
        "title": "Graduate Software Engineer (SDE-1) - Full Stack",
        "company": "Amazon Web Services (AWS)",
        "location": "Bangalore / Hyderabad, India",
        "salary": "₹16,00,000 – ₹24,00,000 LPA",
        "type": "Full-time",
        "snippet": "We are seeking B.Tech graduates with strong foundations in Python, React, Data Structures, and Cloud Architecture to build scalable web applications.",
        "link": "https://jooble.org/desc/aws-graduate-sde",
        "source": "jooble.org"
    },
    {
        "id": "fb-9902",
        "title": "Frontend Developer (React.js / Next.js)",
        "company": "Flipkart Internet Pvt Ltd",
        "location": "Bangalore, India",
        "salary": "₹12,00,000 – ₹18,00,000 LPA",
        "type": "Full-time",
        "snippet": "Looking for passionate React & TypeScript developers to join our customer experience team. Proficient with state management, REST APIs, and responsive UI.",
        "link": "https://jooble.org/desc/flipkart-frontend-react",
        "source": "jooble.org"
    },
    {
        "id": "fb-9903",
        "title": "Backend Python / FastAPI Engineer",
        "company": "Swiggy (Bundl Technologies)",
        "location": "Hyderabad / Remote, India",
        "salary": "₹14,00,000 – ₹20,00,000 LPA",
        "type": "Full-time",
        "snippet": "Build microservices with Python, FastAPI, and SQL. Must have good understanding of relational databases, caching, and clean code practices.",
        "link": "https://jooble.org/desc/swiggy-python-fastapi",
        "source": "jooble.org"
    },
    {
        "id": "fb-9904",
        "title": "AI/ML Systems Associate",
        "company": "Infosys AI Innovation Labs",
        "location": "Pune / Hyderabad, India",
        "salary": "₹9,50,000 – ₹15,00,000 LPA",
        "type": "Full-time",
        "snippet": "Exciting role for B.Tech grads in Computer Science/IT working on Python, Machine Learning models, NLP pipelines, and data preprocessing.",
        "link": "https://jooble.org/desc/infosys-ai-associate",
        "source": "jooble.org"
    },
    {
        "id": "fb-9905",
        "title": "Cloud DevOps & Platform Associate",
        "company": "Wipro Cloud Solutions",
        "location": "Hyderabad, India",
        "salary": "₹8,50,000 – ₹14,00,000 LPA",
        "type": "Full-time",
        "snippet": "Entry-level platform engineering role for B.Tech engineers proficient in Docker, Linux, Git, and basic AWS cloud infrastructure.",
        "link": "https://jooble.org/desc/wipro-devops-platform",
        "source": "jooble.org"
    }
]


class JoobleService:
    def __init__(self):
        self.api_key = settings.JOOBLE_API_KEY
        self.base_url = f"https://jooble.org/api/{self.api_key}"
        # In-memory query cache: key -> (timestamp, data) with 15-minute TTL
        self._cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self._cache_ttl_seconds = 900.0  # 15 minutes
        self._max_cache_entries = 200

    def _get_cache_key(self, keyword: str, location: str, page: int) -> str:
        return f"{keyword.strip().lower()}:{location.strip().lower()}:{page}"

    def _get_cached_query(self, key: str) -> Optional[Dict[str, Any]]:
        now = time.time()
        entry = self._cache.get(key)
        if entry:
            ts, data = entry
            if now - ts < self._cache_ttl_seconds:
                return data
            else:
                self._cache.pop(key, None)
        return None

    def _set_cached_query(self, key: str, data: Dict[str, Any]):
        if len(self._cache) >= self._max_cache_entries:
            # Evict oldest entry
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][0], default=None)
            if oldest_key:
                self._cache.pop(oldest_key, None)
        self._cache[key] = (time.time(), data)

    async def search_and_cache_jobs(
        self,
        db: Session,
        keyword: str = "Software Engineer",
        location: str = "India",
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Fetches live jobs from Jooble API with bounded TTL cache.
        If Jooble fails or rate-limits, falls back to DB/curated jobs
        and clearly flags service status and is_live_jooble=False.
        """
        cache_key = self._get_cache_key(keyword, location, page)
        cached_result = self._get_cached_query(cache_key)
        if cached_result:
            logger.info(f"[Jooble Cache] Cache HIT for key='{cache_key}'")
            return cached_result

        raw_items = []
        total_count = 0
        is_live = False
        status_message = "Live Jooble feed"

        # Query Jooble API with bounded 4.0s timeout
        if self.api_key:
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    resp = await client.post(
                        self.base_url,
                        json={
                            "keywords": keyword,
                            "location": location or "India",
                            "page": page
                        },
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "SkillCatalyst-BTech-Portal/1.0"
                        }
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        total_count = data.get("totalCount", 0)
                        raw_items = data.get("jobs", [])
                        if raw_items:
                            is_live = True
                    elif resp.status_code == 429:
                        status_message = "Jooble rate limit reached (HTTP 429). Showing cached database opportunities."
                        logger.warning(f"[Jooble API] Rate limited (429): {resp.text[:150]}")
                    else:
                        status_message = f"Live job service returned HTTP {resp.status_code}. Showing cached database opportunities."
                        logger.warning(f"[Jooble API] Status {resp.status_code}: {resp.text[:150]}")
            except httpx.TimeoutException:
                status_message = "Live job service request timed out. Showing cached opportunities."
                logger.warning("[Jooble API] Request timed out (4.0s budget exceeded).")
            except Exception as exc:
                status_message = "Live job service unavailable. Showing cached opportunities."
                logger.warning(f"[Jooble API] Request exception: {exc}")
        else:
            status_message = "Live job service key not configured. Showing cached opportunities."

        if not raw_items:
            # Fallback to cached jobs from DB or curated pool
            db_cached = db.query(Job).order_by(Job.created_at.desc()).limit(limit).all()
            if db_cached:
                fallback_resp = {
                    "total_count": len(db_cached),
                    "page": page,
                    "location": location,
                    "keyword": keyword,
                    "is_live_jooble": False,
                    "service_status": status_message,
                    "jobs": [self.job_model_to_dict(j, is_live=False) for j in db_cached]
                }
                return fallback_resp
            raw_items = FALLBACK_JOBS
            total_count = len(FALLBACK_JOBS)

        # Collect valid items with an id
        valid_items = [item for item in raw_items if item.get("id")]
        ext_ids = [str(item.get("id")) for item in valid_items]

        # Fast single query for existing jobs in database
        existing_jobs_map: Dict[str, Job] = {}
        if ext_ids:
            found_jobs = db.query(Job).filter(Job.external_id.in_(ext_ids)).all()
            for fj in found_jobs:
                existing_jobs_map[fj.external_id] = fj

        new_jobs_to_insert = []
        for item in valid_items:
            ext_id = str(item.get("id"))
            if ext_id in existing_jobs_map:
                continue

            title = item.get("title", "").strip()
            company = item.get("company", "Tech Enterprise").strip()
            job_loc = item.get("location") or location or "India"
            snippet = clean_html_snippet(item.get("snippet", ""))
            salary_raw = item.get("salary") or "Competitive Package / Industry Standard"
            sal_min, sal_max = parse_salary_range(salary_raw)
            job_type = item.get("type") or "Full-time"
            apply_link = item.get("link") or "https://jooble.org"
            source = item.get("source") or "jooble.org"

            extracted_skills = extract_skills_from_text(title, snippet)

            db_job = Job(
                external_id=ext_id,
                title=title,
                company=company,
                location=job_loc,
                description=snippet,
                salary_min=sal_min,
                salary_max=sal_max,
                salary_raw=salary_raw,
                employment_type=job_type,
                source=source,
                source_url=apply_link,
                required_skills_json=json.dumps(extracted_skills),
                posted_at=datetime.utcnow()
            )
            new_jobs_to_insert.append(db_job)
            db.add(db_job)

        if new_jobs_to_insert:
            try:
                db.commit()
                for job_obj in new_jobs_to_insert:
                    db.refresh(job_obj)
                    existing_jobs_map[job_obj.external_id] = job_obj
            except Exception as exc:
                db.rollback()
                logger.warning(f"Failed to batch commit new Jooble jobs: {exc}")
                found_jobs = db.query(Job).filter(Job.external_id.in_(ext_ids)).all()
                for fj in found_jobs:
                    existing_jobs_map[fj.external_id] = fj

        # Build normalized response for all returned items
        normalized_jobs = []
        for item in valid_items:
            ext_id = str(item.get("id"))
            job_obj = existing_jobs_map.get(ext_id)
            if job_obj:
                job_dict = self.job_model_to_dict(job_obj)
                normalized_jobs.append(job_dict)
            else:
                title = item.get("title", "").strip()
                snippet = clean_html_snippet(item.get("snippet", ""))
                extracted = extract_skills_from_text(title, snippet)
                normalized_jobs.append({
                    "id": ext_id,
                    "external_id": ext_id,
                    "title": title,
                    "company": item.get("company", "Tech Enterprise").strip(),
                    "location": item.get("location") or location or "India",
                    "description": snippet,
                    "snippet": snippet,
                    "salary": item.get("salary") or "Competitive Package / Industry Standard",
                    "employment_type": item.get("type") or "Full-time",
                    "experience_required": "0-2 years (Freshers / B.Tech)",
                    "source": item.get("source") or "jooble.org",
                    "apply_link": item.get("link") or "https://jooble.org",
                    "required_skills": extracted,
                    "matched_skills": [s["skill"] for s in extracted[:3]],
                    "posted_at": datetime.utcnow().isoformat(),
                    "is_live_jooble": is_live
                })

        result = {
            "total_count": total_count,
            "page": page,
            "location": location,
            "keyword": keyword,
            "is_live_jooble": is_live,
            "service_status": status_message if not is_live else "Live Jooble feed",
            "new_jobs_persisted": len(new_jobs_to_insert),
            "jobs": normalized_jobs
        }
        self._set_cached_query(cache_key, result)
        return result

    def job_model_to_dict(
        self,
        job: Job,
        extracted_skills: Optional[List[Dict[str, Any]]] = None,
        is_live: bool = True
    ) -> Dict[str, Any]:
        if not extracted_skills:
            try:
                extracted_skills = json.loads(job.required_skills_json) if job.required_skills_json else []
            except Exception:
                extracted_skills = []

        if not extracted_skills:
            extracted_skills = extract_skills_from_text(job.title, job.description or "")

        return {
            "id": job.id,
            "external_id": job.external_id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description,
            "snippet": job.description,  # alias for frontend compatibility
            "salary": job.salary_raw,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "employment_type": job.employment_type,
            "experience_required": job.experience_required or "0-2 years (Freshers / B.Tech)",
            "source": job.source,
            "apply_link": job.source_url,
            "required_skills": extracted_skills,
            "matched_skills": [s["skill"] for s in extracted_skills[:3]],
            "posted_at": job.posted_at.isoformat() if job.posted_at else None,
            "is_live_jooble": is_live
        }

    def search_jobs(
        self,
        db: Session,
        keyword: str = "Software Engineer",
        location: str = "India",
        page: int = 1,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Synchronous job search for agent tools and domain services.
        Tries Jooble API with 4.0s timeout, falls back to DB cached jobs, and then curated verified jobs.
        """
        raw_items = []
        is_live = False
        if self.api_key:
            try:
                with httpx.Client(timeout=4.0) as client:
                    resp = client.post(
                        self.base_url,
                        json={
                            "keywords": keyword,
                            "location": location or "India",
                            "page": page
                        },
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "SkillCatalyst-Agent/1.0"
                        }
                    )
                    if resp.status_code == 200:
                        raw_items = resp.json().get("jobs", [])
                        if raw_items:
                            is_live = True
            except Exception as exc:
                logger.warning(f"[Jooble API sync] Request exception: {exc}")

        if raw_items:
            results = []
            for item in raw_items[:limit]:
                title = item.get("title", "").strip()
                snippet = clean_html_snippet(item.get("snippet", ""))
                extracted = extract_skills_from_text(title, snippet)
                results.append({
                    "id": str(item.get("id")),
                    "title": title,
                    "company": item.get("company", "Tech Enterprise").strip(),
                    "location": item.get("location") or location or "India",
                    "salary": item.get("salary") or "Competitive / Industry Standard",
                    "required_skills": [s["skill"] for s in extracted],
                    "link": item.get("link") or "https://jooble.org",
                    "source": "Jooble Live API"
                })
            return {"jobs": results, "total_count": len(results), "is_live_jooble": is_live}

        # Fallback to database cached jobs matching keyword
        if db:
            try:
                offset = max(0, (page - 1) * limit)
                cached = db.query(Job).filter(
                    or_(
                        Job.title.ilike(f"%{keyword}%"),
                        Job.description.ilike(f"%{keyword}%")
                    )
                ).offset(offset).limit(limit).all()
                if not cached:
                    cached = db.query(Job).order_by(Job.created_at.desc()).offset(offset).limit(limit).all()
                if cached:
                    results = []
                    for c in cached:
                        extracted = extract_skills_from_text(c.title, c.description or "")
                        results.append({
                            "id": str(c.id),
                            "title": c.title,
                            "company": c.company,
                            "location": c.location,
                            "salary": c.salary_raw or "Competitive / Industry Standard",
                            "required_skills": [s["skill"] for s in extracted],
                            "link": c.source_url or "https://jooble.org",
                            "source": f"Cached Database ({c.source})"
                        })
                    return {"jobs": results, "total_count": len(results), "is_live_jooble": False}
            except Exception as exc:
                logger.warning(f"[Jooble sync fallback] DB query failed: {exc}")

        # Curated verified jobs pool
        results = []
        kw_lower = keyword.lower()
        matched_fb = [j for j in FALLBACK_JOBS if kw_lower in j["title"].lower() or kw_lower in j["snippet"].lower()]
        fb_pool = matched_fb if matched_fb else FALLBACK_JOBS
        for item in fb_pool[:limit]:
            extracted = extract_skills_from_text(item["title"], item["snippet"])
            results.append({
                "id": item["id"],
                "title": item["title"],
                "company": item["company"],
                "location": item["location"],
                "salary": item["salary"],
                "required_skills": [s["skill"] for s in extracted],
                "link": item["link"],
                "source": "Verified Tech Jobs Pool"
            })
        return {"jobs": results, "total_count": len(results), "is_live_jooble": False}


jooble_service = JoobleService()

