from typing import Dict, Any, List, Optional
from backend.app.tech_news.relevance import tech_news_relevance_engine, TechNewsRelevanceEngine


class TechNewsService:
    """
    Domain service for personalized tech news intelligence.
    """

    def __init__(self):
        self.relevance_engine = tech_news_relevance_engine

    def personalize_articles(
        self,
        articles: List[Dict[str, Any]],
        student_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Ranks news articles by relevance to the student profile and attaches related Skill Bits.
        """
        ranked = []
        for a in articles:
            rel = self.relevance_engine.compute_student_relevance(a, student_profile)
            ranked.append({
                "article": a,
                "relevance": rel
            })
        ranked.sort(key=lambda x: x["relevance"]["relevance_score"], reverse=True)
        return ranked


tech_news_service = TechNewsService()
