import pandas as pd
from sqlalchemy import text
from pathlib import Path

from db import get_engine

# Resolve paths from this file's location so the script works on any machine
# and from any working directory (Airflow runs tasks from a temp dir).
DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"

engine = get_engine()

# Drop views before replacing raw tables — PostgreSQL won't drop a table with dependent views
with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS top_scorers CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_records CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_game_logs CASCADE"))
    conn.commit()

player_stats = pd.read_csv(DATA_DIR / "player_stats.csv")
standings = pd.read_csv(DATA_DIR / "standings.csv")
game_logs = pd.read_csv(DATA_DIR / "game_logs.csv")

player_stats.to_sql("player_stats", engine, if_exists="replace", index=False)
standings.to_sql("standings", engine, if_exists="replace", index=False)
game_logs.to_sql("game_logs", engine, if_exists="replace", index=False)

print("Done! All 3 tables loaded into nba_pipeline.")
