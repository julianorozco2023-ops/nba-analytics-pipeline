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

# Committed snapshot, used when the NBA API is unavailable
SAMPLE_DIR = Path(__file__).resolve().parent / "data" / "sample"
# Season of the CSVs in data/sample/
SAMPLE_SEASON = "2023-24"

# stats.nba.com now returns its website instead of JSON when a request claims to
# come from nba.com, so send nba_api's default headers without the Referer.
HEADERS = {k: v for k, v in NBAStatsHTTP.headers.items() if k != "Referer"}

# Seconds to wait for each API response before giving up
TIMEOUT = 30

# NBA season to fetch, in "YYYY-YY" format
SEASON = "2023-24"


def fetch_player_stats():
    leaders = leagueleaders.LeagueLeaders(
        season=SEASON,
        stat_category_abbreviation="PTS",
        per_mode48="PerGame",
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    return leaders.get_data_frames()[0]


def fetch_game_logs():
    all_logs = []
    for team in teams.get_teams():
        log = teamgamelog.TeamGameLog(team_id=team["id"], season=SEASON, headers=HEADERS, timeout=TIMEOUT)
        df = log.get_data_frames()[0]
        df["TEAM_NAME"] = team["full_name"]
        all_logs.append(df)
        time.sleep(0.6)
    return pd.concat(all_logs, ignore_index=True)


def fetch_standings():
    standings = leaguestandingsv3.LeagueStandingsV3(season=SEASON, headers=HEADERS, timeout=TIMEOUT)
    return standings.get_data_frames()[0]


DATASETS = {
    "player_stats": fetch_player_stats,
    "game_logs": fetch_game_logs,
    "standings": fetch_standings,
}

# Fetch everything into memory before saving anything, so data/raw/ always holds
# one consistent season: either all live data, or all sample data.
try:
    results = {}
    for name, fetch in DATASETS.items():
        results[name] = fetch()
        print(f"Fetched {name} from the NBA API.")
        time.sleep(0.6)
except Exception as e:
    print(f"Could not fetch {name} from the NBA API ({type(e).__name__}). "
          f"Using the {SAMPLE_SEASON} sample data in data/sample/ for all datasets so they match.")
    if SEASON != SAMPLE_SEASON:
        print(f"Warning: SEASON is set to {SEASON}, but the sample data is from {SAMPLE_SEASON}.")
    for name in DATASETS:
        shutil.copy(SAMPLE_DIR / f"{name}.csv", DATA_DIR / f"{name}.csv")
else:
    for name, df in results.items():
        df.to_csv(DATA_DIR / f"{name}.csv", index=False)
    print(f"Saved {SEASON} data from the NBA API to data/raw/.")
