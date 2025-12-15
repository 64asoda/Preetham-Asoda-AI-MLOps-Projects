# Bank Churn Project

Features
⦁	Automated ML Pipeline: End-to-end orchestration with Airflow DAGs.
⦁	Data Management: Raw and processed datasets with feature store integration (Redis).
⦁	Model Training: XGBoost-based churn prediction.
⦁	Deployment: Flask web app exposing prediction API.
⦁	Monitoring & Observability: Real-time model performance tracking using Prometheus and Grafana.
⦁	Data Drift Detection: Integrated via Alibi Detect.
⦁	Versioning: Code and data versioning for reproducibility.



Directory Structure

MLOps-Bank-Churn-Project/
│
├─ artifacts/               # Data storage
│   └─ raw/
│       ├─ bankchurn_train.csv
│       └─ bankchurn_test.csv
│
├─ config/                  # Configuration files
│   ├─ database_config.py
│   └─ paths_config.py
│
├─ dags/                    # Airflow DAGs
│   ├─ exampledag.py
│   └─ extract_data_from_gcp.py
│
├─ notebook/                # Jupyter notebooks for experimentation
│
├─ pipeline/                # Training pipelines
│   └─ training_pipeline.py
│
├─ src/                     # Core source code
│   ├─ data_ingestion.py
│   ├─ data_processing.py
│   ├─ feature_store.py
│   ├─ model_training.py
│   ├─ logger.py
│   └─ custom_exception.py
│
├─ static/                  # Static assets
├─ templates/               # HTML templates for Flask app
│   ├─ index.html
│   └─ result.html
│
├─ app.py                   # Flask API
├─ Dockerfile               # Containerization
├─ docker-compose.yml       # Compose file for local deployment
├─ prometheus.yml           # Prometheus monitoring config
├─ requirements.txt
├─ packages.txt
├─ setup.py
└─ airflow_settings.yaml



Workflow

1.	Database Setup: Configure PostgreSQL for feature storage.
2.	Project Setup: Initialize repository, virtual environment, and dependencies.
3.	ETL Data Pipeline: Airflow DAGs handle ingestion, preprocessing, and feature extraction.
4.	Data & Feature Management: Raw data stored in artifacts/raw/, features in Redis feature store.
5.	Model Training: Training pipeline executed via pipeline/training_pipeline.py.
6.	Deployment: Flask API exposes prediction endpoints.
7.	Monitoring: Prometheus & Grafana dashboards for real-time performance and data drift alerts.
8.	Versioning: GitHub repository ensures code versioning; dataset versioning handled via config.



Technology Stack

⦁	Cloud & Orchestration: GCP, Astro Airflow
⦁	Data Storage & Processing: PostgreSQL, Redis, PySpark
⦁	Machine Learning: XGBoost
⦁	Deployment: Flask, Docker, docker-compose
⦁	Monitoring: Prometheus, Grafana
⦁	MLOps Utilities: Alibi Detect for data drift



How to Run

1.	Clone repository and install dependencies:

    git clone <repo-url>
    cd MLOps-Bank-Churn-Project
    pip install -r requirements.txt


2. Start Airflow:

    airflow db init
    airflow webserver -p 8080
    airflow scheduler

3. Launch API

    python app.py

4. Monitor model performance via Prometheus/Grafana dashboards.



Outcome

⦁	Fully automated pipeline processing 10K+ customer records end-to-end.

⦁	Real-time observability and early detection of data drift.

⦁	Scalable and reproducible MLOps workflow ready for enterprise deployment.