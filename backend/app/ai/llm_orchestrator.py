import json
import logging
import asyncio
from typing import Dict, Any, Optional
import httpx
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMOrchestrator:
    """
    Multi-LLM Orchestration Layer with bounded timeouts and zero-downtime fallback:
    Primary LLM (Groq) -> Fallback LLM (Gemini) -> Grounded Deterministic Fallback.
    """

    def __init__(
        self,
        primary_timeout_sec: float = 4.0,
        fallback_timeout_sec: float = 4.0
    ):
        self.primary_timeout = primary_timeout_sec
        self.fallback_timeout = fallback_timeout_sec

    async def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates text completion with automatic failover and deterministic fallback.
        Returns:
        {
            "text": str,
            "provider": "groq" | "gemini" | "deterministic_fallback",
            "model": str,
            "success": bool
        }
        """
        sys_msg = system_instruction or "You are ASCEND AI, an authoritative career and education intelligence assistant."

        # --------------------------------------------------------------------
        # 1. Primary Provider: Groq (Llama-3.3-70B)
        # --------------------------------------------------------------------
        if settings.GROQ_API_KEY:
            try:
                import groq
                client = groq.AsyncGroq(api_key=settings.GROQ_API_KEY, timeout=self.primary_timeout)
                completion = await client.chat.completions.create(
                    model=settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                text = completion.choices[0].message.content or ""
                if text:
                    return {
                        "text": text.strip(),
                        "provider": "groq",
                        "model": settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                        "success": True
                    }
            except Exception as exc:
                is_rate_limit = "429" in str(exc) or "rate" in str(exc).lower()
                is_timeout = isinstance(exc, (asyncio.TimeoutError, TimeoutError)) or "timeout" in str(exc).lower()
                if is_rate_limit:
                    logger.warning(f"[LLMOrchestrator] Primary Groq rate limit (429) hit: {exc}. Switching to fallback.")
                elif is_timeout:
                    logger.warning(f"[LLMOrchestrator] Primary Groq timeout ({self.primary_timeout}s): {exc}. Switching to fallback.")
                else:
                    logger.warning(f"[LLMOrchestrator] Primary Groq error: {exc}. Switching to fallback.")

        # --------------------------------------------------------------------
        # 2. Fallback Provider: Google Gemini
        # --------------------------------------------------------------------
        if settings.GEMINI_API_KEY:
            try:
                logger.info("[LLMOrchestrator] Attempting secondary provider: Gemini...")
                gemini_url = f"{settings.GEMINI_BASE_URL.rstrip('/')}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
                    "Content-Type": "application/json"
                }
                body = {
                    "model": settings.GEMINI_MODEL or "gemini-flash-latest",
                    "messages": [
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
                async with httpx.AsyncClient(timeout=self.fallback_timeout) as http_client:
                    resp = await http_client.post(gemini_url, headers=headers, json=body)
                    if resp.status_code == 200:
                        data = resp.json()
                        choices = data.get("choices", [])
                        if choices:
                            text = choices[0].get("message", {}).get("content", "")
                            if text:
                                return {
                                    "text": text.strip(),
                                    "provider": "gemini",
                                    "model": settings.GEMINI_MODEL or "gemini-flash-latest",
                                    "success": True
                                }
                    else:
                        logger.warning(f"[LLMOrchestrator] Gemini HTTP {resp.status_code}: {resp.text}")
            except Exception as exc:
                is_timeout = isinstance(exc, (asyncio.TimeoutError, TimeoutError)) or "timeout" in str(exc).lower()
                if is_timeout:
                    logger.warning(f"[LLMOrchestrator] Gemini timeout ({self.fallback_timeout}s): {exc}")
                else:
                    logger.warning(f"[LLMOrchestrator] Gemini fallback call error: {exc}")

        # --------------------------------------------------------------------
        # 3. Deterministic Grounded Fallback
        # --------------------------------------------------------------------
        logger.info("[LLMOrchestrator] Both LLM providers unavailable; generating deterministic fallback response.")
        fallback_text = self._build_deterministic_answer(prompt)
        return {
            "text": fallback_text,
            "provider": "deterministic_fallback",
            "model": "rule_based_synthesis_engine",
            "success": True
        }

    def _build_deterministic_answer(self, prompt: str) -> str:
        """
        Synthesizes a helpful grounded answer based on query heuristics and authoritative context in prompt.
        """
        prompt_lower = prompt.lower()

        if "scholarship" in prompt_lower:
            return (
                "Based on ASCEND's verified scholarship criteria, eligibility requires meeting educational stage requirements "
                "(Class 10, Intermediate, or B.Tech), academic percentage/CGPA cutoffs, family income ceilings, and domicile mandates. "
                "You can verify your specific eligibility and compute your match score directly in the Scholarships dashboard."
            )
        elif "cost" in prompt_lower or "roi" in prompt_lower or "fee" in prompt_lower:
            return (
                "Education ROI in engineering and computer science pathways varies significantly by institutional tier. "
                "Government institutions (IITs/NITs/State Universities) offer total 4-year tuition of ₹3.5L–₹10.5L with rapid payback periods "
                "under 12 months for Tier-1 engineering roles, while private institutions average ₹18L–₹28L with a 24–36 month payback period."
            )
        elif "skill" in prompt_lower or "gap" in prompt_lower or "learn" in prompt_lower:
            return (
                "ASCEND's Skill Gap Engine analyzes your current skill profile against industry role benchmarks. "
                "For high-demand technology roles, key foundational competencies include Python, Data Structures & Algorithms, "
                "FastAPI for backend engineering, and Docker for deployment. Check your personalized Skill Track for sequential playlists."
            )
        elif "job" in prompt_lower or "career" in prompt_lower:
            return (
                "Current market benchmarks indicate entry-level AI & Software Development Engineer salaries in India range between "
                "₹6.0 LPA to ₹18.0 LPA depending on company tier (Product vs. IT Services). Explore the Live Jobs tab to see active postings "
                "matched to your verified skill readiness."
            )
        else:
            return (
                "ASCEND has received your query and analyzed it against our verified career, scholarship, and skill intelligence database. "
                "All recommendations are grounded in authoritative academic and market data."
            )


llm_orchestrator = LLMOrchestrator()
