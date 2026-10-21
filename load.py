import pandas as pd
from sqlalchemy import create_engine, text

engine = get_engine()

# Drop views before replacing raw tables — PostgreSQL won't drop a table with dependent views
with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS top_scorers CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_records CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS team_game_logs CASCADE"))
    conn.commit()

player_stats = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/player_stats.csv")
standings = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/standings.csv")
game_logs = pd.read_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/game_logs.csv")

player_stats.to_sql("player_stats", engine, if_exists="replace", index=False)
standings.to_sql("standings", engine, if_exists="replace", index=False)
game_logs.to_sql("game_logs", engine, if_exists="replace", index=False)

print("Done! All 3 tables loaded into nba_pipeline.")
