# ============================================================
# FINANCIAL FRAUD RISK INTELLIGENCE DASHBOARD
# PURPOSE:
# Build an interactive Streamlit dashboard for monitoring
# future-period fraud risk and prioritizing investigations.
# ============================================================


# ============================================================
# STEP 1 — IMPORT REQUIRED LIBRARIES
# PURPOSE:
# Import libraries required for data loading, processing,
# and dashboard visualization.
# ============================================================

from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# STEP 2 — PAGE CONFIGURATION
# PURPOSE:
# Configure the title, icon, and wide layout of the dashboard.
# ============================================================

st.set_page_config(
    page_title="Financial Fraud Risk Intelligence",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# STEP 3 — PROJECT PATHS
# PURPOSE:
# Define the project root and locations of processed datasets.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DASHBOARD_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dashboard"
    / "presentation"
)

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


# ============================================================
# STEP 4 — LOAD PRESENTATION DATASETS
# PURPOSE:
# Load the aggregated datasets used for dashboard KPIs,
# charts, trends, risk analysis, and priority analysis.
# ============================================================

kpi_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "kpi_dashboard.parquet"
)

fraud_type_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "fraud_type_dashboard.parquet"
)

risk_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "risk_dashboard.parquet"
)

priority_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "priority_dashboard.parquet"
)

fraud_trend_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "fraud_trend_dashboard.parquet"
)

investigation_dashboard = pd.read_parquet(
    DASHBOARD_DATA / "investigation_dashboard.parquet"
)


# ============================================================
# STEP 5 — LOAD FULL RISK-SCORED TEST DATA
# PURPOSE:
# Load the complete future-period transaction population so
# investigation filters can operate on all transactions rather
# than only on a pre-filtered presentation table.
# ============================================================

risk_scored_test = pd.read_parquet(
    PROCESSED_DATA / "fraud_risk_scored_test.parquet"
)


# ============================================================
# STEP 6 — LOAD AUTHORITATIVE INVESTIGATION QUEUE
# PURPOSE:
# Load the actual investigation queue containing the
# authoritative investigation alert and priority assignments.
# ============================================================

investigation_queue = pd.read_parquet(
    PROCESSED_DATA / "investigation_queue.parquet"
)


# ============================================================
# STEP 7 — DEFINE INVESTIGATION MATCHING KEYS
# PURPOSE:
# Identify the transaction-level fields used to connect the
# full scored dataset with the investigation queue.
# ============================================================

investigation_keys = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "nameDest"
]


# ============================================================
# STEP 8 — PREPARE INVESTIGATION FIELDS
# PURPOSE:
# Keep only the investigation information needed from the
# authoritative investigation queue.
# ============================================================

investigation_fields = investigation_queue[
    investigation_keys
    + [
        "investigation_alert",
        "investigation_priority"
    ]
].copy()


# ============================================================
# STEP 9 — MERGE INVESTIGATION INFORMATION
# PURPOSE:
# Attach investigation alert and priority information to the
# complete future-period risk-scored transaction dataset.
# ============================================================

risk_scored_with_investigation = risk_scored_test.merge(
    investigation_fields,
    on=investigation_keys,
    how="left"
)


# ============================================================
# STEP 10 — STANDARDIZE INVESTIGATION ALERT
# PURPOSE:
# Convert missing investigation alerts into zero so that
# transactions outside the investigation queue are clearly
# identified as non-investigation transactions.
# ============================================================

risk_scored_with_investigation[
    "investigation_alert"
] = (
    risk_scored_with_investigation[
        "investigation_alert"
    ]
    .fillna(0)
    .astype(int)
)


# ============================================================
# STEP 11 — SIDEBAR FILTERS
# PURPOSE:
# Create interactive filters for transaction type,
# operational risk category, and investigation priority.
# ============================================================

st.sidebar.header(
    "Investigation Filters"
)


selected_types = st.sidebar.multiselect(
    "Transaction Type",
    options=sorted(
        risk_scored_with_investigation.loc[
            risk_scored_with_investigation[
                "investigation_alert"
            ] == 1,
            "type"
        ]
        .dropna()
        .unique()
    ),
    default=[]
)


selected_risk_categories = st.sidebar.multiselect(
    "Risk Category",
    options=sorted(
        risk_scored_with_investigation.loc[
            risk_scored_with_investigation[
                "investigation_alert"
            ] == 1,
            "operational_risk_category"
        ]
        .dropna()
        .unique()
    ),
    default=[]
)


selected_priorities = st.sidebar.multiselect(
    "Investigation Priority",
    options=sorted(
        risk_scored_with_investigation.loc[
            risk_scored_with_investigation[
                "investigation_alert"
            ] == 1,
            "investigation_priority"
        ]
        .dropna()
        .unique()
    ),
    default=[]
)


# ============================================================
# STEP 12 — CREATE BASE INVESTIGATION POPULATION
# PURPOSE:
# Start filtering from all transactions that actually belong
# to the authoritative investigation queue.
# ============================================================

filtered_risk_data = (
    risk_scored_with_investigation[
        risk_scored_with_investigation[
            "investigation_alert"
        ] == 1
    ]
    .copy()
)


