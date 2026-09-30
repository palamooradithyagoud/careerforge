import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from backend.app.scholarships.eligibility_engine import ScholarshipEligibilityEngine
from backend.app.jobs.skill_gap import SkillGapAnalyzer
from backend.app.careers.pathway_engine import CareerPathwayEngine
from backend.app.ai.tools import AI_TOOLS, AIToolManager, ai_tool_manager
from backend.app.ai.rag import VectorRAG
from backend.app.ai.llm_orchestrator import LLMOrchestrator
from backend.app.tech_news.relevance import TechNewsRelevanceEngine
from backend.app.learning.learning_paths import LearningPathEngine


# ============================================================================
# 1. SCHOLARSHIP ELIGIBILITY ENGINE TESTS (Section 6)
# ============================================================================

@pytest.fixture
def eligibility_engine():
    return ScholarshipEligibilityEngine()


def test_scholarship_eligible_student(eligibility_engine):
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 85.0, "cgpa": 8.8},
        "financial_context": {"annual_family_income": 350000},
        "category": "OBC",
        "location": "Telangana"
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 500000,
        "eligible_categories": "OBC,SC,ST",
        "eligible_states": "Telangana,Andhra Pradesh",
        "status": "verified"
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is True
    assert res["criteria"]["academic"]["passed"] is True
    assert res["criteria"]["income"]["passed"] is True
    assert res["criteria"]["education_stage"]["passed"] is True
    assert res["criteria"]["category"]["passed"] is True
    assert res["criteria"]["domicile"]["passed"] is True


def test_scholarship_academic_failure(eligibility_engine):
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 68.0},
        "financial_context": {"annual_family_income": 200000}
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 500000
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["academic"]["passed"] is False
    assert res["criteria"]["income"]["passed"] is True


def test_scholarship_income_failure(eligibility_engine):
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 90.0},
        "financial_context": {"annual_family_income": 800000}
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 500000
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["income"]["passed"] is False


def test_scholarship_stage_mismatch(eligibility_engine):
    student = {
        "education_stage": "class_10",
        "academic_profile": {"percentage": 95.0}
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 70.0
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["education_stage"]["passed"] is False


def test_scholarship_category_mismatch(eligibility_engine):
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 88.0},
        "category": "general"
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 70.0,
        "eligible_categories": "sc,st"
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["category"]["passed"] is False


def test_scholarship_domicile_mismatch(eligibility_engine):
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 88.0},
        "location": "Karnataka"
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 70.0,
        "eligible_states": "Maharashtra"
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["domicile"]["passed"] is False


