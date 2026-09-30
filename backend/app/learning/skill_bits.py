from typing import Dict, Any, List, Optional

SKILL_BITS_CATALOG: Dict[str, Dict[str, Any]] = {
    "python": {
        "skill": "Python",
        "category": "Programming",
        "bite_size_topics": [
            {
                "topic": "Python Generators & Memory Optimization",
                "key_concept": "Yield statements produce lazy iterators that evaluate on demand, preventing OOM in large data streams.",
                "practical_example": "def stream_lines(f): for line in f: yield line.strip()",
                "estimated_minutes": 5
            },
            {
                "topic": "Decorators & Metaprogramming",
                "key_concept": "First-class functions wrapping callables for cross-cutting concerns like logging, timing, and caching.",
                "practical_example": "def logged(fn): def wrap(*a, **k): print(a); return fn(*a, **k); return wrap",
                "estimated_minutes": 7
            }
        ]
    },
    "fastapi": {
        "skill": "FastAPI",
        "category": "Backend Engineering",
        "bite_size_topics": [
            {
                "topic": "Dependency Injection with Depends",
                "key_concept": "FastAPI resolves dependencies hierarchically at request time, ideal for DB sessions and auth verification.",
                "practical_example": "def get_db(): db = Session(); try: yield db finally: db.close()",
                "estimated_minutes": 5
            },
            {
                "topic": "Pydantic V2 Serialization & Validation",
                "key_concept": "Strict type schema contracts enforced before hitting route logic, preventing malformed payload attacks.",
                "practical_example": "class UserIn(BaseModel): email: EmailStr; age: int = Field(ge=18)",
                "estimated_minutes": 5
            }
        ]
    },
    "react": {
        "skill": "React",
        "category": "Frontend Engineering",
        "bite_size_topics": [
            {
                "topic": "Server Components vs Client Components",
                "key_concept": "RSC execute purely on server with zero bundle weight, Client Components handle user interactivity and hooks.",
                "practical_example": "'use client'; export function Counter() { const [c, sc] = useState(0); ... }",
                "estimated_minutes": 6
            },
            {
                "topic": "State Management with Zustand",
                "key_concept": "Unopinionated, hook-based minimal store with no boilerplate or context provider hell.",
                "practical_example": "export const useStore = create((set) => ({ count: 0, inc: () => set(s => ({count: s.count+1})) }))",
                "estimated_minutes": 5
            }
        ]
    },
    "docker": {
        "skill": "Docker",
        "category": "DevOps & Cloud",
        "bite_size_topics": [
            {
                "topic": "Multi-Stage Builds",
                "key_concept": "Separate builder images containing compilers from minimal runtime alpine containers to shrink image size by 80%.",
                "practical_example": "FROM python:3.11-slim as builder ... FROM python:3.11-alpine; COPY --from=builder ...",
                "estimated_minutes": 5
            }
        ]
    },
    "sql": {
        "skill": "SQL",
        "category": "Databases",
        "bite_size_topics": [
            {
                "topic": "B-Tree Indexing & Query Execution Plans",
                "key_concept": "Use EXPLAIN ANALYZE to identify sequential table scans and index multi-column composite keys appropriately.",
                "practical_example": "CREATE INDEX idx_student_stage ON students(education_stage, created_at DESC);",
                "estimated_minutes": 6
            }
        ]
    },
    "machine_learning": {
        "skill": "Machine Learning",
        "category": "AI & Data",
        "bite_size_topics": [
            {
                "topic": "RAG Embeddings & Vector Distance Metrics",
                "key_concept": "Cosine similarity measures angular distance between semantic embedding vectors independently of document length.",
                "practical_example": "similarity = dot(u, v) / (norm(u) * norm(v))",
                "estimated_minutes": 7
            }
        ]
    }
}


class SkillBitsService:
    """
    Service providing bite-sized micro-learning nuggets (Skill Bits) for fast concept acquisition.
    """

    def get_skill_bits_for_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        target = skill_name.strip().lower()
        for k, v in SKILL_BITS_CATALOG.items():
            if k in target or target in k:
                return v

        # Default fallback bit
        return {
            "skill": skill_name.title(),
            "category": "Technical Skill",
            "bite_size_topics": [
                {
                    "topic": f"{skill_name.title()} Fundamentals & Hands-on Implementation",
                    "key_concept": f"Master the architectural core principles of {skill_name.title()} and apply them in real-world scenarios.",
                    "practical_example": f"# Review official documentation and build a mini-project applying {skill_name.title()}",
                    "estimated_minutes": 5
                }
            ]
        }

    def get_skill_bits_for_skills(self, skill_names: List[str]) -> List[Dict[str, Any]]:
        results = []
        for s in skill_names:
            bit = self.get_skill_bits_for_skill(s)
            if bit:
                results.append(bit)
        return results


skill_bits_service = SkillBitsService()
