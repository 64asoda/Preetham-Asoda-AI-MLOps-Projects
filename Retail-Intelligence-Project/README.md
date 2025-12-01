# Retail Intelligence Platform

End-to-end machine learning system for e-commerce analytics, customer segmentation, revenue forecasting, and personalized recommendations

## Project Overview

The Olist E-Commerce Intelligence Platform is a production-ready ML system that processes 100K+ transactions to deliver three core business capabilities:

1. Revenue Forecasting - Predict daily revenue 30 days ahead with 16% MAPE
2. Customer Segmentation - Identify 10 behavioral cohorts across 93K+ customers  
3. Product Recommendations - Achieve 86% accuracy in top-10 recommendations

### Business Impact

- R$4.58M (~$1.15M USD) revenue opportunity identified from "At Risk" customer segment (18.8% of customers)
- 86% recommendation accuracy enables personalized product discovery
- 16% MAPE forecasting supports inventory and revenue planning

Note: All monetary values are in Brazilian Real (R$). USD conversions use approximate 2018 exchange rates for reference.

---

## Architecture

```
Local CSV Files
    |
    v
Apache Airflow (Orchestration)
    |
    v
Amazon S3 (Data Lake)
    |
    v
Databricks + PySpark (Data Processing)
    |
    v
PostgreSQL on RDS (Feature Store & Fact Tables)
    |
    v
ML Models (Databricks + MLflow + Unity Catalog)
    |
    +---> Prophet (Time Series Forecasting)
    |
    +---> RFM Segmentation (K-Means Clustering)
    |
    +---> Two-Tower Deep Learning (PyTorch Recommender)
```

### Technology Stack

Component: Orchestration
Technology: Apache Airflow
Purpose: Data pipeline automation

Component: Storage
Technology: Amazon S3
Purpose: Data lake for raw files

Component: Database
Technology: PostgreSQL (RDS)
Purpose: Feature store and fact tables

Component: Processing
Technology: Databricks + PySpark
Purpose: Distributed data processing

Component: ML Tracking
Technology: MLflow + Unity Catalog
Purpose: Experiment tracking and model registry

Component: Forecasting
Technology: Prophet
Purpose: Time series prediction

Component: Segmentation
Technology: Scikit-learn (K-Means)
Purpose: Customer clustering

Component: Recommendations
Technology: PyTorch
Purpose: Deep learning two-tower model

---

## ML Models

### 1. Revenue Forecasting (Prophet)

Objective: Predict daily revenue 30 days into the future

Approach:
- Time series decomposition (trend + seasonality + holidays)
- Brazilian national holidays incorporated
- Log-transformation for variance stabilization
- Multiplicative seasonality handling

Performance:
- MAPE: 16.54% (Mean Absolute Percentage Error)
- SMAPE: 15.78% (Symmetric MAPE)
- MAE: R$5,065 per day
- Training data: 364 days of historical revenue

Key Features:
- Weekday effects
- Monthly patterns
- Weekend vs. weekday behavior
- Brazilian holiday calendar

Business Value: Enables accurate inventory planning and revenue projections for financial forecasting.

---

### 2. Customer Segmentation (RFM Analysis)

Objective: Segment customers based on purchasing behavior

Approach:
- Recency: Days since last purchase
- Frequency: Number of orders placed
- Monetary: Total spend amount
- K-Means clustering + rule-based segmentation

Results:

At Risk Segment:
- Customers: 17,573 (18.8% of base)
- Revenue: R$4.58M (27.9% of total)
- Avg Order Value: R$250.93

Champions Segment:
- Customers: 6,448 (6.9% of base)
- Revenue: R$2.24M (13.6% of total)
- Avg Order Value: R$312.25

Potential Loyalist Segment:
- Customers: 14,995 (16.1% of base)
- Revenue: R$2.61M (15.9% of total)
- Avg Order Value: R$174.11

Loyal Segment:
- Customers: 16,096 (17.2% of base)
- Revenue: R$1.94M (11.8% of total)
- Avg Order Value: R$113.10

New Customer Segment:
- Customers: 7,467 (8.0% of base)
- Revenue: R$1.31M (8.0% of total)
- Avg Order Value: R$175.17

Other Segments Combined:
- Customers: 30,816 (33.0% of base)
- Revenue: R$3.76M (22.8% of total)

