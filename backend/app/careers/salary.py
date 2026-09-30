from typing import Dict, Any, Optional

# Authoritative industry salary benchmark database (India & Global Remote 2025-2026)
SALARY_ESTIMATES_DATABASE: Dict[str, Any] = {
    "ai_engineer": {
        "career_title": "AI / Machine Learning Engineer",
        "category": "Artificial Intelligence & Data",
        "market": "India & Global Remote Benchmarks (2025-2026)",
        "currency": "INR (LPA)",
        "experience_breakdown": {
            "entry_level_0_2_yrs": {
                "range": "₹8.0 – ₹18.0 LPA",
                "median": "₹12.0 LPA",
                "median_val": 12.0,
                "breakdown": {
                    "service_companies_tier3": "₹5.0 – ₹7.5 LPA",
                    "mid_tier_product_startups": "₹10.0 – ₹16.0 LPA",
                    "tier1_product_faang": "₹20.0 – ₹35.0 LPA (including stock/joining bonus)"
                }
            },
            "mid_level_2_5_yrs": {
                "range": "₹18.0 – ₹35.0 LPA",
                "median": "₹25.0 LPA",
                "median_val": 25.0,
                "breakdown": {
                    "enterprise_tech": "₹16.0 – ₹24.0 LPA",
                    "high_growth_product_fintech": "₹26.0 – ₹42.0 LPA"
                }
            },
            "senior_lead_5_plus_yrs": {
                "range": "₹38.0 – ₹75.0+ LPA",
                "median": "₹52.0 LPA",
                "median_val": 52.0,
                "breakdown": {
                    "principal_lead_ai_architect": "₹55.0 – ₹95.0+ LPA (with equity/ESOPs)"
                }
            }
        },
        "us_global_benchmark": "$115,000 – $185,000 / year (Remote / US)",
        "key_skills_driving_top_pay": [
            "LLM Fine-Tuning (LoRA, QLoRA)",
            "RAG Architecture & Vector DBs",
            "PyTorch, LangChain, vLLM",
            "MLOps, Docker, Kubernetes & Model Serving"
        ],
        "top_hiring_sectors": ["Fintech & Trading", "HealthTech", "Enterprise SaaS", "E-Commerce", "Autonomous Systems"]
    },
    "software_engineer": {
        "career_title": "Software Development Engineer (SDE / Full Stack)",
        "category": "Core Software Engineering",
        "market": "India & Global Remote Benchmarks (2025-2026)",
        "currency": "INR (LPA)",
        "experience_breakdown": {
            "entry_level_0_2_yrs": {
                "range": "₹6.0 – ₹16.0 LPA",
                "median": "₹9.5 LPA",
                "median_val": 9.5,
                "breakdown": {
                    "it_services_tcs_wipro_infy": "₹3.8 – ₹6.5 LPA (Ninja/Digital/Turbo)",
                    "product_startups_unicorns": "₹12.0 – ₹20.0 LPA",
                    "faang_tier1_mncs": "₹18.0 – ₹32.0 LPA (Base + ESOPs)"
                }
            },
            "mid_level_2_5_yrs": {
                "range": "₹16.0 – ₹32.0 LPA",
                "median": "₹22.0 LPA",
                "median_val": 22.0,
                "breakdown": {
                    "standard_product_firm": "₹15.0 – ₹25.0 LPA",
                    "tier1_fintech_hypergrowth": "₹28.0 – ₹42.0 LPA"
                }
            },
            "senior_lead_5_plus_yrs": {
                "range": "₹32.0 – ₹65.0+ LPA",
                "median": "₹45.0 LPA",
                "median_val": 45.0,
                "breakdown": {
                    "staff_sde_engineering_manager": "₹50.0 – ₹85.0+ LPA"
                }
            }
        },
        "us_global_benchmark": "$95,000 – $160,000 / year",
        "key_skills_driving_top_pay": [
            "Data Structures & System Design (HLD/LLD)",
            "Distributed Systems & Microservices",
            "Go, Rust, Java/Spring or Node/TypeScript",
            "AWS/GCP Cloud Architecture"
        ],
        "top_hiring_sectors": ["Cloud Infrastructure", "Fintech", "Consumer Internet", "B2B SaaS"]
    },
    "data_scientist": {
        "career_title": "Data Scientist / Data Analyst",
        "category": "Data Science & Analytics",
        "market": "India & Global Remote Benchmarks (2025-2026)",
        "currency": "INR (LPA)",
        "experience_breakdown": {
            "entry_level_0_2_yrs": {
                "range": "₹5.5 – ₹14.0 LPA",
                "median": "₹8.5 LPA",
                "median_val": 8.5,
                "breakdown": {
                    "analytics_consultancies": "₹4.5 – ₹7.5 LPA",
                    "tech_product_analytics": "₹10.0 – ₹16.0 LPA"
                }
            },
            "mid_level_2_5_yrs": {
                "range": "₹14.0 – ₹28.0 LPA",
                "median": "₹19.0 LPA",
                "median_val": 19.0,
                "breakdown": {
                    "banking_consulting_big4": "₹14.0 – ₹22.0 LPA",
                    "product_bi_team": "₹20.0 – ₹32.0 LPA"
                }
            },
            "senior_lead_5_plus_yrs": {
                "range": "₹30.0 – ₹55.0+ LPA",
                "median": "₹38.0 LPA",
                "median_val": 38.0,
                "breakdown": {
                    "principal_data_scientist": "₹42.0 – ₹70.0+ LPA"
                }
            }
        },
        "us_global_benchmark": "$100,000 – $165,000 / year",
        "key_skills_driving_top_pay": [
            "Predictive Modeling & Statistical Inference",
            "SQL, Pandas, NumPy, Scikit-Learn",
            "A/B Testing & Causal Inference",
            "Tableau, PowerBI & Storytelling"
        ],
        "top_hiring_sectors": ["Financial Services", "Retail Analytics", "Healthcare", "Consulting"]
    },
    "devops_engineer": {
        "career_title": "DevOps / Cloud & Site Reliability Engineer (SRE)",
        "category": "Cloud & Infrastructure",
        "market": "India & Global Remote Benchmarks (2025-2026)",
        "currency": "INR (LPA)",
        "experience_breakdown": {
            "entry_level_0_2_yrs": {
                "range": "₹6.0 – ₹14.0 LPA",
                "median": "₹9.0 LPA",
                "median_val": 9.0,
                "breakdown": {
                    "tier3_service_firms": "₹4.0 – ₹6.5 LPA",
                    "cloud_consulting_partners": "₹8.0 – ₹14.0 LPA"
                }
            },
            "mid_level_2_5_yrs": {
                "range": "₹15.0 – ₹30.0 LPA",
                "median": "₹21.0 LPA",
                "median_val": 21.0,
                "breakdown": {
                    "saas_enterprise_ops": "₹15.0 – ₹24.0 LPA",
                    "tier1_fintech_sre": "₹25.0 – ₹38.0 LPA"
                }
            },
            "senior_lead_5_plus_yrs": {
                "range": "₹32.0 – ₹65.0+ LPA",
                "median": "₹44.0 LPA",
                "median_val": 44.0,
                "breakdown": {
                    "cloud_architect_head_of_infra": "₹48.0 – ₹80.0+ LPA"
                }
            }
        },
        "us_global_benchmark": "$110,000 – $175,000 / year",
        "key_skills_driving_top_pay": [
            "Kubernetes & Container Orchestration",
            "Terraform & Infrastructure as Code (IaC)",
            "CI/CD Pipeline Automation (GitHub Actions, GitLab)",
            "AWS / Azure / GCP Solutions Architecture"
        ],
        "top_hiring_sectors": ["Cloud SaaS Providers", "Fintech & Banking", "Telecom", "Gaming Infrastructure"]
    },
    "cybersecurity_analyst": {
        "career_title": "Cybersecurity Analyst / Security Engineer",
        "category": "Information Security & Defense",
        "market": "India & Global Remote Benchmarks (2025-2026)",
        "currency": "INR (LPA)",
        "experience_breakdown": {
            "entry_level_0_2_yrs": {
                "range": "₹5.5 – ₹13.0 LPA",
                "median": "₹8.0 LPA",
                "median_val": 8.0,
                "breakdown": {
                    "soc_analyst_l1_service": "₹4.0 – ₹6.0 LPA",
                    "security_product_firm": "₹8.0 – ₹14.0 LPA"
                }
            },
            "mid_level_2_5_yrs": {
                "range": "₹14.0 – ₹28.0 LPA",
                "median": "₹19.5 LPA",
                "median_val": 19.5,
                "breakdown": {
                    "penetration_tester_vapt": "₹14.0 – ₹22.0 LPA",
                    "cloud_security_devsecops": "₹22.0 – ₹32.0 LPA"
                }
            },
            "senior_lead_5_plus_yrs": {
                "range": "₹30.0 – ₹60.0+ LPA",
                "median": "₹40.0 LPA",
                "median_val": 40.0,
                "breakdown": {
                    "ciso_security_architect": "₹45.0 – ₹75.0+ LPA"
                }
            }
        },
        "us_global_benchmark": "$105,000 – $170,000 / year",
        "key_skills_driving_top_pay": [
            "SIEM & Incident Response (Splunk, Sentinel)",
            "Cloud Security (AWS Security Hub, IAM, GuardDuty)",
            "DevSecOps & SAST/DAST Tooling",
            "Certifications: OSCP, CISSP, CEH"
        ],
        "top_hiring_sectors": ["Banking & Financial Services", "Defense & Government", "Healthcare IT", "E-Commerce"]
    }
}


