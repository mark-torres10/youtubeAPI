"""Airflow DAG for updating DB with latest integration data."""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.integrations.sync_integrations import main as sync_integrations_main
from transformations.main import main as transformations_main

default_args = {
    'owner': 'default',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_data_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

def run_sync_integrations():
    sync_integrations_main()

def run_transformations():
    transformations_main()

task_sync_integrations = PythonOperator(
    task_id='sync_integrations',
    python_callable=run_sync_integrations,
    dag=dag,
)

task_transformations = PythonOperator(
    task_id='transformations',
    python_callable=run_transformations,
    dag=dag,
)

task_sync_integrations >> task_transformations

if __name__ == "__main__":
    dag.cli()