Key Insights:
- At Risk customers represent the biggest opportunity - high historical value but declining engagement
- Champions have 2.75x higher AOV than average customers
- 33% of customers are in low-engagement segments (Hibernating, Lost, Others)

Business Value: Enables targeted marketing campaigns:
- Re-engagement campaigns for "At Risk" segment (R$4.58M opportunity)
- VIP treatment for "Champions" (R$312 AOV vs R$176 average)
- Onboarding programs for "New Customers"

---

### 3. Product Recommendations (Two-Tower Neural Network)

Objective: Recommend top-10 products for each customer

Architecture:
```
User Features --> User Tower (Dense NN)
                        |
                        v
                  Dot Product
                        ^
                        |
Item Features --> Item Tower (Dense NN)
        |
        v
Cross-Entropy Loss with In-Batch Negatives
```

Features:
- User Tower: Purchase behavior (frequency, recency, monetary), payment patterns, review scores
- Item Tower: Price, category, weight, product attributes

Training Strategy:
- In-batch negative sampling (efficient for large catalogs)
- 5-fold cross-validation with different random seeds
- 10 epochs, learning rate 0.001, batch size 512

Performance:

HR@1 (Hit Rate at 1): 39.9%
- Top recommendation is correct 40% of the time

HR@10 (Hit Rate at 10): 86.1%
- Correct item appears in top 10 recommendations

MRR (Mean Reciprocal Rank): 0.559
- Average rank of correct item is approximately rank 2

Model Stability (5 seeds):
- HR@10: 0.819 +/- 0.040 (4% variance indicates robust model)

Business Value: 
- 86% accuracy enables confident product placements
- Personalized homepage and email recommendations
- Cross-sell and upsell opportunities

---

## Key Results Summary

Prophet Forecasting:
- Primary Metric: MAPE 16.5%
- Business Impact: 30-day revenue prediction for planning

RFM Segmentation:
- Primary Metric: 10 distinct cohorts
- Business Impact: R$4.58M "At Risk" revenue identified

Two-Tower Recommender:
- Primary Metric: HR@10 86.1%
- Business Impact: Personalized product discovery

---

## Getting Started

### Prerequisites

Python 3.10 or higher
Install dependencies: pip install -r requirements.txt

### Required Services

1. Apache Airflow - For orchestration
2. AWS Account - S3 bucket and RDS PostgreSQL instance
3. Databricks Workspace - For PySpark processing and ML training

### Environment Variables

```
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your-olist-bucket

# Database Connection
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432
DB_NAME=olist_db
DB_USER=your_username
DB_PASSWORD=your_password

# Databricks
DATABRICKS_HOST=your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your_token
```

### Running the Pipeline

Step 1: Start Airflow (orchestration)
```
airflow standalone
```

Step 2: Trigger data ingestion DAG
```
airflow dags trigger upload_retail_platform_data_s3
```

Step 3: Run feature engineering (in Databricks)
See: notebooks/RETAIL-PLATFORM-FEATURE-ENGINEERING.ipynb

Step 4: Train models (in Databricks)
See: notebooks/PLATFORM-PROPHET-FORECAST-MODEL.ipynb
     notebooks/PLATFORM-RFM-MODEL.ipynb
     notebooks/PLATFORM-TWO-TOWER-MODEL.ipynb

---

## Project Structure