# ============================================================
# STEP 13 — APPLY TRANSACTION TYPE FILTER
# PURPOSE:
# Filter the investigation population by transaction type.
# ============================================================

if selected_types:

    filtered_risk_data = filtered_risk_data[
        filtered_risk_data["type"].isin(
            selected_types
        )
    ]


# ============================================================
# STEP 14 — APPLY RISK CATEGORY FILTER
# PURPOSE:
# Filter the investigation population by operational risk.
# ============================================================

if selected_risk_categories:

    filtered_risk_data = filtered_risk_data[
        filtered_risk_data[
            "operational_risk_category"
        ].isin(
            selected_risk_categories
        )
    ]


# ============================================================
# STEP 15 — APPLY INVESTIGATION PRIORITY FILTER
# PURPOSE:
# Filter the investigation population by investigation priority.
# ============================================================

if selected_priorities:

    filtered_risk_data = filtered_risk_data[
        filtered_risk_data[
            "investigation_priority"
        ].isin(
            selected_priorities
        )
    ]


# ============================================================
# STEP 16 — SORT INVESTIGATION DATA
# PURPOSE:
# Rank the currently filtered investigation population from
# highest to lowest risk score.
# ============================================================

filtered_risk_data = filtered_risk_data.sort_values(
    "risk_score",
    ascending=False
)


# ============================================================
# STEP 17 — CREATE TOP-RISK INVESTIGATION QUEUE
# PURPOSE:
# Display the 100 highest-risk transactions from the currently
# filtered investigation population.
# ============================================================

filtered_investigation_dashboard = (
    filtered_risk_data
    .head(100)
    .copy()
)


# ============================================================
# STEP 18 — PREPARE INVESTIGATION TABLE
# PURPOSE:
# Show only the business-relevant fields in the investigation
# queue instead of exposing every raw modelling column.
# ============================================================

investigation_display_columns = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "nameDest",
    "fraud_probability",
    "risk_score",
    "operational_risk_category",
    "investigation_alert",
    "investigation_priority",
    "risk_reasons"
]


filtered_investigation_dashboard = (
    filtered_investigation_dashboard[
        [
            column
            for column in investigation_display_columns
            if column in filtered_investigation_dashboard.columns
        ]
    ]
    .rename(
        columns={
            "step": "Step",
            "type": "Transaction Type",
            "amount": "Amount",
            "nameOrig": "Origin Account",
            "nameDest": "Destination Account",
            "fraud_probability": "Fraud Probability",
            "risk_score": "Risk Score",
            "operational_risk_category": "Risk Category",
            "investigation_alert": "Investigation Alert",
            "investigation_priority": "Investigation Priority",
            "risk_reasons": "Risk Reasons"
        }
    )
)


# ============================================================
# STEP 19 — DASHBOARD HEADER
# PURPOSE:
# Display the dashboard title and business purpose.
# ============================================================

st.title(
    "Financial Fraud Risk Intelligence Dashboard"
)

st.markdown(
    """
    **Future-period transaction monitoring and investigation prioritization**
    """
)

st.divider()


# ============================================================
# STEP 20 — EXECUTIVE RISK OVERVIEW
# PURPOSE:
# Display the main fraud, risk, and investigation KPIs.
# ============================================================

st.subheader(
    "Executive Risk Overview"
)


kpi_values = dict(
    zip(
        kpi_dashboard["metric"],
        kpi_dashboard["display_value"]
    )
)


# First KPI row
col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Transactions",
        kpi_values["Total Transactions"]
    )


with col2:

    st.metric(
        "Fraud Transactions",
        kpi_values["Fraud Transactions"]
    )


with col3:

    st.metric(
        "Fraud Rate",
        kpi_values["Fraud Rate"]
    )


with col4:

    st.metric(
        "Fraud Amount",
        kpi_values["Fraud Amount"]
    )


# Second KPI row
col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        "Investigation Alerts",
        kpi_values["Investigation Alerts"]
    )


with col6:

    st.metric(
        "Investigation Rate",
        kpi_values["Investigation Rate"]
    )


with col7:

    st.metric(
        "High/Critical Transactions",
        kpi_values["High/Critical Transactions"]
    )


with col8:

    st.metric(
        "Fraud Capture Rate",
        kpi_values["Fraud Capture Rate"]
    )


st.divider()


# ============================================================
# STEP 21 — FRAUD RATE BY TRANSACTION TYPE
# PURPOSE:
# Compare fraud rates across transaction types.
# ============================================================

st.subheader(
    "Fraud Rate by Transaction Type"
)

st.bar_chart(
    fraud_type_dashboard,
    x="Transaction Type",
    y="Fraud Rate %"
)

st.caption(
    "Observed fraud rate across transaction types in the "
    "future-period test dataset."
)

st.divider()


# ============================================================
# STEP 22 — FRAUD RATE TREND
# PURPOSE:
# Show fraud-rate movement across the future-period test window.
# ============================================================

st.subheader(
    "Fraud Rate Trend Over Time"
)

