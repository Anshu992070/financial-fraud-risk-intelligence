from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "production_fraud_model.joblib"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "test_features.parquet"
)


NUMERICAL_FEATURES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "origin_balance_change",
    "destination_balance_change",
    "amount_to_origin_balance_ratio",
    "origin_balance_zero_flag",
    "amount_exceeds_origin_balance",
]

CATEGORICAL_FEATURES = [
    "type"
]

TARGET = "isFraud"


def evaluate_production_model():

    print("Loading production model...")

    model = joblib.load(
        MODEL_PATH
    )

    print("Loading future test data...")

    test_df = pd.read_parquet(
        TEST_PATH
    )

    features = (
        NUMERICAL_FEATURES
        + CATEGORICAL_FEATURES
    )

    X_test = test_df[features]
    y_test = test_df[TARGET]

    print(
        "Test data:",
        X_test.shape
    )

    # Generate predictions
    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    predictions = (
        probabilities >= 0.50
    ).astype(int)

    # Metrics
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    pr_auc = average_precision_score(
        y_test,
        probabilities
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print("\n" + "=" * 50)
    print("FINAL FUTURE-TEST EVALUATION")
    print("=" * 50)

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print(
        f"ROC-AUC   : {roc_auc:.4f}"
    )

    print(
        f"PR-AUC    : {pr_auc:.4f}"
    )

    print("\nConfusion Matrix:")
    print(cm)

    print("\nFraud transactions:")
    print(int(y_test.sum()))

    print(
        "\nPredicted fraud transactions:"
    )

    print(int(predictions.sum()))

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "confusion_matrix": cm,
    }


if __name__ == "__main__":

    evaluate_production_model()