def test_scholarship_multiple_simultaneous_failures(eligibility_engine):
    student = {
        "education_stage": "class_10",
        "academic_profile": {"percentage": 55.0},
        "financial_context": {"annual_family_income": 900000},
        "location": "Delhi"
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 400000,
        "eligible_states": "Telangana"
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is False
    assert res["criteria"]["academic"]["passed"] is False
    assert res["criteria"]["income"]["passed"] is False
    assert res["criteria"]["education_stage"]["passed"] is False
    assert res["criteria"]["domicile"]["passed"] is False


def test_scholarship_boundary_values(eligibility_engine):
    # Exactly on cutoff boundary (score = 75.0, max_income = 500000)
    student = {
        "education_stage": "b_tech",
        "academic_profile": {"percentage": 75.0},
        "financial_context": {"annual_family_income": 500000}
    }
    scholarship = {
        "eligible_stages": "b_tech",
        "min_cgpa_or_percentage": 75.0,
        "max_income": 500000
    }
    res = eligibility_engine.check_eligibility(student, scholarship)
    assert res["eligible"] is True
    assert res["criteria"]["academic"]["passed"] is True
    assert res["criteria"]["income"]["passed"] is True


# ============================================================================
# 2. SKILL GAP ANALYZER TESTS (Section 8)
# ============================================================================

@pytest.fixture
def skill_gap_analyzer():
    return SkillGapAnalyzer()


def test_skill_gap_no_gap(skill_gap_analyzer):
    student_skills = [
        {"skill_name": "Python", "proficiency": "Advanced"},
        {"skill_name": "FastAPI", "proficiency": "Intermediate"}
    ]
    required_skills = [
        {"skill": "Python", "required_level": 3},
        {"skill": "FastAPI", "required_level": 3}
    ]
    res = skill_gap_analyzer.calculate_gap(student_skills, required_skills)
    assert res["coverage"] == 100.0
    assert len(res["matched_skills"]) == 2
    assert len(res["missing_skills"]) == 0
    assert len(res["priority_gaps"]) == 0
    assert res["readiness_status"] == "Ready to Apply"


def test_skill_gap_complete_gap(skill_gap_analyzer):
    student_skills = []
    required_skills = [
        {"skill": "Python", "required_level": 4, "importance": "high"},
        {"skill": "Docker", "required_level": 3, "importance": "medium"}
    ]
    res = skill_gap_analyzer.calculate_gap(student_skills, required_skills)
    assert res["coverage"] == 0.0
    assert len(res["matched_skills"]) == 0
    assert len(res["missing_skills"]) == 2
    assert len(res["priority_gaps"]) == 2
    assert res["readiness_status"] == "Significant Upskilling Needed"


def test_skill_gap_partial_overlap(skill_gap_analyzer):
    student_skills = [
        {"skill_name": "Python", "proficiency": "Beginner"}  # level 1
    ]
    required_skills = [
        {"skill": "Python", "required_level": 3, "importance": "high"}  # level 3
    ]
    res = skill_gap_analyzer.calculate_gap(student_skills, required_skills)
    assert len(res["partial_skills"]) == 1
    assert res["partial_skills"][0]["gap"] == 2
    assert res["coverage"] > 0.0
    assert len(res["priority_gaps"]) == 1


def test_skill_gap_case_normalization(skill_gap_analyzer):
    student_skills = [{"skill_name": "pYtHoN", "proficiency": "intermediate"}]
    required_skills = [{"skill": "PYTHON", "required_level": 3}]
    res = skill_gap_analyzer.calculate_gap(student_skills, required_skills)
    assert len(res["matched_skills"]) == 1
    assert res["coverage"] == 100.0


def test_skill_gap_duplicate_skills(skill_gap_analyzer):
    # Duplicate student skill with different proficiencies -> should select higher
    student_skills = [
        {"skill_name": "Python", "proficiency": "Beginner"},
        {"skill_name": "Python", "proficiency": "Advanced"}
    ]
    required_skills = [{"skill": "Python", "required_level": 4}]
    res = skill_gap_analyzer.calculate_gap(student_skills, required_skills)
    assert len(res["matched_skills"]) == 1
    assert res["matched_skills"][0]["student_level"] == 4


def test_skill_gap_empty_input(skill_gap_analyzer):
    res = skill_gap_analyzer.calculate_gap([], [])
    assert res["coverage"] == 100.0
    assert res["total_required"] == 0


def test_skill_gap_invalid_input(skill_gap_analyzer):
    res = skill_gap_analyzer.calculate_gap(None, None)
    assert isinstance(res, dict)
    assert "coverage" in res
    assert "matched_skills" in res


# ============================================================================
# 3. CAREER PATHWAY ENGINE TESTS (Section 7)
# ============================================================================

def test_career_comparison():
    engine = CareerPathwayEngine()
    res = engine.compare_career_pathways("ai_engineer", "software_engineer")
    assert "pathway_a" in res
    assert "pathway_b" in res
    assert res["pathway_a"]["name"] == "AI / Machine Learning Engineer"
    assert res["pathway_b"]["name"] == "Software Development Engineer (SDE / Full Stack)"


def test_salary_estimation():
    engine = CareerPathwayEngine()
    res = engine.get_salary_estimate("ai_engineer", "entry")
    assert res["matched_benchmark"] == "AI / Machine Learning Engineer"
    assert "entry_level_0_2_yrs" in res["experience_breakdown"]


def test_education_cost_calculation():
    engine = CareerPathwayEngine()
    res = engine.get_education_cost("b_tech", "government")
    assert res["standardized_degree"] == "Bachelor of Technology (B.Tech / B.E.)"
    assert "government_institutes" in res["institutional_tier_breakdown"]


def test_education_roi_calculation():
    engine = CareerPathwayEngine()
    res = engine.calculate_education_roi("b_tech", "ai_engineer", "government")
    assert "five_year_roi_multiplier" in res
    assert "estimated_payback_period_months" in res
    assert res["estimated_payback_period_months"] > 0


# ============================================================================
# 4. AI AGENT 9 TOOLS REGISTRY TESTS (Section 11)
# ============================================================================

def test_ai_tools_registration():
    expected_tools = {
        "getEducationCost",
        "getSalaryEstimate",
        "calculateEducationROI",
        "compareCareerPathways",
        "findEligibleScholarships",
        "checkScholarshipEligibility",
        "calculateSkillGap",
        "searchJobs",
        "searchKnowledgeBase"
    }
    assert expected_tools.issubset(set(AI_TOOLS.keys()))


def test_ai_tools_selection():
    manager = AIToolManager()
    tool = manager.get_tool("getSalaryEstimate")
    assert tool is not None
    assert callable(tool)


def test_ai_tools_valid_execution():
    manager = AIToolManager()
    res = manager.execute("getSalaryEstimate", {"career_name": "ai_engineer"})
    assert res["success"] is True
    assert "data" in res


def test_ai_tools_invalid_tool_handling():
    manager = AIToolManager()
    res = manager.execute("nonExistentFakeTool", {})
    assert res["success"] is False
    assert "Unknown tool" in res["error"]


def test_ai_tools_failure_handling():
    manager = AIToolManager()
    # Mock a tool that raises an exception
    def broken_tool(args):
        raise ValueError("Simulated database timeout")
    manager.register_tool("brokenTool", broken_tool)
    res = manager.execute("brokenTool", {})
    assert res["success"] is False
    assert "Simulated database timeout" in res["error"]


# ============================================================================
# 5. VECTOR RAG TESTS (Section 12)
# ============================================================================

def test_vector_rag_retrieval():
    rag = VectorRAG()
    # Query knowledge base
    results = rag.retrieve("scholarship eligibility requirements", top_k=2)
    assert isinstance(results, list)


def test_vector_rag_empty_retrieval():
    rag = VectorRAG()
    results = rag.retrieve("")
    assert results == []


def test_vector_rag_malformed_documents():
    rag = VectorRAG()
    malformed = [
        {"unexpected_key": "some value"},
        "plain text document",
        None
    ]
    # Should not raise exception
    context = rag.build_context([m for m in malformed if m is not None])
    assert isinstance(context, str)
    assert "UNTRUSTED DATA" in context


def test_vector_rag_context_construction():
    rag = VectorRAG()
    docs = [
        {
            "chunk_id": "test_chunk_1",
            "content": "Official guidelines mandate 75% for merit eligibility.",
            "title": "State Scholarship Norms",
            "publisher": "Govt Dept",
            "score": 0.88,
            "source_url": "https://gov.in"
        }
    ]
    context = rag.build_context(docs)
    assert "UNTRUSTED DATA" in context
    assert "State Scholarship Norms" in context
    assert "Official guidelines mandate" in context


def test_vector_rag_retrieval_failure_handling():
    rag = VectorRAG()
    with patch("backend.app.ai.rag.search_knowledge_base", side_effect=RuntimeError("Chroma offline")):
        res = rag.retrieve("any query")
        assert res == []


# ============================================================================
# 6. MULTI-LLM ORCHESTRATION TESTS (Section 13)
# ============================================================================

@pytest.mark.anyio
async def test_llm_orchestrator_deterministic_fallback():
    orchestrator = LLMOrchestrator()
    # When keys are unset or fail, deterministic fallback is executed
    with patch("backend.app.core.config.settings.GROQ_API_KEY", ""):
        with patch("backend.app.core.config.settings.GEMINI_API_KEY", ""):
            res = await orchestrator.generate("What is the cost and ROI of B.Tech?")
            assert res["success"] is True
            assert res["provider"] == "deterministic_fallback"
            assert "tuition" in res["text"].lower() or "roi" in res["text"].lower()


@pytest.mark.anyio
async def test_llm_orchestrator_timeout():
    orchestrator = LLMOrchestrator(primary_timeout_sec=0.01)
    # Primary timeout triggers fallback gracefully
    with patch("backend.app.core.config.settings.GROQ_API_KEY", "mock_key"):
        with patch("groq.AsyncGroq") as mock_groq:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(side_effect=TimeoutError("Connection timed out"))
            mock_groq.return_value = mock_client

            res = await orchestrator.generate("Tell me about scholarships")
            assert res["success"] is True
            # Should have fallen back
            assert res["provider"] in ("gemini", "deterministic_fallback")


@pytest.mark.anyio
async def test_llm_orchestrator_rate_limit():
    orchestrator = LLMOrchestrator()
    with patch("backend.app.core.config.settings.GROQ_API_KEY", "mock_key"):
        with patch("groq.AsyncGroq") as mock_groq:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(side_effect=Exception("Rate limit 429 exceeded"))
            mock_groq.return_value = mock_client

            res = await orchestrator.generate("Skill gap guidance")
            assert res["success"] is True
            assert res["provider"] in ("gemini", "deterministic_fallback")


# ============================================================================
# 7. TECH NEWS RELEVANCE & LEARNING TESTS (Section 15)
# ============================================================================

def test_tech_news_relevance_and_skill_connection():
    engine = TechNewsRelevanceEngine()
    article = {
        "title": "OpenAI releases new ChatGPT reasoning model using advanced Python orchestration",
        "description": "Deep learning architectures demand high-performance API design.",
        "url": "https://techcrunch.com/article",
        "publishedAt": "2026-03-30T10:00:00Z"
    }
    student_profile = {
        "target_role": "AI Engineer",
        "skills": [{"skill_name": "Python", "proficiency": "Intermediate"}],
        "interests": ["Machine Learning"]
    }
    rel = engine.compute_student_relevance(article, student_profile)
    assert rel["is_highly_relevant"] is True
    assert rel["relevance_score"] >= 70
    assert rel["related_skill"] in ("Python", "Machine Learning")
    assert "skill_bit" in rel
    assert "learning_path_action" in rel
