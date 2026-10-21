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

- Pulls 2023-24 season player stats, team standings, and full game logs for all 30 teams from the NBA API
- Loads the raw data into a PostgreSQL database
- Uses dbt to transform the raw tables into three clean, analysis-ready views:
  - `top_scorers` — top 25 players ranked by points per game
  - `team_records` — all 30 teams ranked by win percentage
  - `team_game_logs` — every game played that season by every team
- Serves the views in an interactive Streamlit dashboard
- Runs the full pipeline automatically every day via an Airflow DAG

---

## Project Structure

```
nba-analytics-pipeline/
├── main.py              # Extract: NBA API → CSVs in data/raw/
├── load.py              # Load: CSVs → PostgreSQL raw tables
├── db.py                # Shared database connection (reads settings from .env)
├── dashboard.py         # Streamlit dashboard
├── nba_dag.py           # Airflow DAG that runs extract → load → dbt daily
├── requirements.txt     # Pinned Python dependencies
├── .env.example         # Template for your database settings
├── data/raw/            # Raw CSV files (created on first run, gitignored)
└── nba_transforms/      # dbt project
    ├── profiles.yml     # dbt connection (reads the same settings from the environment)
    └── models/nba/
        ├── sources.yml
        ├── top_scorers.sql
        ├── team_records.sql
        └── team_game_logs.sql
```

---

## How to Run Locally

### Prerequisites
- Python 3.13
- PostgreSQL 15 or newer, running locally

### Setup

1. Clone the repo and create a virtual environment:
```bash
git clone https://github.com/julianorozco2023-ops/nba-analytics-pipeline.git
cd nba-analytics-pipeline
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your database connection. Copy the template, then edit `.env` with your Postgres username (and password, if your setup uses one):
```bash
cp .env.example .env
```

4. Create the database:
```bash
createdb nba_pipeline
```

### Run the pipeline

Run every command from the project root.

1. Extract data from the NBA API (takes about a minute; it pauses between requests to respect rate limits):
```bash
python main.py
```

2. Load into PostgreSQL:
```bash
python load.py
```

3. Run dbt transformations. dbt doesn't read `.env` on its own, so export the variables into your shell first:
```bash
set -a && source .env && set +a
dbt run --project-dir nba_transforms --profiles-dir nba_transforms
```

4. Launch the dashboard:
```bash
streamlit run dashboard.py
```

### Scheduling with Airflow (optional)

Airflow is installed separately with its official constraints file, which pins compatible versions of its many dependencies. Install it into the same virtual environment so the DAG's tasks can use the pipeline's packages:
```bash
pip install "apache-airflow==3.3.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.3.0/constraints-3.13.txt"
```

Link the DAG into Airflow's DAG folder. Use a symlink rather than a copy, because the DAG locates the project by following the link back to this folder:
```bash
mkdir -p ~/airflow/dags
ln -s "$(pwd)/nba_dag.py" ~/airflow/dags/nba_dag.py
```

Start Airflow:
```bash
airflow standalone
```
Then open `http://localhost:8080`, sign in with the credentials printed in the terminal, find the `nba_pipeline` DAG and enable it.

### Troubleshooting

- **`main.py` fails with `JSONDecodeError`:** stats.nba.com sometimes returns a web page instead of data, usually when it blocks automated requests. This comes from the NBA's side, not the pipeline. Wait and retry, or try from a different network. The rest of the pipeline can still run on CSVs you've already extracted.
- **dbt fails with `role "postgres" does not exist` (or another connection error) while `load.py` works:** dbt isn't seeing your `.env` settings. Run the `set -a && source .env && set +a` line in the same terminal before `dbt run`.
