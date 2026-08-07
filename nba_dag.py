#imports DAG (pipeline blueprint)
#DAG is the class I use to define the pipeline
#blueprint that holds all the tasks and their schedule
from airflow import DAG
#imports BashOperator (runs terminal command)
#This allows each task inside the DAG to run a terminal command
#when airflow runs the pipeline, it uses BashOperator to execute commands like python3 main.py as if I typed them in the terminal myself
from airflow.operators.bash import BashOperator
#imports datetime (for setting the start date)
from datetime import datetime

#default settings that apply to every task in the DAG. start_date tell Airflow when the pipeline became active
#start_date doesn't really matter when it's set as long as catchup = false
#if catchup = true, start_date would matter more because it would try to make up for every day before today and hammer the API and take forever
default_args = {
    'owner': 'julianorozco',
    "start_date": datetime(2025, 1, 1),
}

#Essentially, do these tasks in this order on this schedule
#Creates the dag with:
#dag_id - the name you see in the Airflow UI
#default_args=default_args - these settings apply to every task in the DAG
#schedule=@daily - run automatically every day
#catchup=false - don't try to run all missed days since the start date
#as dag - gives DAG a variable name for reference if needed later
with (DAG(
    dag_id = "nba_pipeline",
    default_args = default_args,
    schedule = "@daily",
    catchup = False,
    ) as dag):

#a task that runs the phase 1 script - pulls data from the NBA api and saves CSV's
#using BashOperator() is like telling python to type into the terminal directly
#saves the task_id as fetch_data in the Dag UI
#bash_command basically a terminal command telling it to run main.py to extract the data
    fetch_data = BashOperator(
        task_id = "fetch_data",
        bash_command = "python3 /Users/julianorozco/PycharmProjects/NBA/main.py",
    )

#a task that runs the phase 2 script - reads the CSV's and loads them into PostgreSQL
    load_data = BashOperator(
        task_id = "load_data",
        bash_command = "python3 /Users/julianorozco/PycharmProjects/NBA/load.py",
    )

#a task that runs dbt - recreates your clean views on top of the fresh data
#--project-dir tells dbt where to find your dbt project, in this case nba_transforms.
#without it dbt wouldn't know where your SQL models and dbt_project.yml are located
    run_dbt = BashOperator(
        task_id = "run_dbt",
        bash_command = "/Users/julianorozco/Library/Python/3.13/bin/dbt run --project-dir /Users/julianorozco/PycharmProjects/NBA/nba_transforms",
    )