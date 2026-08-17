from typing import Dict

import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
)


def evaluate_model(
    model,
    test_df: pd.DataFrame,
) -> Dict[str, float]:
    """
    Evaluate a trained fraud detection model.

    Parameters
    ----------
    model : trained sklearn model/pipeline
        Trained fraud detection model.

    test_df : pd.DataFrame
        Test dataset containing features and isFraud target.

    Returns
    -------
    Dict[str, float]
        Classification and ranking metrics.
    """

    numerical_features = [
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

    categorical_features = [
        "type"
    ]

    target = "isFraud"

    features = numerical_features + categorical_features

    X_test = test_df[features]
    y_test = test_df[target]

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities
        ),
        "pr_auc": average_precision_score(
            y_test,
            probabilities
        ),
    }

    return metrics


if __name__ == "__main__":

    import joblib

    from src.data_ingestion.load_data import load_raw_data
    from src.data_cleaning.clean_data import clean_data
    from src.feature_engineering.build_features import create_features

    print("Loading test sample...")

    df = load_raw_data(nrows=10000)

    cleaned_df = clean_data(df)

    featured_df = create_features(cleaned_df)

    print("Loading trained model...")

    model = joblib.load(
        "models/fraud_model_pipeline.joblib"
    )

    metrics = evaluate_model(
        model,
        featured_df
    )

    print("\nModel evaluation:")

    for metric_name, value in metrics.items():
        print(
            f"{metric_name.upper():<10}: "
            f"{value:.4f}"
        )