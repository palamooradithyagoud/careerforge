import logging
from typing import Dict, Any, Callable, Optional
from sqlalchemy.orm import Session

from backend.app.services.agent.tool_executor import (
    _execute_get_education_cost,
    _execute_get_salary_estimate,
    _execute_calculate_education_roi,
    _execute_compare_career_pathways,
    _execute_find_eligible_scholarships,
    _execute_check_scholarship_eligibility,
    _execute_calculate_skill_gap,
    _execute_search_jobs,
    _execute_search_knowledge_base,
    execute_agent_tool
)
from backend.app.services.agent.agent_context import AgentContext

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# 9 Canonical AI Tool Wrappers
# ----------------------------------------------------------------------------

def get_education_cost(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_get_education_cost(args)


def get_salary_estimate(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_get_salary_estimate(args)


def calculate_education_roi(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_calculate_education_roi(args)


def compare_career_pathways(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_compare_career_pathways(args)


def find_eligible_scholarships(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    ctx = context or AgentContext(request_id="ai_tool_call")
    return _execute_find_eligible_scholarships(args, ctx, db)


def check_scholarship_eligibility(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    ctx = context or AgentContext(request_id="ai_tool_call")
    return _execute_check_scholarship_eligibility(args, ctx, db)


def calculate_skill_gap(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    ctx = context or AgentContext(request_id="ai_tool_call")
    return _execute_calculate_skill_gap(args, ctx, db)


def search_jobs(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_search_jobs(args, db)


def search_knowledge_base(args: Dict[str, Any], context: Optional[AgentContext] = None, db: Optional[Session] = None) -> Dict[str, Any]:
    return _execute_search_knowledge_base(args)


# ----------------------------------------------------------------------------
# Canonical AI Tools Registry
# ----------------------------------------------------------------------------

AI_TOOLS: Dict[str, Callable[..., Dict[str, Any]]] = {
    "getEducationCost": get_education_cost,
    "getSalaryEstimate": get_salary_estimate,
    "calculateEducationROI": calculate_education_roi,
    "compareCareerPathways": compare_career_pathways,
    "findEligibleScholarships": find_eligible_scholarships,
    "checkScholarshipEligibility": check_scholarship_eligibility,
    "calculateSkillGap": calculate_skill_gap,
    "searchJobs": search_jobs,
    "searchKnowledgeBase": search_knowledge_base,
}


class AIToolManager:
    """
    Manager for registering, selecting, and safely executing AI tools.
    """

    def __init__(self, registry: Optional[Dict[str, Callable]] = None):
        self._tools: Dict[str, Callable] = dict(registry or AI_TOOLS)

    def register_tool(self, name: str, func: Callable):
        self._tools[name] = func

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def execute(
        self,
        tool_name: str,
        args: Dict[str, Any],
        context: Optional[AgentContext] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Executes a registered AI tool with validation, error isolation, and structured reporting.
        """
        if tool_name not in self._tools:
            return {
                "success": False,
                "error": f"Unknown tool '{tool_name}'. Available tools: {list(self._tools.keys())}",
                "tool_name": tool_name
            }

        tool_fn = self._tools[tool_name]
        try:
            # Inspect tool function params and invoke safely
            import inspect
            sig = inspect.signature(tool_fn)
            params = sig.parameters

            kwargs = {}
            if "context" in params:
                kwargs["context"] = context
            if "db" in params:
                kwargs["db"] = db

            result = tool_fn(args, **kwargs)
            return {
                "success": True,
                "tool_name": tool_name,
                "data": result
            }
        except Exception as exc:
            logger.error(f"[AIToolManager] Tool '{tool_name}' failed during execution: {exc}", exc_info=True)
            return {
                "success": False,
                "error": f"Tool '{tool_name}' execution error: {str(exc)}",
                "tool_name": tool_name
            }


ai_tool_manager = AIToolManager()
