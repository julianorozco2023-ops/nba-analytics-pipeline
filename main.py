from nba_api.stats.endpoints import leagueleaders, leaguestandingsv3, teamgamelog
from nba_api.stats.static import teams
import pandas as pd
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent() / "data" / "raw"
DATA_DIR.mkdir(parents = True, exist_ok = True)

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
    log = teamgamelog.TeamGameLog(team_id=team["id"], season="2024-25")
    df = log.get_data_frames()[0]
    df["TEAM_NAME"] = team["full_name"]
    all_logs.append(df)
    time.sleep(0.6)

combined = pd.concat(all_logs, ignore_index=True)
combined.to_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/game_logs.csv", index=False)

standings = leaguestandingsv3.LeagueStandingsV3(season="2024-25")
df = standings.get_data_frames()[0]
df.to_csv("/Users/julianorozco/PycharmProjects/NBA/data/raw/standings.csv", index=False)
