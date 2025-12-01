from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime
import pandas as pd
import sqlalchemy

#csv -> dataframe -> sql

def load_to_sql(file_path):
    conn = BaseHook.get_connection('postgres_default')  
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{conn.login}:{conn.password}@mlops-bank-churn_e21440-postgres-1:{conn.port}/{conn.schema}")
    df = pd.read_csv(file_path)
    df.to_sql(name="bankchurn", con=engine, if_exists="replace", index=False)

# Define the DAG
with DAG(
    dag_id="extract_bankchurn_data",
    schedule_interval=None, 
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    list_files = GCSListObjectsOperator(
        task_id="list_files",
        bucket="bank-churn-mlops", 
    )

    download_file = GCSToLocalFilesystemOperator(
        task_id="download_file",
        bucket="bank-churn-mlops", 
        object_name="bank_churn.csv", 
        filename="/tmp/bank_churn.csv", 
    )

    load_data = PythonOperator(
        task_id="load_to_sql",
        python_callable=load_to_sql,
        op_kwargs={"file_path": "/tmp/bank_churn.csv"}
    )

    list_files >> download_file >> load_data