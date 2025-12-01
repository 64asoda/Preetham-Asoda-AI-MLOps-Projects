from __future__ import annotations

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.utils.dates import days_ago


# AWS Connection
AWS_CONN_ID = "amazon_s3_retail_platform"       # Astro connection id
LOCAL_DATA_DIR = "/usr/local/airflow/data/raw"  # Raw Artifacts location
S3_BUCKET_NAME = "retail-intelligence-data"     # S3 bucket name

# Files List
CSV_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"]

# DAG definition

with DAG(
    dag_id="upload_retail_platform_data_s3",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["s3","ingestion","retail"]
) as dag:
    
    start = EmptyOperator(task_id = "start_upload")
    end = EmptyOperator(task_id = "end_upload")

    previous_task = start
    # List to hold all tasks that must complete before 'end' runs
    validation_tasks = []

    for file_name in CSV_FILES:

        # Upload Task
        upload_task = LocalFilesystemToS3Operator(
            task_id=f"upload_{file_name.replace('.csv','')}", #generate a task_id
            filename=f"{LOCAL_DATA_DIR}/{file_name}",         #location of the files
            dest_key=f"raw/{file_name}",                      #create location in s3 for files
            dest_bucket=S3_BUCKET_NAME,
            aws_conn_id=AWS_CONN_ID,
            replace=True
        )

        # Validation Task
        validate_task = S3KeySensor(
            task_id=f"validate_{file_name.replace('.csv','')}",
            bucket_key=f"raw/{file_name}",
            bucket_name=S3_BUCKET_NAME,
            aws_conn_id=AWS_CONN_ID,
            poke_interval=10,  #check every 10 sec
            timeout=60 * 5,    # timeout = 5 min
            mode="poke"
        )

        # Set dependencies and update chain
        previous_task >> upload_task >> validate_task
        previous_task = validate_task 
        
        # Collect the task for the explicit end link
        validation_tasks.append(validate_task)

    # Final Dependency: Wait for all validation tasks to complete
    validation_tasks >> end