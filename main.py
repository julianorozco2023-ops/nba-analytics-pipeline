from nba_api.stats.endpoints import leagueleaders, leaguestandingsv3, teamgamelog
from nba_api.stats.static import teams
import pandas as pd
import time
from pathlib import Path

# Resolve paths from this file's location so the script works on any machine
# and from any working directory (Airflow runs tasks from a temp dir).
DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"
# data/raw/ isn't in the repo (CSVs are gitignored), so create it on first run
DATA_DIR.mkdir(parents=True, exist_ok=True)

all_teams = teams.get_teams()

leaders = leagueleaders.LeagueLeaders(
    season="2023-24",
    stat_category_abbreviation="PTS",
    per_mode48="PerGame"
)
df = leaders.get_data_frames()[0]
df.to_csv(DATA_DIR / "player_stats.csv", index=False)

time.sleep(0.6)

all_logs = []
for team in all_teams:
    log = teamgamelog.TeamGameLog(team_id=team["id"], season="2023-24")
    df = log.get_data_frames()[0]
    df["TEAM_NAME"] = team["full_name"]
    all_logs.append(df)
    time.sleep(0.6)

combined = pd.concat(all_logs, ignore_index=True)
combined.to_csv(DATA_DIR / "game_logs.csv", index=False)

standings = leaguestandingsv3.LeagueStandingsV3(season="2023-24")
df = standings.get_data_frames()[0]
df.to_csv(DATA_DIR / "standings.csv", index=False)
