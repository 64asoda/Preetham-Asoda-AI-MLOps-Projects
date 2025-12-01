"""
Retail Platform ML Pipeline - Databricks Execution DAG
======================================================
Orchestrates ML model training on Databricks after data upload to S3.

This DAG should run AFTER: upload_pc_to_s3_dag.py

Execution Flow:
1. Transform raw data
2. Feature engineering
3. Train Three ML Models (Two-Tower, RFM, Prophet)

Author: Preetham Asoda
Date: December 2025
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago
from datetime import timedelta

# ============================================================
# CONFIGURATION
# ============================================================

# Databricks Connection
DATABRICKS_CONN_ID = "databricks_retail_platform"  # Configure in Airflow UI
DATABRICKS_CLUSTER_ID = "1110-033343-i55cdiq9"  # Replace with your cluster ID

# Notebook paths in Databricks Workspace
TRANSFORM_NOTEBOOK = "/Workspace/Shared/RETAIL-PLATFORM-TRANSFORM-RETAIL-DATA"
FEATURE_ENGINEERING_NOTEBOOK = "/Workspace/Shared/RETAIL-PLATFORM-FEATURE-ENGINEERING"
TWO_TOWER_NOTEBOOK = "/Workspace/Shared/RETAIL-PLATFORM-TWO-TOWER-MODEL"
RFM_NOTEBOOK = "/Workspace/Shared/RETAIL-PLATFORM-RFM-MODEL"
PROPHET_NOTEBOOK = "/Workspace/Shared/RETAIL-PLATFORM-PROPHET-FORECAST-MODEL"

# Default arguments
default_args = {
    'owner': 'ai-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['preetham.asoda@gmail.com	'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ============================================================
# DAG DEFINITION
# ============================================================

with DAG(
    dag_id='retail_platform_ml_pipeline_dag',
    default_args=default_args,
    description='Execute ML models on Databricks after S3 data upload',
    schedule_interval=None,  # Trigger manually or via external trigger
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'databricks', 'retail', 'production'],
    max_active_runs=1,
) as dag:
    
    # --------------------------------------------------------
    # START: Pipeline Initialization
    # --------------------------------------------------------
    start = EmptyOperator(
        task_id='start_ml_pipeline'
    )
    
    # --------------------------------------------------------
    # Wait for S3 Upload DAG to Complete
    # --------------------------------------------------------   
    """
     wait_for_s3_upload = ExternalTaskSensor(
        task_id='wait_for_s3_upload',
        external_dag_id='upload_retail_platform_data_s3',
        external_task_id='end_upload',
        timeout=3600,  # Wait up to 1 hour
        poke_interval=60,  # Check every minute
        mode='poke'
        )
    """
    
    # --------------------------------------------------------
    # TASK 1: Transform Raw Data
    # --------------------------------------------------------
    transform_data = DatabricksSubmitRunOperator(
        task_id='transform_retail_data',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_CLUSTER_ID,
        notebook_task={
            'notebook_path': TRANSFORM_NOTEBOOK,
            'base_parameters': {
                'execution_date': '{{ ds }}',
                's3_bucket': 'retail-intelligence-data',
                's3_prefix': 'raw/'
            }
        },
        timeout_seconds=3600,  # 1 hour timeout
    )
    
    # --------------------------------------------------------
    # TASK 2: Feature Engineering
    # --------------------------------------------------------
    feature_engineering = DatabricksSubmitRunOperator(
        task_id='feature_engineering',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_CLUSTER_ID,
        notebook_task={
            'notebook_path': FEATURE_ENGINEERING_NOTEBOOK,
            'base_parameters': {
                'execution_date': '{{ ds }}',
            }
        },
        timeout_seconds=3600,  # 1 hour timeout
    )
    
    # --------------------------------------------------------
    # TASK 3: Two-Tower Recommender Model
    # --------------------------------------------------------
    two_tower_model = DatabricksSubmitRunOperator(
        task_id='two_tower_model',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_CLUSTER_ID,
        notebook_task={
            'notebook_path': TWO_TOWER_NOTEBOOK,
            'base_parameters': {
                'execution_date': '{{ ds }}',
                'num_epochs': '10',
                'batch_size': '512',
            }
        },
        timeout_seconds=7200,  # 2 hour timeout (deep learning)
    )
    
    # --------------------------------------------------------
    # TASK 4: RFM Customer Segmentation
    # --------------------------------------------------------
    rfm_model = DatabricksSubmitRunOperator(
        task_id='rfm_segmentation',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_CLUSTER_ID,
        notebook_task={
            'notebook_path': RFM_NOTEBOOK,
            'base_parameters': {
                'execution_date': '{{ ds }}',
            }
        },
        timeout_seconds=1800,  # 30 minutes timeout
    )
    
    # --------------------------------------------------------
    # TASK 5: Prophet Forecasting Model
    # --------------------------------------------------------
    prophet_model = DatabricksSubmitRunOperator(
        task_id='prophet_forecasting',
        databricks_conn_id=DATABRICKS_CONN_ID,
        existing_cluster_id=DATABRICKS_CLUSTER_ID,
        notebook_task={
            'notebook_path': PROPHET_NOTEBOOK,
            'base_parameters': {
                'execution_date': '{{ ds }}',
                'forecast_days': '30',
            }
        },
        timeout_seconds=1800,  # 30 minutes timeout
    )
    
    # --------------------------------------------------------
    # END: Pipeline Completion
    # --------------------------------------------------------
    end = EmptyOperator(
        task_id='ml_pipeline_complete'
    )
    
    # --------------------------------------------------------
    # TASK DEPENDENCIES
    # --------------------------------------------------------
    
    # Sequential execution through transform and feature engineering
    start >> transform_data >> feature_engineering
    
    # Parallel execution of three ML models
    feature_engineering >> [two_tower_model, rfm_model, prophet_model] >> end
    
    # If using ExternalTaskSensor
    # start >> wait_for_s3_upload >> transform_data >> ...


# ============================================================
# ALTERNATIVE: Sequential Model Training
# ============================================================
# 
# start >> transform_data >> feature_engineering >> two_tower_model >> rfm_model >> prophet_model >> end
#


# ============================================================
# EXPECTED RUNTIME
# ============================================================

"""
Task                    | Duration  | Notes
------------------------|-----------|---------------------------
transform_data          | 20-30 min | PySpark transformations
feature_engineering     | 15-20 min | Feature creation
two_tower_model         | 45-90 min | Deep learning (longest)
rfm_model               | 5-10 min  | K-Means clustering
prophet_model           | 5-10 min  | Time series forecasting
------------------------|-----------|---------------------------
Total (parallel)        | ~2 hours  | Limited by two_tower_model
Total (sequential)      | ~3 hours  | Sum of all tasks
"""
