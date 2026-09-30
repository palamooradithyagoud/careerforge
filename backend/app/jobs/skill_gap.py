from typing import List, Dict, Any, Union, Optional
from backend.app.services.skill_taxonomy import normalize_skill

PROFICIENCY_MAP = {
    "beginner": 1,
    "basic": 2,
    "intermediate": 3,
    "advanced": 4,
    "expert": 5
}

REVERSE_PROFICIENCY_MAP = {
    1: "Beginner",
    2: "Basic",
    3: "Intermediate",
    4: "Advanced",
    5: "Expert"
}


def parse_proficiency_level(prof: Any) -> int:
    if isinstance(prof, int):
        return max(1, min(5, prof))
    if isinstance(prof, str):
        clean = prof.strip().lower()
        return PROFICIENCY_MAP.get(clean, 3)
    return 3


class SkillGapAnalyzer:
    """
    Deterministic domain analyzer for comparing student skills against career/job requirements.
    Identifies matched skills, missing skills, partial gaps, coverage, and priority gaps.
    """

    def calculate_gap(
        self,
        student_skills: Union[List[Any], Any],
        required_skills: Union[List[Any], Any]
    ) -> Dict[str, Any]:
        """
        Calculates deterministic skill gap.
        Gracefully handles empty inputs, invalid types, duplicates, and case differences.
        """
        # 1. Validate inputs
        if not isinstance(student_skills, list):
            student_skills = [] if student_skills is None else [student_skills]
        if not isinstance(required_skills, list):
            required_skills = [] if required_skills is None else [required_skills]

        # 2. Normalize and deduplicate student skills (keep highest proficiency)
        normalized_student_skills: Dict[str, Dict[str, Any]] = {}
        for sk in student_skills:
            if not sk:
                continue
            if isinstance(sk, str):
                raw_name = sk.strip()
                level = 3
            elif isinstance(sk, dict):
                raw_name = (sk.get("skill_name") or sk.get("name") or sk.get("skill") or "").strip()
                level = parse_proficiency_level(sk.get("proficiency") or sk.get("level") or 3)
            else:
                raw_name = str(sk).strip()
                level = 3

            if not raw_name:
                continue

            norm = normalize_skill(raw_name)
            norm_key = norm["normalized_name"]

            if norm_key not in normalized_student_skills or level > normalized_student_skills[norm_key]["level"]:
                normalized_student_skills[norm_key] = {
                    "name": norm["name"],
                    "normalized_name": norm_key,
                    "category": norm["category"],
                    "level": level,
                    "level_label": REVERSE_PROFICIENCY_MAP.get(level, "Intermediate")
                }

        # 3. Normalize and deduplicate required skills
        normalized_required: Dict[str, Dict[str, Any]] = {}
        for req in required_skills:
            if not req:
                continue
            if isinstance(req, str):
                req_name = req.strip()
                req_level = 3
                importance = "medium"
            elif isinstance(req, dict):
                req_name = (req.get("skill") or req.get("name") or req.get("skill_name") or "").strip()
                req_level = parse_proficiency_level(req.get("required_proficiency") or req.get("required_level") or req.get("level") or 3)
                importance = req.get("importance", "medium")
            else:
                req_name = str(req).strip()
                req_level = 3
                importance = "medium"

            if not req_name:
                continue

            norm = normalize_skill(req_name)
            req_key = norm["normalized_name"]

            # Keep highest required level if duplicate in requirement list
            if req_key not in normalized_required or req_level > normalized_required[req_key]["required_level"]:
                normalized_required[req_key] = {
                    "skill": norm["name"],
                    "normalized_skill": req_key,
                    "category": norm["category"],
                    "required_level": req_level,
                    "required_level_label": REVERSE_PROFICIENCY_MAP.get(req_level, "Intermediate"),
                    "importance": importance
                }

        matched_skills = []
        partial_skills = []
        missing_skills = []
        priority_gaps = []

        total_req_count = len(normalized_required)

        # 4. Compare student skills against required skills
        for req_key, req_data in normalized_required.items():
            req_display = req_data["skill"]
            req_level = req_data["required_level"]
            req_label = req_data["required_level_label"]
            importance = req_data["importance"]

            if req_key in normalized_student_skills:
                student_sk = normalized_student_skills[req_key]
                student_level = student_sk["level"]
                student_label = student_sk["level_label"]

                if student_level >= req_level:
                    matched_skills.append({
                        "skill": req_display,
                        "normalized_skill": req_key,
                        "student_level": student_level,
                        "student_level_label": student_label,
                        "required_level": req_level,
                        "required_level_label": req_label,
                        "importance": importance
                    })
                else:
                    gap = req_level - student_level
                    partial_item = {
                        "skill": req_display,
                        "normalized_skill": req_key,
                        "student_level": student_level,
                        "student_level_label": student_label,
                        "required_level": req_level,
                        "required_level_label": req_label,
                        "gap": gap,
                        "importance": importance
                    }
                    partial_skills.append(partial_item)
                    priority_gaps.append({
                        "skill": req_display,
                        "type": "partial",
                        "gap": gap,
                        "importance": importance,
                        "recommendation": f"Advance {req_display} from {student_label} to {req_label}."
                    })
            else:
                missing_item = {
                    "skill": req_display,
                    "normalized_skill": req_key,
                    "required_level": req_level,
                    "required_level_label": req_label,
                    "importance": importance
                }
                missing_skills.append(missing_item)
                priority_gaps.append({
                    "skill": req_display,
                    "type": "missing",
                    "gap": req_level,
                    "importance": importance,
                    "recommendation": f"Learn {req_display} up to {req_label} level."
                })

        # Sort priority gaps: high importance first, then largest gap
        importance_weight = {"critical": 3, "high": 2, "medium": 1, "low": 0}
        priority_gaps.sort(
            key=lambda x: (importance_weight.get(str(x.get("importance", "")).lower(), 1), x.get("gap", 1)),
            reverse=True
        )

        # 5. Calculate coverage percentage
        if total_req_count == 0:
            coverage = 100.0
        else:
            # Full points for fully matched, partial points for partially matched
            matched_points = len(matched_skills) * 1.0
            for p in partial_skills:
                # fraction earned: student_level / required_level
                ratio = p["student_level"] / max(1, p["required_level"])
                matched_points += ratio * 0.5
            coverage = round(min(100.0, (matched_points / total_req_count) * 100.0), 1)

        # 6. Readiness status
        if coverage >= 80.0:
            status = "Ready to Apply"
        elif coverage >= 50.0:
            status = "Minor Gaps"
        else:
            status = "Significant Upskilling Needed"

        return {
            "matched_skills": matched_skills,
            "partial_skills": partial_skills,
            "missing_skills": missing_skills,
            "coverage": coverage,
            "priority_gaps": priority_gaps,
            "readiness_status": status,
            "total_required": total_req_count,
            "total_matched": len(matched_skills),
            "total_missing": len(missing_skills),
            "total_partial": len(partial_skills)
        }


skill_gap_analyzer = SkillGapAnalyzer()
