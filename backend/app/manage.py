"""
ASCEND Database & Operations Management CLI

Usage:
    python -m backend.app.manage migrate
    python -m backend.app.manage seed
    python -m backend.app.manage init-db
"""

import sys
import logging
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.seeds.migrate_db import apply_migrations
from backend.app.seeds.seed_data import seed_database
from backend.app.seeds.agent_seed_data import seed_agent_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ASCEND-CLI")


def run_migrate():
    logger.info("Executing database table creation and schema migrations...")
    Base.metadata.create_all(bind=engine)
    apply_migrations()
    logger.info("Migrations completed successfully.")


def run_seed():
    logger.info("Executing authoritative data seeding...")
    db = SessionLocal()
    try:
        seed_database(db)
        seed_agent_data(db)
        logger.info("Seeding completed successfully.")
    except Exception as exc:
        logger.error(f"Seeding failed: {exc}")
        db.rollback()
        raise
    finally:
        db.close()


def run_init():
    run_migrate()
    run_seed()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m backend.app.manage [migrate | seed | init-db]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "migrate":
        run_migrate()
    elif command == "seed":
        run_seed()
    elif command in ("init-db", "init"):
        run_init()
    else:
        print(f"Unknown command '{command}'. Available: migrate, seed, init-db")
        sys.exit(1)
