from typing import Dict, Any, List, Optional
from backend.app.learning.skill_bits import skill_bits_service
from backend.app.learning.learning_paths import learning_path_engine


TOPIC_SKILL_MAP: Dict[str, str] = {
    "openai": "Machine Learning",
    "chatgpt": "Machine Learning",
    "llm": "Machine Learning",
    "ai": "Machine Learning",
    "nvidia": "Machine Learning",
    "python": "Python",
    "react": "React",
    "web": "React",
    "frontend": "React",
    "fastapi": "FastAPI",
    "api": "FastAPI",
    "backend": "FastAPI",
    "docker": "Docker",
    "cloud": "Docker",
    "kubernetes": "Docker",
    "sql": "SQL",
    "database": "SQL",
    "data": "SQL"
}


class TechNewsRelevanceEngine:
    """
    Connects industry technology news directly to student learning:
    Tech News -> Student Relevance -> Related Skill -> Skill Bit -> Learning Path Action
    """

    def __init__(self):
        self.skill_bits = skill_bits_service
        self.learning_engine = learning_path_engine

    def identify_related_skill(self, text: str) -> Optional[str]:
        clean = (text or "").lower()
        for kw, skill in TOPIC_SKILL_MAP.items():
            if kw in clean:
                return skill
        return None

    def compute_student_relevance(
        self,
        article: Dict[str, Any],
        student_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates relevance of a news article to a student's profile (target role, skills, stage).
        """
        title = article.get("title", "")
        desc = article.get("description", "") or ""
        combined_text = f"{title} {desc}".lower()

        target_role = (student_profile.get("target_role") or "Software Engineer").lower()
        student_skills = [
            (s.get("skill_name") or s.get("name") or str(s)).lower()
            for s in student_profile.get("skills", [])
        ]
        interests = [
            (i if isinstance(i, str) else i.get("interest", "")).lower()
            for i in student_profile.get("interests", [])
        ]

        relevance_score = 40  # baseline general tech interest
        reasons = []

        # Target role alignment
        if any(w in combined_text for w in target_role.split()):
            relevance_score += 25
            reasons.append(f"Directly impacts your target role: '{target_role.title()}'.")

        # Student skill alignment
        matched_skills = [sk for sk in student_skills if sk in combined_text]
        if matched_skills:
            relevance_score += 20
            reasons.append(f"Involves technology in your skillset: {', '.join(s.title() for s in matched_skills)}.")

        # Student interest alignment
        matched_interests = [it for it in interests if it in combined_text]
        if matched_interests:
            relevance_score += 15
            reasons.append(f"Matches your stated career interest: {', '.join(it.title() for it in matched_interests)}.")

        relevance_score = min(98, relevance_score)

        # Connect to skill bit and learning path
        related_skill = self.identify_related_skill(combined_text) or "Python"
        skill_bit = self.skill_bits.get_skill_bits_for_skill(related_skill)

        return {
            "article_title": title,
            "article_url": article.get("url"),
            "published_at": article.get("publishedAt"),
            "relevance_score": relevance_score,
            "is_highly_relevant": relevance_score >= 70,
            "relevance_reasons": reasons if reasons else ["General industry technology update."],
            "related_skill": related_skill,
            "skill_bit": skill_bit,
            "learning_path_action": f"Review {related_skill} Skill Bit and incorporate into current project roadmap."
        }


tech_news_relevance_engine = TechNewsRelevanceEngine()