class SalaryEstimator:
    """
    Deterministic domain service for market salary benchmarks.
    """

    def estimate_salary(self, career_name: str, experience_level: str = "all") -> Dict[str, Any]:
        target = (career_name or "").strip().lower().replace(" ", "_").replace("-", "_")

        matched_key = None
        for k in SALARY_ESTIMATES_DATABASE.keys():
            if k in target or target in k:
                matched_key = k
                break

        if not matched_key:
            if "ai" in target or "machine" in target or "ml" in target or "deep" in target:
                matched_key = "ai_engineer"
            elif "data" in target or "analyst" in target:
                matched_key = "data_scientist"
            elif "cloud" in target or "devops" in target or "sre" in target or "infra" in target:
                matched_key = "devops_engineer"
            elif "security" in target or "cyber" in target or "soc" in target:
                matched_key = "cybersecurity_analyst"
            else:
                matched_key = "software_engineer"

        data = SALARY_ESTIMATES_DATABASE[matched_key]
        breakdown = data["experience_breakdown"]

        exp_filter = (experience_level or "all").lower().strip()
        filtered_breakdown = {}
        if "entry" in exp_filter or "0" in exp_filter or "fresher" in exp_filter:
            filtered_breakdown = {"entry_level_0_2_yrs": breakdown["entry_level_0_2_yrs"]}
        elif "mid" in exp_filter or "2" in exp_filter or "3" in exp_filter:
            filtered_breakdown = {"mid_level_2_5_yrs": breakdown["mid_level_2_5_yrs"]}
        elif "senior" in exp_filter or "lead" in exp_filter or "5" in exp_filter:
            filtered_breakdown = {"senior_lead_5_plus_yrs": breakdown["senior_lead_5_plus_yrs"]}
        else:
            filtered_breakdown = breakdown

        return {
            "career_queried": career_name,
            "matched_benchmark": data["career_title"],
            "category": data["category"],
            "currency": data["currency"],
            "market": data["market"],
            "experience_breakdown": filtered_breakdown,
            "us_global_remote_benchmark": data.get("us_global_benchmark"),
            "key_skills_driving_top_compensation": data.get("key_skills_driving_top_pay", []),
            "top_hiring_sectors": data.get("top_hiring_sectors", [])
        }


salary_estimator = SalaryEstimator()
