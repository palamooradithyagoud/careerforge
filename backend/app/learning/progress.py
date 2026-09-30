from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class LearningProgressTracker:
    """
    Domain tracker for student milestone completion, hours logged, and learning trajectory.
    """

    def calculate_progress_summary(
        self,
        completed_milestones: int,
        total_milestones: int,
        completed_lectures: int = 0,
        total_lectures: int = 0
    ) -> Dict[str, Any]:
        tot_m = max(1, total_milestones)
        milestone_pct = round((completed_milestones / tot_m) * 100.0, 1)

        lecture_pct = 0.0
        if total_lectures > 0:
            lecture_pct = round((completed_lectures / total_lectures) * 100.0, 1)

        overall = round((milestone_pct * 0.6) + (lecture_pct * 0.4), 1) if total_lectures > 0 else milestone_pct

        return {
            "completed_milestones": completed_milestones,
            "total_milestones": total_milestones,
            "milestone_completion_rate": f"{milestone_pct}%",
            "completed_lectures": completed_lectures,
            "total_lectures": total_lectures,
            "lecture_completion_rate": f"{lecture_pct}%",
            "overall_progress_percentage": min(100.0, overall),
            "status": "Completed" if overall >= 100.0 else ("In Progress" if overall > 0 else "Not Started"),
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }


learning_progress_tracker = LearningProgressTracker()
