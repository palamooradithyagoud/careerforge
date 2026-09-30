from typing import Dict, Any, Optional
from backend.app.careers.salary import salary_estimator, SALARY_ESTIMATES_DATABASE
from backend.app.careers.education_cost import education_cost_calculator, EDUCATION_COST_DATABASE


class EducationROICalculator:
    """
    Deterministic domain service for calculating Education Return on Investment (ROI),
    payback period, and 5-year net economic surplus.
    """

    def calculate_roi(
        self,
        degree: str,
        target_career: str,
        college_tier: str = "government",
        starting_salary_lpa: Optional[float] = None
    ) -> Dict[str, Any]:
        cost_info = education_cost_calculator.calculate_cost(degree, college_tier)
        salary_info = salary_estimator.estimate_salary(target_career, "entry")

        # Determine total educational investment cost
        tier_data = cost_info["institutional_tier_breakdown"]
        primary_tier = list(tier_data.values())[0] if tier_data else {}
        total_cost_str = primary_tier.get("total_4_year_cost") or primary_tier.get("total_2_year_cost", "₹6,50,000")

        # Numeric cost estimate
        deg_key = (degree or "").lower().replace(" ", "_").replace(".", "")
        if "b_tech" in deg_key or "btech" in deg_key:
            numeric_cost = 650000 if "gov" in college_tier else (2200000 if "priv" in college_tier else 850000)
        elif "mba" in deg_key:
            numeric_cost = 1500000 if "gov" in college_tier else (2400000 if "priv" in college_tier else 650000)
        elif "m_tech" in deg_key or "mtech" in deg_key:
            numeric_cost = 180000 if "gov" in college_tier else 850000
        elif "ms" in deg_key or "abroad" in deg_key:
            numeric_cost = 2350000 if "gov" in college_tier else 7500000
        else:
            numeric_cost = 500000

        # Numeric salary estimate
        if starting_salary_lpa is not None and starting_salary_lpa > 0:
            median_salary = float(starting_salary_lpa)
        else:
            exp_bd = salary_info["experience_breakdown"]
            entry_bd = exp_bd.get("entry_level_0_2_yrs", {})
            median_salary = entry_bd.get("median_val", 10.0)

        annual_salary_inr = median_salary * 100000
        estimated_living_cost_annual = 250000  # Baseline annual living cost in tier-1/2 Indian tech hubs
        annual_net_savings = max(100000.0, annual_salary_inr * 0.45)

        # Payback period (months)
        payback_months = round((numeric_cost / annual_net_savings) * 12, 1)

        # 5-Year net economic surplus
        gross_5yr_earnings = annual_salary_inr * 5.8  # factoring 15% annual average career progression
        net_5yr_surplus = round(gross_5yr_earnings - numeric_cost, 2)
        roi_ratio = round(gross_5yr_earnings / numeric_cost, 2) if numeric_cost > 0 else 99.9

        return {
            "degree": cost_info["standardized_degree"],
            "target_career": salary_info["matched_benchmark"],
            "institutional_tier": college_tier.capitalize(),
            "total_education_investment_inr": numeric_cost,
            "total_investment_range_display": total_cost_str,
            "starting_salary_lpa": median_salary,
            "projected_annual_gross_inr": int(annual_salary_inr),
            "estimated_payback_period_months": payback_months,
            "five_year_net_economic_surplus_inr": int(net_5yr_surplus),
            "five_year_roi_multiplier": f"{roi_ratio}x",
            "verdict": "Exceptional ROI" if roi_ratio >= 4.0 else ("Strong ROI" if roi_ratio >= 2.0 else "Moderate ROI")
        }


education_roi_calculator = EducationROICalculator()
