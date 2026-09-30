from typing import Dict, Any, List, Optional
from backend.app.jobs.skill_gap import skill_gap_analyzer, SkillGapAnalyzer
from backend.app.learning.skill_bits import skill_bits_service
from backend.app.services.agent.tool_executor import CURATED_LEARNING_COURSES


# Canonical skill requirements for top career pathways in ASCEND
CAREER_REQUIRED_SKILLS: Dict[str, List[Dict[str, Any]]] = {
    "ai_engineer": [
        {"skill": "Python", "required_level": 4, "importance": "critical"},
        {"skill": "Machine Learning", "required_level": 3, "importance": "critical"},
        {"skill": "FastAPI", "required_level": 3, "importance": "high"},
        {"skill": "Docker", "required_level": 3, "importance": "high"},
        {"skill": "SQL", "required_level": 3, "importance": "medium"},
    ],
    "software_engineer": [
        {"skill": "Python", "required_level": 3, "importance": "high"},
        {"skill": "FastAPI", "required_level": 3, "importance": "high"},
        {"skill": "React", "required_level": 3, "importance": "high"},
        {"skill": "SQL", "required_level": 3, "importance": "high"},
        {"skill": "Data Structures", "required_level": 4, "importance": "critical"},
    ],
    "data_scientist": [
        {"skill": "Python", "required_level": 4, "importance": "critical"},
        {"skill": "Machine Learning", "required_level": 3, "importance": "high"},
        {"skill": "SQL", "required_level": 4, "importance": "critical"},
        {"skill": "Data Structures", "required_level": 3, "importance": "medium"},
    ]
}


class LearningPathEngine:
    """
    Learning Path Engine implementing the core ASCEND sequence:
    Target Career / Job -> Required Skills -> Student Skills -> SkillGapAnalyzer -> Missing Skills -> Learning Resources & Skill Bits.
    """

    def __init__(self):
        self.gap_analyzer = skill_gap_analyzer
        self.skill_bits = skill_bits_service
        self.curated_courses = CURATED_LEARNING_COURSES

    def get_course_for_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        norm = skill_name.strip().lower().replace(" ", "_").replace(".", "")
        for k, v in self.curated_courses.items():
            if k in norm or norm in k:
                return v
        return {
            "title": f"{skill_name.title()} Complete Technical Tutorial",
            "channel_title": "freeCodeCamp.org / Official Docs",
            "embed_url": "https://www.youtube-nocookie.com/embed/videoseries",
            "source": "Verified Technical Resource"
        }

    def generate_learning_path(
        self,
        target_career: str,
        student_skills: Optional[List[Any]] = None,
        custom_required_skills: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        End-to-end learning path generation connected to student skill gaps.
        """
        clean_target = (target_career or "software_engineer").strip().lower().replace(" ", "_")
        matched_target = "software_engineer"
        for k in CAREER_REQUIRED_SKILLS.keys():
            if k in clean_target or clean_target in k:
                matched_target = k
                break

        required = custom_required_skills or CAREER_REQUIRED_SKILLS.get(matched_target, CAREER_REQUIRED_SKILLS["software_engineer"])
        stud_skills = student_skills or []

        # 1. Calculate Skill Gap
        gap_result = self.gap_analyzer.calculate_gap(stud_skills, required)

        # 2. Extract Missing & Partial Skills needing learning
        target_skills_to_learn = []
        for p in gap_result["priority_gaps"]:
            target_skills_to_learn.append(p["skill"])

        # Deduplicate
        seen = set()
        deduped_skills = []
        for s in target_skills_to_learn:
            if s.lower() not in seen:
                seen.add(s.lower())
                deduped_skills.append(s)

        # 3. Assemble Sequential Learning Modules with Verified Courses & Skill Bits
        learning_modules = []
        for idx, skill_name in enumerate(deduped_skills, start=1):
            course = self.get_course_for_skill(skill_name)
            bits = self.skill_bits.get_skill_bits_for_skill(skill_name)

            learning_modules.append({
                "sequence": idx,
                "skill": skill_name,
                "priority": "High" if idx <= 2 else "Medium",
                "learning_resource": course,
                "skill_bit": bits,
                "actionable_milestone": f"Complete {skill_name} core project and verify in portfolio."
            })

        return {
            "target_career": target_career,
            "readiness_status": gap_result["readiness_status"],
            "coverage_percentage": gap_result["coverage"],
            "matched_skills_count": len(gap_result["matched_skills"]),
            "gap_skills_count": len(deduped_skills),
            "priority_gaps": gap_result["priority_gaps"],
            "learning_modules": learning_modules,
            "next_best_action": f"Begin Module 1: {deduped_skills[0]}" if deduped_skills else "Ready to Apply!"
        }


learning_path_engine = LearningPathEngine()
