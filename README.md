# Financial Fraud Risk Intelligence Platform

An end-to-end financial fraud analytics and risk intelligence platform designed to detect potentially fraudulent transactions, quantify transaction-level risk, classify operational risk, and prioritize transactions for investigation.

The project goes beyond simple fraud prediction by converting model outputs into an operational investigation workflow.

---

## Project Objective

Financial fraud is a highly imbalanced problem where fraudulent transactions represent a very small proportion of overall transaction activity.

The objective of this project is to build a practical fraud-risk intelligence workflow that can:

- Detect potentially fraudulent transactions
- Generate transaction-level fraud probability
- Convert fraud probability into a standardized risk score
- Classify transactions into operational risk categories
- Generate investigation alerts
- Assign investigation priorities
- Quantify financial exposure
- Provide an interactive investigation dashboard
- Support fraud investigators with a prioritized investigation queue

---

## Business Problem

A traditional fraud model may answer:

> "Is this transaction likely to be fraudulent?"

However, a fraud operations team needs to answer additional questions:

- How risky is the transaction?
- Why is it risky?
- How urgent is the investigation?
- Which transactions should investigators review first?
- How much financial exposure is associated with the identified fraud?
- How effectively is the investigation system capturing observed fraud?

This project addresses these questions by connecting predictive fraud signals with an operational risk and investigation framework.

---

## End-to-End Workflow

    Raw Transaction Data
            |
            v
    Data Preparation
            |
            v
    Feature Engineering
            |
            v
    Fraud Risk Modeling
            |
            v
    Fraud Probability
            |
            v
    Risk Score
            |
            v
    Operational Risk Category
            |
            v
    Investigation Alert
            |
            v
    Investigation Priority
            |
            v
    Investigation Queue
            |
            v
    Streamlit Risk Intelligence Dashboard

---

## Project Architecture

    financial-fraud-risk-intelligence/
    |
    |-- app/
    |   |-- dashboard.py
    |
    |-- data/
    |   |-- raw/
    |   |
    |   |-- processed/
    |       |-- dashboard/
    |       |   |-- presentation/
    |       |
    |       |-- fraud_risk_scored_test.parquet
    |       |-- investigation_queue.parquet
    |       |-- test_features.parquet
    |       |-- train_features.parquet
    |       |-- validation_features.parquet
    |
    |-- models/
    |
    |-- notebooks/
    |   |-- 02_feature_engineering.ipynb
    |   |-- 03_fraud_modeling.ipynb
    |
    |-- sql/
    |
    |-- src/
    |
    |-- tests/
    |
    |-- docs/
    |   |-- business_insights.md
    |
    |-- requirements.txt
    |-- README.md

---

## Key Components

### 1. Data Preparation

Transaction-level financial data is prepared for downstream fraud analysis.

The dataset contains transaction information including:

- Transaction step
- Transaction type
- Transaction amount
- Origin account
- Destination account
- Origin account balances
- Destination account balances
- Fraud indicator

---

### 2. Feature Engineering

Transaction-level features are created to capture potentially suspicious financial behavior.

Examples include:

- Origin balance changes
- Destination balance changes
- Amount-to-origin-balance ratio
- Origin balance zero flag
- Amount exceeding origin balance
- Balance-draining behavior

These features provide additional signals beyond the raw transaction fields.

---

### 3. Fraud Risk Modeling

The fraud modeling workflow generates a transaction-level:

**Fraud Probability**

This represents the model's estimated likelihood that a transaction belongs to the fraudulent class.

The probability is subsequently used as an input to the risk-scoring framework.

---

### 4. Risk Scoring

Fraud probability is transformed into a standardized:

**Risk Score**

The risk score provides a more operational interpretation of the model output.

Higher scores represent greater transaction risk.

---

### 5. Operational Risk Classification

Transactions are classified into operational risk categories:

- Critical
- High
- Medium
- Low

This allows fraud teams to distinguish between different levels of operational concern.

---

### 6. Investigation Alert Generation

Transactions selected by the investigation framework are converted into investigation alerts.

The investigation queue contains transactions selected for operational review.

---

### 7. Investigation Prioritization

Investigation alerts are assigned operational priorities:

| Priority | Meaning |
|---|---|
| P1 - Immediate | Highest urgency |
| P2 - High | High-priority investigation |
| P3 - Review | Requires review |
| P4 - Monitor | Lower-priority monitoring |

