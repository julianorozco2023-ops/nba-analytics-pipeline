from nba_api.stats.endpoints import leagueleaders, leaguestandingsv3, teamgamelog
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.static import teams
import pandas as pd
import shutil
import time
from pathlib import Path

# Resolve paths from this file's location so the script works on any machine
# and from any working directory (Airflow runs tasks from a temp dir).
DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"
# data/raw/ isn't in the repo (CSVs are gitignored), so create it on first run
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Committed 2023-24 snapshot, used when the NBA API is unavailable
SAMPLE_DIR = Path(__file__).resolve().parent / "data" / "sample"

# stats.nba.com now returns its website instead of JSON when a request claims to
# come from nba.com, so send nba_api's default headers without the Referer.
HEADERS = {k: v for k, v in NBAStatsHTTP.headers.items() if k != "Referer"}

# Seconds to wait for each API response before giving up
TIMEOUT = 30


def use_sample(name, error):
    print(f"Could not fetch {name} from the NBA API ({type(error).__name__}). "
          f"Using sample data from data/sample/{name}.csv instead.")
    shutil.copy(SAMPLE_DIR / f"{name}.csv", DATA_DIR / f"{name}.csv")


all_teams = teams.get_teams()

try:
    leaders = leagueleaders.LeagueLeaders(
        season="2023-24",
        stat_category_abbreviation="PTS",
        per_mode48="PerGame",
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    df = leaders.get_data_frames()[0]
    df.to_csv(DATA_DIR / "player_stats.csv", index=False)
    print("Fetched player_stats from the NBA API.")
except Exception as e:
    use_sample("player_stats", e)

time.sleep(0.6)

# If any team fails, use the sample for all game logs rather than saving a partial season
try:
    all_logs = []
    for team in all_teams:
        log = teamgamelog.TeamGameLog(team_id=team["id"], season="2023-24", headers=HEADERS, timeout=TIMEOUT)
        df = log.get_data_frames()[0]
        df["TEAM_NAME"] = team["full_name"]
        all_logs.append(df)
        time.sleep(0.6)

    combined = pd.concat(all_logs, ignore_index=True)
    combined.to_csv(DATA_DIR / "game_logs.csv", index=False)
    print("Fetched game_logs from the NBA API.")
except Exception as e:
    use_sample("game_logs", e)

try:
    standings = leaguestandingsv3.LeagueStandingsV3(season="2023-24", headers=HEADERS, timeout=TIMEOUT)
    df = standings.get_data_frames()[0]
    df.to_csv(DATA_DIR / "standings.csv", index=False)
    print("Fetched standings from the NBA API.")
except Exception as e:
    use_sample("standings", e)
