# NBA Analytics Pipeline

An end-to-end project that extracts live NBA stats, loads them into PostgreSQL, transforms them with dbt, orchestrates the pipeline with Airflow, and serves the results through a Streamlit dashboard.

---

## Stack

| Tool | Role |
|---|---|
| Python | Extraction scripts and data loading |
| NBA API | Data source (player stats, standings, game logs) |
| Pandas | DataFrame manipulation |
| PostgreSQL | Data warehouse |
| SQLAlchemy | Python-to-database connection |
| dbt | SQL transformations |
| Apache Airflow | Pipeline orchestration and scheduling |
| Streamlit | Interactive dashboard |

---

## Architecture

```
NBA API
   ↓
Python (extract) → CSVs
   ↓
PostgreSQL (raw tables: player_stats, standings, game_logs)
   ↓
dbt (SQL models → views: top_scorers, team_records, team_game_logs)
   ↓
Streamlit Dashboard
   ↓
Airflow (schedules all of the above daily)
```

---

## What It Does

- Pulls current season player stats, team standings, and full game logs for all 30 teams from the NBA API
- Loads the raw data into a PostgreSQL database
- Uses dbt to transform the raw tables into three clean, analysis-ready views:
  - `top_scorers` — top 25 players ranked by points per game
  - `team_records` — all 30 teams ranked by win percentage
  - `team_game_logs` — every game played this season by every team
- Serves the views in an interactive Streamlit dashboard
- Runs the full pipeline automatically every day via an Airflow DAG

---

## Project Structure

```
NBA/
├── main.py              # Phase 1: Extract data from NBA API → CSVs
├── load.py              # Phase 2: Load CSVs into PostgreSQL
├── dashboard.py         # Phase 4: Streamlit dashboard
├── data/raw/            # Raw CSV files (gitignored)
├── nba_transforms/      # dbt project
│   └── models/nba/
│       ├── sources.yml
│       ├── top_scorers.sql
│       ├── team_records.sql
│       └── team_game_logs.sql
└── nba_dag.py       # Airflow DAG definition
```

---

## How to Run Locally

### Prerequisites
- Python 3.13
- PostgreSQL 15
- dbt-postgres
- Apache Airflow

### Setup

1. Install dependencies:
```bash
pip3 install nba_api pandas psycopg2 sqlalchemy dbt-postgres apache-airflow streamlit
```

2. Create the database:
```bash
psql postgres -c "CREATE DATABASE nba_pipeline;"
```

3. Extract data:
```bash
python3 main.py
```

4. Load into PostgreSQL:
```bash
python3 load.py
```

5. Run dbt transformations:
```bash
dbt run --project-dir nba_transforms
```

6. Launch the dashboard:
```bash
streamlit run dashboard.py
```

7. Start Airflow (optional, for automated scheduling):
```bash
airflow standalone
```
Then open `http://localhost:8080`, find the `nba_pipeline` DAG and enable it.