This creates a practical queue for fraud investigators.

---

# Dashboard

The project includes an interactive Streamlit dashboard designed for fraud-risk monitoring and investigation.

## Executive Risk Overview

The dashboard provides the following executive KPIs:

- Total Transactions
- Fraud Transactions
- Fraud Rate
- Fraud Amount
- Investigation Alerts
- Investigation Rate
- High/Critical Transactions
- Fraud Capture Rate

---

## Fraud Analysis

The dashboard provides:

- Fraud Rate by Transaction Type
- Fraud Rate Trend Over Time
- Fraud Amount by Transaction Type

These views help identify transaction types and periods associated with higher fraud activity or financial exposure.

---

## Risk Analysis

The dashboard provides:

- Operational Risk Distribution
- Fraud Concentration by Risk Category
- Investigation Priority Distribution

These views connect model-level risk with operational risk classification.

---

## Investigation Management

The dashboard provides:

- Transaction Type filter
- Risk Category filter
- Investigation Priority filter
- Top-Risk Investigation Queue
- Investigation Workload
- Investigation Workload by Priority

The investigation queue dynamically responds to the selected filters and displays the highest-risk matching transactions.

---

## Interactive Investigation Queue

The investigation queue provides transaction-level details including:

- Step
- Transaction Type
- Amount
- Origin Account
- Destination Account
- Fraud Probability
- Risk Score
- Risk Category
- Investigation Alert
- Investigation Priority
- Risk Reasons

The queue is sorted by risk score and displays the highest-risk transactions from the filtered investigation population.

---

# Test Dataset Results

The future-period test dataset contains:

| Metric | Result |
|---|---:|
| Total Transactions | 918,617 |
| Fraud Transactions | 4,006 |
| Fraud Rate | 0.44% |
| Fraud Amount | 6,323,046,615.20 |
| Investigation Alerts | 3,998 |
| Investigation Rate | 0.44% |
| High/Critical Transactions | 10,124 |
| Fraud Capture Rate | 99.80% |

---

## Investigation Queue Results

The evaluated investigation queue contains:

| Metric | Result |
|---|---:|
| Investigation Transactions | 3,998 |
| Fraud Transactions in Queue | 3,998 |
| Non-Fraud Transactions in Queue | 0 |
| Investigation Queue Amount | 6,303,392,081.75 |

The investigation framework captured:

**99.80% of observed fraudulent transactions.**

The evaluated investigation queue contained no observed non-fraud transactions.

> Note: The observed results are specific to the evaluated future-period test dataset and should not automatically be interpreted as production performance.

---

## Investigation Priority Distribution

The investigation queue is distributed as follows:

| Priority | Transactions |
|---|---:|
| P1 - Immediate | 3,976 |
| P2 - High | 13 |
| P3 - Review | 6 |
| P4 - Monitor | 3 |
| **Total** | **3,998** |

Approximately **99.45%** of investigation alerts are classified as P1 - Immediate.

This indicates that the current risk framework strongly concentrates identified investigation alerts into the highest-priority category.

---

## Risk Score Distribution

Observed risk-score ranges within the investigation queue:

| Priority | Risk Score Range |
|---|---:|
| P1 - Immediate | 90.20 - 100.00 |
| P2 - High | 70.28 - 88.54 |
| P3 - Review | 45.02 - 69.73 |
| P4 - Monitor | 24.97 - 37.47 |

This creates a quantitative connection between transaction-level risk and investigation urgency.

---

# Key Business Insights

## 1. Fraud is Low Frequency but High Impact

Fraudulent transactions represent only **0.44%** of total transactions but are associated with approximately **6.32 billion** in transaction value.

This demonstrates why fraud monitoring should consider financial exposure in addition to fraud frequency.

---

## 2. Strong Fraud Capture

The investigation framework captured **99.80%** of observed fraudulent transactions in the evaluated future-period test dataset.

This indicates strong coverage within the evaluated period.

---

## 3. Highly Focused Investigation Queue

The system reduced a transaction population of **918,617 transactions** to an investigation queue of **3,998 alerts**.

This provides a significantly more manageable population for operational review.

---

## 4. Investigation Queue Concentration

Approximately **99.45%** of investigation alerts are classified as P1 - Immediate.

This indicates that the current framework heavily concentrates alerts into the highest-priority category.

In a production environment, investigation capacity and alert thresholds should therefore be monitored carefully.

---

## 5. Financial Exposure Matters