st.line_chart(
    fraud_trend_dashboard,
    x="Step",
    y="Fraud Rate %"
)

st.caption(
    "Fraud-rate movement across the future-period test window. "
    "Short-lived spikes should be interpreted alongside "
    "transaction volume."
)

st.divider()


# ============================================================
# STEP 23 — OPERATIONAL RISK DISTRIBUTION
# PURPOSE:
# Display transaction distribution across operational risk
# categories.
# ============================================================

st.subheader(
    "Operational Risk Distribution"
)

st.bar_chart(
    risk_dashboard,
    x="Risk Category",
    y="Transactions"
)

st.caption(
    "Distribution of future-period transactions across "
    "operational risk categories."
)

st.divider()


# ============================================================
# STEP 24 — FRAUD CONCENTRATION BY RISK CATEGORY
# PURPOSE:
# Display fraud transactions captured within each operational
# risk category.
# ============================================================

st.subheader(
    "Fraud Concentration by Risk Category"
)

st.bar_chart(
    risk_dashboard,
    x="Risk Category",
    y="Fraud Transactions"
)

st.caption(
    "Observed fraud transactions captured within each "
    "operational risk category."
)

st.divider()


# ============================================================
# STEP 25 — INVESTIGATION PRIORITY DISTRIBUTION
# PURPOSE:
# Display the overall distribution of transactions across
# investigation priority levels.
# ============================================================

st.subheader(
    "Investigation Priority Distribution"
)

st.bar_chart(
    priority_dashboard,
    x="Investigation Priority",
    y="Transactions"
)

st.caption(
    "Distribution of future-period transactions across "
    "investigation priority levels."
)

st.divider()


# ============================================================
# STEP 26 — FRAUD AMOUNT BY TRANSACTION TYPE
# PURPOSE:
# Display total fraudulent transaction amount by transaction
# type.
# ============================================================

st.subheader(
    "Fraud Amount by Transaction Type"
)

st.bar_chart(
    fraud_type_dashboard,
    x="Transaction Type",
    y="Fraud Amount"
)

st.caption(
    "Total transaction amount associated with observed "
    "fraudulent transactions."
)

st.divider()


# ============================================================
# STEP 27 — TOP-RISK INVESTIGATION QUEUE
# PURPOSE:
# Display the highest-risk 100 transactions after applying
# the currently selected sidebar filters.
# ============================================================

st.subheader(
    "Top-Risk Investigation Queue"
)

st.dataframe(
    filtered_investigation_dashboard,
    width="stretch",
    hide_index=True
)

st.caption(
    f"Showing {len(filtered_risk_data):,} "
    "transactions matching the selected investigation filters. "
    "Displaying the top 100 by risk score."
)

st.divider()


# ============================================================
# STEP 28 — FILTER-AWARE INVESTIGATION WORKLOAD
# PURPOSE:
# Calculate workload metrics from the currently selected
# investigation filters.
# ============================================================

st.subheader(
    "Investigation Workload"
)


investigation_transactions = len(
    filtered_risk_data
)


investigation_fraud = int(
    filtered_risk_data["isFraud"].sum()
)


investigation_amount = (
    filtered_risk_data["amount"].sum()
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Investigation Queue",
        f"{investigation_transactions:,}"
    )


with col2:

    st.metric(
        "Fraud Captured in Queue",
        f"{investigation_fraud:,}"
    )


with col3:

    st.metric(
        "Queue Transaction Amount",
        f"{investigation_amount:,.2f}"
    )


st.caption(
    "Summary of transactions matching the currently selected "
    "investigation filters."
)

st.divider()


# ============================================================
# STEP 29 — FILTER-AWARE PRIORITY WORKLOAD
# PURPOSE:
# Show how the currently filtered investigation workload is
# distributed across P1, P2, P3 and P4.
# ============================================================

st.subheader(
    "Investigation Workload by Priority"
)


priority_workload = (
    filtered_risk_data
    .groupby(
        "investigation_priority"
    )
    .size()
    .reset_index(
        name="Transactions"
    )
)


priority_workload = (
    priority_workload
    .rename(
        columns={
            "investigation_priority":
            "Investigation Priority"
        }
    )
    .sort_values(
        "Transactions",
        ascending=False
    )
)


if not priority_workload.empty:

    st.bar_chart(
        priority_workload,
        x="Investigation Priority",
        y="Transactions"
    )

else:

    st.info(
        "No investigation transactions match the selected "
        "filters."
    )


st.caption(
    "Number of transactions assigned to each investigation "
    "priority level within the currently filtered workload."
)

st.divider()


# ============================================================
# STEP 30 — DATASET LOADING VERIFICATION
# PURPOSE:
# Confirm that all required dashboard datasets were loaded
# successfully.
# ============================================================

st.success(
    "Dashboard datasets loaded successfully."
)


loaded_datasets = [
    kpi_dashboard,
    fraud_type_dashboard,
    risk_dashboard,
    priority_dashboard,
    fraud_trend_dashboard,
    investigation_dashboard,
    risk_scored_test,
    investigation_queue
]


st.write(
    f"""
    **Loaded datasets:** {len(loaded_datasets)}
    """
)