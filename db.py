import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Load PG* settings from .env in the project root (same variables dbt's profiles.yml reads).
# Variables already set in the shell take priority over the file.
load_dotenv(Path(__file__).resolve().parent / ".env")


def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        username=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD") or None,
        database=os.getenv("PGDATABASE", "nba_pipeline"),
    )
    return create_engine(url)
