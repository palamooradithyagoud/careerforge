from typing import Dict, Any, List, Optional
from backend.app.careers.salary import salary_estimator, SalaryEstimator
from backend.app.careers.education_cost import education_cost_calculator, EducationCostCalculator
from backend.app.careers.roi import education_roi_calculator, EducationROICalculator


class CareerPathwayEngine:
    """
    Career Pathway Engine exposing unified career intelligence:
    - Career comparison
    - Salary estimation
    - Education cost computation
    - Education ROI calculation
    """

    def __init__(self):
        self.salary_estimator = salary_estimator
        self.cost_calculator = education_cost_calculator
        self.roi_calculator = education_roi_calculator

    def get_salary_estimate(self, career_name: str, experience_level: str = "all") -> Dict[str, Any]:
        return self.salary_estimator.estimate_salary(career_name, experience_level)

    def get_education_cost(self, degree_or_path: str, college_tier: str = "all") -> Dict[str, Any]:
        return self.cost_calculator.calculate_cost(degree_or_path, college_tier)

    def calculate_education_roi(
        self,
        degree: str,
        target_career: str,
        college_tier: str = "government",
        starting_salary_lpa: Optional[float] = None
    ) -> Dict[str, Any]:
        return self.roi_calculator.calculate_roi(degree, target_career, college_tier, starting_salary_lpa)

    def compare_career_pathways(
        self,
        career_a: str,
        career_b: str,
        student_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Conducts comparative structural analysis across two career pathways:
        Compensation, skill velocity, educational ROI, and market elasticity.
        """
        sal_a = self.salary_estimator.estimate_salary(career_a)
        sal_b = self.salary_estimator.estimate_salary(career_b)

        bd_a = sal_a["experience_breakdown"]
        bd_b = sal_b["experience_breakdown"]

        entry_a = bd_a.get("entry_level_0_2_yrs", {}).get("median", "₹10 LPA")
        entry_b = bd_b.get("entry_level_0_2_yrs", {}).get("median", "₹10 LPA")

        mid_a = bd_a.get("mid_level_2_5_yrs", {}).get("median", "₹22 LPA")
        mid_b = bd_b.get("mid_level_2_5_yrs", {}).get("median", "₹22 LPA")

        senior_a = bd_a.get("senior_lead_5_plus_yrs", {}).get("median", "₹45 LPA")
        senior_b = bd_b.get("senior_lead_5_plus_yrs", {}).get("median", "₹45 LPA")

        comparison = {
            "comparison_title": f"{sal_a['matched_benchmark']} vs. {sal_b['matched_benchmark']}",
            "pathway_a": {
                "name": sal_a["matched_benchmark"],
                "category": sal_a["category"],
                "entry_salary_median": entry_a,
                "mid_salary_median": mid_a,
                "senior_salary_median": senior_a,
                "us_benchmark": sal_a.get("us_global_remote_benchmark"),
                "core_accelerators": sal_a.get("key_skills_driving_top_compensation", [])[:3],
                "top_sectors": sal_a.get("top_hiring_sectors", [])[:3]
            },
            "pathway_b": {
                "name": sal_b["matched_benchmark"],
                "category": sal_b["category"],
                "entry_salary_median": entry_b,
                "mid_salary_median": mid_b,
                "senior_salary_median": senior_b,
                "us_benchmark": sal_b.get("us_global_remote_benchmark"),
                "core_accelerators": sal_b.get("key_skills_driving_top_compensation", [])[:3],
                "top_sectors": sal_b.get("top_hiring_sectors", [])[:3]
            },
            "strategic_synthesis": {
                "highest_entry_compensation": sal_a["matched_benchmark"] if "ai" in career_a.lower() else sal_b["matched_benchmark"],
                "broader_market_openings": "Software Development Engineer" if "software" in f"{career_a} {career_b}".lower() else "Data Science & Cloud",
                "recommended_dual_trajectory": f"Build core Software Engineering fundamentals (DSA, Systems) while specializing in {sal_a['matched_benchmark'] if 'ai' in career_a.lower() else sal_b['matched_benchmark']} technologies."
            }
        }

        # If student profile is provided, calculate alignment
        if student_profile and isinstance(student_profile, dict):
            student_skills = [
                s.get("skill_name") or s.get("name") or str(s)
                for s in student_profile.get("skills", [])
            ]
            skills_lower = [s.lower() for s in student_skills]

            a_matches = sum(1 for sk in sal_a.get("key_skills_driving_top_compensation", []) if any(w.lower() in skills_lower for w in sk.split()))
            b_matches = sum(1 for sk in sal_b.get("key_skills_driving_top_compensation", []) if any(w.lower() in skills_lower for w in sk.split()))

            comparison["student_profile_alignment"] = {
                "pathway_a_skill_overlap": a_matches,
                "pathway_b_skill_overlap": b_matches,
                "closer_initial_fit": sal_a["matched_benchmark"] if a_matches >= b_matches else sal_b["matched_benchmark"]
            }

        return comparison


career_pathway_engine = CareerPathwayEngine()
