import os 
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging 
from main import get_latest_comments, clean_comments, textblob_sentiment_analysis
import create_tables
from insert_values import insert_data_into_mysql
from dotenv import load_dotenv


load_dotenv()
yt_api = os.getenv("YT_API")
video_id = os.getenv("YT_VID_ID")

#Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#Instantiate the DAG object
dag = DAG(
    'youtube_etl_dag',
    default_args=default_args,
    description='A simple youtube ETL DAG for sentiment analysis',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 10, 8),
    catchup=False
)

# Task 1: Fetch YouTube comments
def fetch_comments(**kwargs):
    video_id = kwargs['video_id']
    comments = get_latest_comments(video_id, api_key="YOUR_API_KEY")  # Provide your API key here
    logging.info(f"Fetched {len(comments)} comments for video {video_id}")
    return comments

# Task 2: Clean comments
def clean_comments_task(**kwargs):
    comments = kwargs['ti'].xcom_pull(task_ids='fetch_comments')  # Pull from the previous task
    cleaned_comments_df = clean_comments(comments)
    return cleaned_comments_df

# Task 3: Perform sentiment analysis
def sentiment_analysis_task(**kwargs):
    comments_df = kwargs['ti'].xcom_pull(task_ids='clean_comments_task')
    comments_df["Sentiment"] = comments_df["CleanedComment"].apply(textblob_sentiment_analysis)
    return comments_df

# Task 4: Create MySQL tables and insert data
def insert_data_task(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='sentiment_analysis_task')
    create_tables.setup_database()
    insert_data_into_mysql(df, video_id='YOUR_VIDEO_ID')
    logging.info("Data inserted into MySQL")

# PythonOperator for each task
fetch_comments_op = PythonOperator(
    task_id='fetch_comments',
    python_callable=fetch_comments,
    op_kwargs={'video_id': video_id},  # Replace with actual video ID
    provide_context=True,
    dag=dag,
)

clean_comments_op = PythonOperator(
    task_id='clean_comments_task',
    python_callable=clean_comments_task,
    provide_context=True,
    dag=dag,
)

sentiment_analysis_op = PythonOperator(
    task_id='sentiment_analysis_task',
    python_callable=sentiment_analysis_task,
    provide_context=True,
    dag=dag,
)

insert_data_op = PythonOperator(
    task_id='insert_data_task',
    python_callable=insert_data_task,
    provide_context=True,
    dag=dag,
)

# Setting up the task dependencies
fetch_comments_op >> clean_comments_op >> sentiment_analysis_op >> insert_data_op 