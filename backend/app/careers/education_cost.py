from typing import Dict, Any, Optional

EDUCATION_COST_DATABASE: Dict[str, Any] = {
    "b_tech": {
        "degree_name": "Bachelor of Technology (B.Tech / B.E.)",
        "duration_years": 4,
        "government_institutes": {
            "institutes": "IITs, NITs, IIITs, State Govt Engineering Colleges (COEP, VJTI, JNTU, OU)",
            "tuition_per_year": "₹1,20,000 – ₹2,20,000 (IITs/NITs) | ₹25,000 – ₹60,000 (State Govt)",
            "hostel_mess_per_year": "₹35,000 – ₹65,000",
            "total_4_year_cost": "₹3,50,000 – ₹10,50,000",
            "estimated_numeric_cost": 650000,
            "stipend_offset": "Eligible for Central Sector, NSP, and State Post-Matric scholarships covering up to 100% tuition for eligible categories."
        },
        "private_institutes": {
            "institutes": "Tier-1/2 Private: BITS Pilani, VIT Vellore, Manipal (MIT), Thapar, SRM",
            "tuition_per_year": "₹3,50,000 – ₹6,00,000",
            "hostel_mess_per_year": "₹1,20,000 – ₹2,00,000",
            "total_4_year_cost": "₹18,00,000 – ₹28,00,000",
            "estimated_numeric_cost": 2200000,
            "stipend_offset": "Merit scholarships available: BITS Merit-cum-Need offers 25%–80% tuition waiver for high scorers."
        },
        "tier3_private_colleges": {
            "institutes": "Regional Affiliated Engineering Colleges (State Counseling / Management Quota)",
            "tuition_per_year": "₹75,000 – ₹1,60,000 (Govt quota) | ₹2,00,000 – ₹3,50,000 (Management)",
            "hostel_mess_per_year": "₹60,000 – ₹90,000",
            "total_4_year_cost": "₹5,50,000 – ₹14,00,000",
            "estimated_numeric_cost": 850000,
            "stipend_offset": "State fee reimbursement (Jagananna Vidya Deevena, Telangana ePass, MahaDBT) frequently covers 60%–100% of tuition."
        },
        "additional_expenses": {
            "books_supplies": "₹20,000 – ₹40,000 total",
            "laptop_hardware": "₹50,000 – ₹90,000 one-time",
            "exam_certification_fees": "₹15,000 – ₹30,000 total"
        }
    },
    "m_tech": {
        "degree_name": "Master of Technology (M.Tech)",
        "duration_years": 2,
        "government_institutes": {
            "institutes": "IISc Bangalore, IITs, NITs",
            "tuition_per_year": "₹25,000 – ₹60,000",
            "hostel_mess_per_year": "₹35,000 – ₹55,000",
            "total_2_year_cost": "₹1,20,000 – ₹2,50,000",
            "estimated_numeric_cost": 180000,
            "stipend_offset": "GATE Qualified students receive mandatory MHRD stipend of ₹12,400/month (₹2.97 Lakhs over 2 years), rendering tuition effectively FREE."
        },
        "private_institutes": {
            "institutes": "BITS Pilani, VIT, IIIT Hyderabad",
            "tuition_per_year": "₹2,50,000 – ₹4,50,000",
            "hostel_mess_per_year": "₹80,000 – ₹1,20,000",
            "total_2_year_cost": "₹6,50,000 – ₹11,50,000",
            "estimated_numeric_cost": 850000,
            "stipend_offset": "Teaching Assistantships (TA/RA) often provide ₹10,000–₹15,000/month stipend."
        },
        "tier3_private_colleges": {
            "institutes": "State Affiliated Private Colleges",
            "tuition_per_year": "₹50,000 – ₹1,00,000",
            "hostel_mess_per_year": "₹50,000 – ₹80,000",
            "total_2_year_cost": "₹2,00,000 – ₹3,60,000",
            "estimated_numeric_cost": 280000,
            "stipend_offset": "Eligible for state government welfare fee reimbursement schemes."
        },
        "additional_expenses": {
            "books_supplies": "₹10,000 – ₹20,000 total",
            "laptop_hardware": "₹45,000 – ₹70,000 one-time",
            "exam_registration_fees": "₹5,000 – ₹10,000 total"
        }
    },
    "mba": {
        "degree_name": "MBA / PGDM (Master of Business Administration)",
        "duration_years": 2,
        "government_institutes": {
            "institutes": "IIM Ahmedabad/Bangalore/Calcutta, FMS Delhi, JBIMS Mumbai, IIT DMS",
            "tuition_per_year": "₹1,00,000 (FMS Delhi) to ₹12,50,000 (Top IIMs)",
            "hostel_mess_per_year": "₹60,000 – ₹1,50,000",
            "total_2_year_cost": "₹2,00,000 (FMS Delhi) | ₹10,00,000 (IITs) | ₹24,00,000 – ₹28,00,000 (Top IIMs)",
            "estimated_numeric_cost": 1500000,
            "stipend_offset": "100% collateral-free education loans available under SBI Scholar Scheme at prime rates."
        },
        "private_institutes": {
            "institutes": "XLRI, SPJIMR, NMIMS, Symbiosis (SIBM), Great Lakes",
            "tuition_per_year": "₹8,00,000 – ₹13,00,000",
            "hostel_mess_per_year": "₹1,50,000 – ₹2,50,000",
            "total_2_year_cost": "₹19,00,000 – ₹31,00,000",
            "estimated_numeric_cost": 2400000,
            "stipend_offset": "Corporate foundation grants and banking education credit available."
        },
        "tier3_private_colleges": {
            "institutes": "Regional Management Institutes & State University Affiliated",
            "tuition_per_year": "₹1,50,000 – ₹3,50,000",
            "hostel_mess_per_year": "₹70,000 – ₹1,20,000",
            "total_2_year_cost": "₹4,40,000 – ₹9,40,000",
            "estimated_numeric_cost": 650000,
            "stipend_offset": "State post-matric scholarships for eligible students."
        },
        "additional_expenses": {
            "books_supplies": "₹30,000 – ₹50,000 total",
            "laptop_hardware": "₹60,000 – ₹1,00,000 one-time",
            "exam_registration_fees": "CAT/XAT/GMAT fees: ₹15,000 – ₹30,000"
        }
    },
    "ms_abroad": {
        "degree_name": "MS Abroad (United States, Germany, UK, Canada)",
        "duration_years": 2,
        "government_institutes": {
            "institutes": "Germany Public Universities (e.g. TUM, RWTH Aachen, TU Berlin)",
            "tuition_per_year": "₹0 tuition (Administrative semester fee ~₹30,000/yr)",
            "hostel_mess_per_year": "₹10,00,000 – ₹12,50,000/yr (Mandatory German Blocked Account)",
            "total_2_year_cost": "₹21,00,000 – ₹26,00,000",
            "estimated_numeric_cost": 2350000,
            "stipend_offset": "Students can work 20 hours/week part-time (€1,000–€1,400/month) to cover living expenses."
        },
        "private_institutes": {
            "institutes": "United States Universities (Public & Private Tier-1/2)",
            "tuition_per_year": "₹18,00,000 – ₹38,00,000",
            "hostel_mess_per_year": "₹10,00,000 – ₹16,00,000",
            "total_2_year_cost": "₹56,00,000 – ₹1,08,00,000 total",
            "estimated_numeric_cost": 7500000,
            "stipend_offset": "Graduate Teaching/Research Assistantships (TA/RA) waive tuition and provide $1,500–$2,500/mo."
        },
        "tier3_private_colleges": {
            "institutes": "UK / Canada / Australia Mid-Tier Universities",
            "tuition_per_year": "₹14,00,000 – ₹22,00,000",
            "hostel_mess_per_year": "₹8,00,000 – ₹12,00,000",
            "total_2_year_cost": "₹44,00,000 – ₹68,00,000",
            "estimated_numeric_cost": 5500000,
            "stipend_offset": "Part-time work permitted up to 20 hrs/week during academic semesters."
        },
        "additional_expenses": {
            "books_supplies": "₹50,000 – ₹1,00,000",
            "laptop_hardware": "₹80,000 – ₹1,50,000",
            "exam_registration_fees": "GRE + TOEFL/IELTS + Visa & Sevis: ~₹85,000"
        }
    },
    "intermediate": {
        "degree_name": "Intermediate / Higher Secondary (11th & 12th / +2)",
        "duration_years": 2,
        "government_institutes": {
            "institutes": "Government Junior Colleges, Kendriya Vidyalayas (KV), Navodaya Vidyalayas",
            "tuition_per_year": "₹1,500 – ₹6,000 per year",
            "hostel_mess_per_year": "Free or ₹10,000 – ₹20,000/yr",
            "total_2_year_cost": "₹3,000 – ₹50,000",
            "estimated_numeric_cost": 25000,
            "stipend_offset": "Eligible for NMMS scholarship (₹12,000/yr) and state post-matric allowances."
        },
        "private_institutes": {
            "institutes": "Integrated Coaching Colleges (Sri Chaitanya, Narayana, FIITJEE)",
            "tuition_per_year": "₹1,10,000 – ₹2,50,000 per year",
            "hostel_mess_per_year": "₹70,000 – ₹1,40,000 per year",
            "total_2_year_cost": "₹3,60,000 – ₹7,80,000",
            "estimated_numeric_cost": 500000,
            "stipend_offset": "Concessions up to 75% fee discount based on 10th board GPA or entrance tests."
        },
        "tier3_private_colleges": {
            "institutes": "Local Private Day-Scholar Junior Colleges",
            "tuition_per_year": "₹25,000 – ₹55,000 per year",
            "hostel_mess_per_year": "Day scholar / local PG ₹40,000/yr",
            "total_2_year_cost": "₹50,000 – ₹1,30,000",
            "estimated_numeric_cost": 90000,
            "stipend_offset": "State fee reimbursement and welfare scholarships applicable."
        },
        "additional_expenses": {
            "books_supplies": "₹5,000 – ₹15,000 total",
            "laptop_hardware": "Not required",
            "exam_registration_fees": "Board & entrance exam fees: ₹4,000 – ₹8,000"
        }
    }
}