Fraud monitoring should not focus only on probability of fraud.

A transaction with both:

- High fraud probability
- High transaction value

can represent significantly greater financial exposure.

---

## 6. CASH_OUT and TRANSFER Require Attention

The analysis identifies CASH_OUT and TRANSFER activity as important areas of fraudulent financial exposure.

High-risk CASH_OUT transactions are particularly prominent within the investigation queue.

---

## 7. Highly Imbalanced Fraud Problem

With 4,006 fraudulent transactions out of 918,617 total transactions, the observed fraud rate is only 0.44%.

This demonstrates why overall accuracy alone is not an appropriate primary measure for evaluating a fraud-risk system.

Operational metrics such as fraud capture rate, investigation precision, financial exposure, and investigation workload are more meaningful.

---

# Business Recommendations

## Recommendation 1 — Risk-Based Investigation

Use risk score and investigation priority to allocate investigation resources.

P1 transactions should receive immediate attention, while lower-priority transactions can be handled through review or monitoring workflows.

---

## Recommendation 2 — Monitor Financial Exposure

Fraud operations should track not only the number of fraudulent transactions but also the monetary value associated with them.

---

## Recommendation 3 — Strengthen CASH_OUT Monitoring

Transactions involving suspicious cash-out behavior should receive enhanced monitoring, particularly when combined with strong fraud-risk signals.

---

## Recommendation 4 — Monitor Investigation Workload

Because the current framework concentrates most investigation alerts into P1, the investigation team should monitor alert volume and operational capacity.

---

## Recommendation 5 — Track Production Metrics

A production fraud-risk system should continuously monitor:

- Fraud capture rate
- Investigation precision
- False-positive rate
- Financial exposure captured
- Investigation workload
- P1/P2 alert volume
- Risk-score distribution
- Model drift

---

# Limitations

The reported results are based on the evaluated future-period test dataset.

The following limitations should be considered:

- Fraud represents only 0.44% of the evaluated transaction population.
- Fraud patterns can change over time.
- The observed investigation precision is specific to this evaluated test dataset.
- The current investigation queue is heavily concentrated in P1 - Immediate.
- Individual transaction-step fraud rates can be volatile when transaction volume is low.
- Production deployment would require continuous monitoring and threshold calibration.
- Model performance should be re-evaluated on future unseen transaction periods.

---

# Technology Stack

- Python
- Pandas
- Streamlit
- Parquet
- Jupyter Notebook
- Git
- GitHub

---

# Running the Dashboard Locally

## 1. Clone the repository

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd financial-fraud-risk-intelligence

## 2. Create and activate the virtual environment

    python -m venv .venv
    source .venv/bin/activate

## 3. Install dependencies

    pip install -r requirements.txt

## 4. Run the Streamlit dashboard

    streamlit run app/dashboard.py

The dashboard will open locally in the browser.

---

# Project Workflow for Interview Discussion

The project can be explained in five major stages:

### Stage 1 — Detect

Identify transactions with potentially fraudulent behavior.

### Stage 2 — Score

Generate fraud probability and convert it into a standardized risk score.

### Stage 3 — Classify

Translate risk scores and transaction signals into operational risk categories.

### Stage 4 — Prioritize

Convert high-risk transactions into investigation alerts and assign P1-P4 investigation priorities.

### Stage 5 — Investigate

Present the prioritized transactions through an interactive dashboard so investigators can focus on the highest-risk cases first.

---

# Why This Project Matters

The key objective of this project is not simply to build a fraud classifier.

It demonstrates how analytical outputs can be converted into a practical business workflow:

    Prediction
        |
        v
    Risk Quantification
        |
        v
    Operational Classification
        |
        v
    Investigation Prioritization
        |
        v
    Business Action

This makes the project relevant to:

- Fraud Analytics
- Risk Analytics
- Financial Services Analytics
- Business Intelligence
- Data Analytics
- Decision Analytics

---

# Future Enhancements

Potential future improvements include:

- Real-time transaction scoring
- Model monitoring
- Threshold optimization
- False-positive analysis
- Investigator feedback loops
- Alert ageing analysis
- Customer-level risk profiling
- Account-level network analysis
- Explainable model predictions
- Automated investigation case management
- Production API deployment
- Model drift detection

---

# Author

**AnshuRaj**

Financial Fraud Risk Intelligence Project

Built as an end-to-end analytics and fraud-risk intelligence portfolio project.