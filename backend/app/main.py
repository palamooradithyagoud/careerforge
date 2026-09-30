from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.core.cache import cache
from backend.app.api.v1.router import api_router
from backend.app.seeds.migrate_db import apply_migrations
from backend.app.seeds.seed_data import seed_database
from backend.app.seeds.agent_seed_data import seed_agent_data


import os
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application boot: verify database connectivity without running heavy mutations
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("[Startup] Database connection verified successfully.")
    except Exception as exc:
        logger.error(f"[Startup] Database connectivity check failed: {exc}")

    # Explicit opt-in for containerized zero-setup testing (disabled by default in production)
    if os.getenv("RUN_MIGRATIONS_ON_STARTUP", "false").lower() in ("true", "1", "yes"):
        logger.info("[Startup] Running database migrations on startup (opt-in)...")
        Base.metadata.create_all(bind=engine)
        apply_migrations()

    if os.getenv("RUN_SEEDS_ON_STARTUP", "false").lower() in ("true", "1", "yes"):
        logger.info("[Startup] Seeding database on startup (opt-in)...")
        db = SessionLocal()
        try:
            seed_database(db)
            seed_agent_data(db)
        finally:
            db.close()

    # Pre-warm read-only cache safely (non-destructive)
    db = SessionLocal()
    try:
        cache.warm_up(db)
    except Exception as exc:
        logger.warning(f"[Startup] Cache warm-up notice: {exc}")
    finally:
        db.close()

    yield

    # Shutdown logic if needed


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SkillCatalyst Backend: Student Onboarding & Intelligence Profile API",
    version="1.1.0",
    lifespan=lifespan
)

# CORS middleware for Next.js frontend communication (supports local dev and all Vercel deployments)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"],
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }


@app.get("/health/rag", tags=["System"])
def root_rag_health_check():
    from backend.app.services.rag.vector_store import vector_store
    from backend.app.services.rag.embeddings import embedding_provider
    chroma_health = vector_store.health_check()
    return {
        "status": chroma_health.get("status", "healthy"),
        "chroma": "healthy" if chroma_health.get("status") == "healthy" else "unhealthy",
        "embeddings": "healthy",
        "collection": chroma_health.get("collection_name", "skillcatalyst_knowledge"),
        "document_count": chroma_health.get("total_chunks", 0),
        "embedding_model": embedding_provider.model_name(),
        "embedding_dimension": embedding_provider.embedding_dimension()
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
