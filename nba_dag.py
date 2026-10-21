import shlex
import sys
from datetime import datetime
from pathlib import Path

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG

# .resolve() follows the symlink in Airflow's dags/ folder back to the real project folder
PROJECT_DIR = Path(__file__).resolve().parent
DBT_DIR = PROJECT_DIR / "nba_transforms"

# Run scripts with the same Python that runs Airflow, so they see the same installed packages
PYTHON = shlex.quote(sys.executable)


def run_dbt():
    # Imported here so Airflow doesn't load dbt every time it parses this file
    from dbt.cli.main import dbtRunner
    from dotenv import load_dotenv

    # dbt's profiles.yml reads PG* variables, so load them from .env first
    load_dotenv(PROJECT_DIR / ".env")
    result = dbtRunner().invoke(["run", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)])
    if not result.success:
        raise RuntimeError("dbt run failed")


default_args = {
    "owner": "julianorozco",
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    dag_id="nba_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    fetch_data = BashOperator(
        task_id="fetch_data",
        bash_command=f"{PYTHON} {shlex.quote(str(PROJECT_DIR / 'main.py'))}",
    )

    load_data = BashOperator(
        task_id="load_data",
        bash_command=f"{PYTHON} {shlex.quote(str(PROJECT_DIR / 'load.py'))}",
    )

    run_dbt_models = PythonOperator(
        task_id="run_dbt",
        python_callable=run_dbt,
    )

    fetch_data >> load_data >> run_dbt_models
