from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class ScholarshipEligibilityEngine:
    """
    Deterministic rule-based eligibility verification engine for scholarships.
    Evaluates academic performance, family income, education stage, category, and domicile.
    Returns an explainable criteria breakdown.
    """

    def check_eligibility(
        self,
        student: Union[Any, Dict[str, Any]],
        scholarship: Union[Any, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Deterministically evaluates student profile against scholarship criteria.
        Returns:
        {
            "eligible": bool,
            "criteria": {
                "academic": {"required": float, "student": float, "passed": bool},
                "income": {"maximum": float, "student": float, "passed": bool},
                "education_stage": {"required": str, "student": str, "passed": bool},
                "category": {"required": str, "student": str, "passed": bool},
                "domicile": {"required": str, "student": str, "passed": bool}
            }
        }
        """
        # Helper getters supporting both ORM models and dictionaries
        def get_val(obj, key, default=None):
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        # 1. EDUCATION STAGE CHECK
        student_stage = get_val(student, "education_stage") or ""
        student_stage_norm = student_stage.strip().lower()

        eligible_stages_raw = get_val(scholarship, "eligible_stages") or ""
        if isinstance(eligible_stages_raw, list):
            req_stages = [s.strip().lower() for s in eligible_stages_raw if s]
        else:
            req_stages = [s.strip().lower() for s in eligible_stages_raw.split(",") if s.strip()]

        if not req_stages:
            stage_passed = True
            req_stage_display = "Any"
        else:
            stage_passed = student_stage_norm in req_stages
            req_stage_display = ", ".join(s.replace("_", " ").title() for s in req_stages)

        criteria_stage = {
            "required": req_stage_display,
            "student": student_stage.replace("_", " ").title() if student_stage else "Unspecified",
            "passed": bool(stage_passed)
        }

        # 2. ACADEMIC PERFORMANCE CHECK
        req_academic = get_val(scholarship, "min_cgpa_or_percentage")
        acad_obj = get_val(student, "academic_profile")
        student_perc = None
        student_cgpa = None

        if acad_obj:
            student_perc = get_val(acad_obj, "percentage")
            student_cgpa = get_val(acad_obj, "cgpa")
        else:
            student_perc = get_val(student, "percentage")
            student_cgpa = get_val(student, "cgpa")

        # Normalize student academic score to percentage scale (0-100)
        eff_student_score = None
        if student_perc is not None:
            eff_student_score = float(student_perc)
        elif student_cgpa is not None:
            # 10-point CGPA standard conversion: CGPA * 9.5
            eff_student_score = float(student_cgpa) * 9.5

        if req_academic is None or req_academic <= 0:
            academic_passed = True
            req_academic_val = 0.0
        else:
            req_academic_val = float(req_academic)
            # If required is given as CGPA <= 10.0, convert to percentage for comparison
            target_perc = req_academic_val if req_academic_val > 10.0 else (req_academic_val * 9.5)
            if eff_student_score is not None:
                academic_passed = eff_student_score >= target_perc
            else:
                academic_passed = False

        criteria_academic = {
            "required": req_academic_val,
            "student": round(eff_student_score, 1) if eff_student_score is not None else 0.0,
            "passed": bool(academic_passed)
        }

        # 3. FAMILY INCOME CHECK
        max_income = get_val(scholarship, "max_income")
        fin_obj = get_val(student, "financial_context")
        student_income = None

        if fin_obj:
            student_income = get_val(fin_obj, "annual_family_income")
            if student_income is None:
                budget = get_val(fin_obj, "education_budget")
                if budget and isinstance(budget, (int, float)):
                    student_income = float(budget)
        if student_income is None:
            student_income = get_val(student, "annual_family_income") or get_val(student, "income")

        if max_income is None or max_income <= 0:
            income_passed = True
            max_income_val = None
        else:
            max_income_val = float(max_income)
            if student_income is not None:
                income_passed = float(student_income) <= max_income_val
            else:
                # If no income ceiling violation reported, default to True unless income is strictly required
                income_passed = True

        criteria_income = {
            "maximum": max_income_val if max_income_val is not None else "No Limit",
            "student": float(student_income) if student_income is not None else "Not Provided",
            "passed": bool(income_passed)
        }

        # 4. CATEGORY CHECK
        req_categories_raw = get_val(scholarship, "eligible_categories") or ""
        if isinstance(req_categories_raw, list):
            req_categories = [c.strip().lower() for c in req_categories_raw if c]
        else:
            req_categories = [c.strip().lower() for c in req_categories_raw.split(",") if c.strip()]

        student_cat = (get_val(student, "category") or get_val(student, "social_category") or "").strip().lower()

        if not req_categories or any(c in ["all", "any", "general", "open"] for c in req_categories):
            category_passed = True
            req_cat_display = "All Categories"
        else:
            req_cat_display = ", ".join(c.upper() for c in req_categories)
            if student_cat:
                category_passed = any(c == student_cat for c in req_categories)
            else:
                # If student did not specify category, cannot claim reservation
                category_passed = False

        criteria_category = {
            "required": req_cat_display,
            "student": student_cat.upper() if student_cat else "General / Unspecified",
            "passed": bool(category_passed)
        }

        # 5. DOMICILE CHECK
        req_states_raw = get_val(scholarship, "eligible_states") or ""
        if isinstance(req_states_raw, list):
            req_states = [s.strip().lower() for s in req_states_raw if s]
        else:
            req_states = [s.strip().lower() for s in req_states_raw.split(",") if s.strip()]

        student_loc = (get_val(student, "location") or get_val(student, "state") or get_val(student, "domicile") or "").strip().lower()

        if not req_states or any(s in ["all", "pan-india", "pan india", "any"] for s in req_states):
            domicile_passed = True
            req_states_display = "Pan-India"
        else:
            req_states_display = ", ".join(s.title() for s in req_states)
            if student_loc:
                domicile_passed = any(s in student_loc or student_loc in s for s in req_states)
            else:
                domicile_passed = False

        criteria_domicile = {
            "required": req_states_display,
            "student": student_loc.title() if student_loc else "Unspecified",
            "passed": bool(domicile_passed)
        }

        # Check expired or closed status
        status = get_val(scholarship, "status")
        is_active = status != "expired"

        overall_eligible = (
            stage_passed and
            academic_passed and
            income_passed and
            category_passed and
            domicile_passed and
            is_active
        )

        return {
            "eligible": bool(overall_eligible),
            "criteria": {
                "academic": criteria_academic,
                "income": criteria_income,
                "education_stage": criteria_stage,
                "category": criteria_category,
                "domicile": criteria_domicile
            }
        }