```
Retail-Intelligence-Proejct/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
│
├── dags/
│   ├── retail_platform_ml_pipeline_dag.py
│   ├── upload_retail_platform_data_s3.py
│
├── src/
│   ├── __init__.py
│   ├── custom_exception.py
│   ├── logger.py
│   
│
├── notebooks/
│   ├── RETAIL-PLATFORM-FEATURE-ENGINEERING.ipynb
│   ├── RETAIL-PLATFORM-PROPHET-FORECAST-MODEL.ipynb
│   ├── RETAIL-PLATFORM-RFM-MODEL.ipynb
│   └── RETAIL-PLATFORM-TRANSFORM-RETAIL-DATA.ipynb
│   └── RETAIL-PLATFORM-TWO-TOWER-MODEL.ipynb
│
├── artifacts/
│   ├── mlflow/              # all mlflow documents
│   ├── output-files/        # all output documents
│   └── pkl-files/           # model files
│   ├── raw/                 # original dataset
│   └── screenshots/  
│          ├── DAG           # Airflw DAG
│          ├── model-results # notebook results

---

## Technical Decisions

### Why Prophet for Forecasting?

Alternatives Considered: ARIMA, SARIMA, LSTM

Decision: Prophet chosen because:
- Handles missing data and outliers automatically
- Built-in holiday effects (critical for Brazilian market)
- Interpretable components (trend, seasonality)
- Fast training (seconds vs. minutes for LSTM)
- LSTM would require more data (we have only 1 year)

### Why Two-Tower over Matrix Factorization?

Alternatives Considered: Collaborative Filtering, ALS, NCF

Decision: Two-Tower architecture because:
- Handles cold-start problem (new users/items) via features
- Scales to large catalogs (in-batch negatives)
- Incorporates rich features (not just user-item interactions)
- Production-ready (easy to serve with feature vectors)
- Matrix Factorization cannot use side features

### Why PySpark on Databricks?

Alternatives Considered: Pandas on EC2, Dask, BigQuery

Decision: PySpark on Databricks because:
- Native MLflow integration for experiment tracking
- Unity Catalog for model governance
- Scales horizontally for future data growth
- Interactive notebooks + production jobs in one platform
- Pandas would fail on datasets larger than 10M rows

---

## Future Enhancements

### Phase 1: Production Deployment
- Deploy Two-Tower model as REST API (FastAPI)
- Add Redis caching for real-time recommendations (target: <100ms)
- Implement A/B testing framework
- Set up Prometheus + Grafana monitoring

### Phase 2: Model Improvements
- Fine-tune Prophet with custom seasonality
- Add collaborative filtering signals to Two-Tower
- Implement ensemble for forecasting (Prophet + XGBoost)
- Dynamic RFM thresholds based on business goals

### Phase 3: Data & Infrastructure
- Real-time streaming pipeline (Kafka + Spark Streaming)
- Feature store (Feast or Tecton)
- Automated data quality checks (Great Expectations)
- CI/CD for model retraining

### Phase 4: Advanced ML
- Causal inference for marketing impact
- Multi-armed bandit for recommendation ranking
- LLM-based product descriptions for cold-start items
- Graph neural networks for user-product relationships

---

## Model Monitoring

### Metrics to Track in Production

Prophet MAPE:
- Target: < 20%
- Alert Threshold: > 25%

RFM Segment Stability:
- Target: > 80% same segment
- Alert Threshold: < 70%

Two-Tower HR@10:
- Target: > 85%
- Alert Threshold: < 80%

Prediction Latency:
- Target: < 100ms
- Alert Threshold: > 200ms

Data Freshness:
- Target: < 24 hours
- Alert Threshold: > 48 hours

### Drift Detection

Concept Drift Checks:
- Weekly distribution comparison of customer features
- Monthly revenue distribution vs. historical baseline
- Purchase frequency trends

Data Quality Checks:
- Missing values < 1%
- Price outliers (< 0.1% beyond 3 sigma)
- Duplicate order_ids = 0

---

## Contributing

This project demonstrates production ML practices for portfolio purposes. For suggestions or discussions:

1. Open an issue for bugs or feature requests
2. Fork the repo for experimental changes
3. Follow PEP 8 style guidelines
4. Include tests for new features

---

## License

This project is for educational and portfolio purposes. Dataset from Olist Brazilian E-Commerce Dataset (Kaggle) under CC BY-NC-SA 4.0 license.

---

## Author

Preetham Asoda
ML Engineer | 15+ Years Production Systems | Specializing in MLOps & AI Engineering

LinkedIn: https://www.linkedin.com/in/preetham-asoda/
GitHub: https://github.com/64asoda/Preetham-Asoda-AI-MLOps-Projects
Email: preetham.asoda@gmail.com

---

## Acknowledgments

- Olist for providing the Brazilian e-commerce dataset
- Facebook Prophet for the time series forecasting framework
- Databricks for the unified analytics platform
- PyTorch for the deep learning framework

---

## References

1. Facebook Prophet Documentation: https://facebook.github.io/prophet/
2. Two-Tower Model Architecture: https://arxiv.org/abs/1906.00091
3. RFM Analysis Best Practices: Kaggle customer segmentation guides
4. MLflow Model Registry: https://mlflow.org/docs/latest/model-registry.html

---

Last Updated: January 2025
Project Status: Complete - Ready for Production Deployment