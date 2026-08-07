from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

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
        bash_command="python3 /Users/julianorozco/PycharmProjects/NBA/main.py",
    )

    load_data = BashOperator(
        task_id="load_data",
        bash_command="python3 /Users/julianorozco/PycharmProjects/NBA/load.py",
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="/Users/julianorozco/Library/Python/3.13/bin/dbt run --project-dir /Users/julianorozco/PycharmProjects/NBA/nba_transforms",
    )

    fetch_data >> load_data >> run_dbt
