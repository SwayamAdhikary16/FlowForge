from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import os
import logging
from scripts import main as etl_process

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),  # Set your start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'youtube_etl_dag',
    default_args=default_args,
    description='A simple YouTube ETL DAG',
    schedule_interval=timedelta(days=1),  # preferred schedule
)

# Python callable task
def run_etl():
    video_id = "aRcUVhVlSHg"  # default video_id
    try:
        logging.info("Running ETL process...")
        etl_process(video_id)
        logging.info("ETL process completed successfully.")
    except Exception as e:
        logging.error(f"Error during ETL process: {e}")
        raise e

# Task: Run the ETL process
run_etl_task = PythonOperator(
    task_id='run_etl_task',
    python_callable=run_etl,
    dag=dag,
)

run_etl_task
