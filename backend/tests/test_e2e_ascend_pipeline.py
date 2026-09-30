import pytest
from backend.app.careers.pathway_engine import CareerPathwayEngine
from backend.app.jobs.skill_gap import SkillGapAnalyzer
from backend.app.learning.learning_paths import LearningPathEngine
from backend.app.jobs.job_search import JobSearchService
from backend.app.scholarships.eligibility_engine import ScholarshipEligibilityEngine


def test_end_to_end_ascend_product_journey():
    """
    CRITICAL INTEGRATION TEST (Section 16):
    Demonstrates the complete end-to-end ASCEND student intelligence pipeline:
    Student Profile -> Career Goal -> Skill Gap -> Learning Path -> Job Opportunity -> Scholarship Eligibility
    Executes real services across all domain layers.
    """
    # ------------------------------------------------------------------------
    # STEP 1: Student Profile
    # ------------------------------------------------------------------------
    student_profile = {
        "student_id": "test_student_pipeline_001",
        "name": "Priya Sharma",
        "education_stage": "b_tech",
        "target_role": "AI Engineer",
        "academic_profile": {
            "branch": "Computer Science & Engineering",
            "year": "3rd Year",
            "cgpa": 8.5,
            "percentage": 80.75
        },
        "financial_context": {
            "annual_family_income": 350000,
            "education_budget": "100000"
        },
        "skills": [
            {"skill_name": "Python", "proficiency": "Intermediate"},
            {"skill_name": "SQL", "proficiency": "Beginner"}
        ],
        "category": "OBC",
        "location": "Telangana"
    }

    assert student_profile["target_role"] == "AI Engineer"
    assert len(student_profile["skills"]) == 2

    # ------------------------------------------------------------------------
    # STEP 2: Career Pathway Intelligence
    # ------------------------------------------------------------------------
    career_engine = CareerPathwayEngine()
    career_goal = student_profile["target_role"]

    salary_intel = career_engine.get_salary_estimate(career_goal, experience_level="entry")
    assert salary_intel["matched_benchmark"] == "AI / Machine Learning Engineer"
    assert "entry_level_0_2_yrs" in salary_intel["experience_breakdown"]

    roi_intel = career_engine.calculate_education_roi("b_tech", career_goal, college_tier="government")
    assert roi_intel["total_education_investment_inr"] > 0
    assert roi_intel["estimated_payback_period_months"] < 36
    assert "five_year_roi_multiplier" in roi_intel

    # ------------------------------------------------------------------------
    # STEP 3: Skill Gap Analysis
    # ------------------------------------------------------------------------
    skill_analyzer = SkillGapAnalyzer()
    required_role_skills = [
        {"skill": "Python", "required_level": 4, "importance": "critical"},
        {"skill": "Machine Learning", "required_level": 3, "importance": "critical"},
        {"skill": "FastAPI", "required_level": 3, "importance": "high"},
        {"skill": "Docker", "required_level": 3, "importance": "high"},
        {"skill": "SQL", "required_level": 3, "importance": "medium"},
    ]

    gap_analysis = skill_analyzer.calculate_gap(student_profile["skills"], required_role_skills)
    assert 0.0 < gap_analysis["coverage"] < 100.0
    assert gap_analysis["readiness_status"] in ("Minor Gaps", "Significant Upskilling Needed")
    assert len(gap_analysis["missing_skills"]) >= 2  # Machine Learning, FastAPI, Docker
    assert any(p["skill"] in ("Machine Learning", "FastAPI", "Docker") for p in gap_analysis["priority_gaps"])

    # ------------------------------------------------------------------------
    # STEP 4: Learning Path Generation
    # ------------------------------------------------------------------------
    learning_engine = LearningPathEngine()
    learning_path = learning_engine.generate_learning_path(
        target_career=career_goal,
        student_skills=student_profile["skills"],
        custom_required_skills=required_role_skills
    )

    assert len(learning_path["learning_modules"]) > 0
    module_1 = learning_path["learning_modules"][0]
    assert module_1["sequence"] == 1
    assert "learning_resource" in module_1
    assert "skill_bit" in module_1
    assert module_1["learning_resource"]["source"] == "YouTube (Verified Tutorial)"

    # ------------------------------------------------------------------------
    # STEP 5: Job Opportunity Connection
    # ------------------------------------------------------------------------
    job_service = JobSearchService()
    job_results = job_service.search_jobs("AI Engineer", location="India", result_count=5)
    assert job_results["total_found"] > 0
    assert "jobs" in job_results

    first_job = job_results["jobs"][0]
    assert "title" in first_job
    assert "company" in first_job
    assert "provenance" in first_job  # live_jooble_api or curated_database_fallback

    # ------------------------------------------------------------------------
    # STEP 6: Scholarship Eligibility Engine
    # ------------------------------------------------------------------------
    scholarship_engine = ScholarshipEligibilityEngine()
    scholarship = {
        "id": "telangana_merit_fellowship_2026",
        "title": "Telangana State Engineering Excellence Grant",
        "provider": "Department of Higher Education",
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 500000,
        "eligible_categories": "OBC,SC,ST,General",
        "eligible_states": "Telangana,Andhra Pradesh",
        "status": "verified"
    }

    eligibility = scholarship_engine.check_eligibility(student_profile, scholarship)
    assert eligibility["eligible"] is True
    assert eligibility["criteria"]["academic"]["passed"] is True
    assert eligibility["criteria"]["income"]["passed"] is True
    assert eligibility["criteria"]["education_stage"]["passed"] is True
    assert eligibility["criteria"]["category"]["passed"] is True
    assert eligibility["criteria"]["domicile"]["passed"] is True

    # Complete pipeline assertion
    pipeline_summary = {
        "student": student_profile["name"],
        "target": career_goal,
        "salary_benchmark_median": salary_intel["experience_breakdown"]["entry_level_0_2_yrs"]["median"],
        "coverage": gap_analysis["coverage"],
        "top_missing_skill": learning_path["learning_modules"][0]["skill"],
        "jobs_matched": job_results["total_found"],
        "scholarship_eligible": eligibility["eligible"]
    }
    assert pipeline_summary["student"] == "Priya Sharma"
    assert pipeline_summary["scholarship_eligible"] is True