class EducationCostCalculator:
    """
    Deterministic domain service for calculating total cost of education across institutional tiers.
    """

    def calculate_cost(self, degree_or_path: str, college_tier: str = "all") -> Dict[str, Any]:
        key = (degree_or_path or "").strip().lower().replace(" ", "_").replace(".", "")
        if "btech" in key or "b_tech" in key or "engineering" in key or "be" == key:
            key = "b_tech"
        elif "mtech" in key or "m_tech" in key:
            key = "m_tech"
        elif "mba" in key or "management" in key or "pgdm" in key:
            key = "mba"
        elif "ms" in key or "abroad" in key or "foreign" in key or "masters" in key:
            key = "ms_abroad"
        elif "intermediate" in key or "inter" in key or "11" in key or "12" in key or "plus2" in key:
            key = "intermediate"
        else:
            key = "b_tech"

        data = EDUCATION_COST_DATABASE[key]
        tier_filter = (college_tier or "all").lower().strip()

        tier_breakdown = {}
        if "gov" in tier_filter or "iit" in tier_filter or "nit" in tier_filter:
            tier_breakdown = {"government_institutes": data["government_institutes"]}
        elif "priv" in tier_filter or "bits" in tier_filter or "vit" in tier_filter:
            tier_breakdown = {"private_institutes": data["private_institutes"]}
        elif "tier3" in tier_filter or "local" in tier_filter or "regional" in tier_filter:
            tier_breakdown = {"tier3_private_colleges": data["tier3_private_colleges"]}
        else:
            tier_breakdown = {
                "government_institutes": data["government_institutes"],
                "private_institutes": data["private_institutes"],
                "tier3_private_colleges": data["tier3_private_colleges"]
            }

        return {
            "degree_queried": degree_or_path,
            "standardized_degree": data["degree_name"],
            "duration_years": data["duration_years"],
            "institutional_tier_breakdown": tier_breakdown,
            "additional_estimated_expenses": data.get("additional_expenses", {})
        }


education_cost_calculator = EducationCostCalculator()
