from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


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


def create_preprocessor():
    """
    Create preprocessing pipeline for numerical
    and categorical features.
    """

    return ColumnTransformer(
        transformers=[
            (
                "numerical",
                StandardScaler(),
                NUMERICAL_FEATURES
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                CATEGORICAL_FEATURES
            )
        ]
    )


def create_logistic_model():
    """
    Create the baseline Logistic Regression pipeline.
    """

    preprocessor = create_preprocessor()

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )


def train_model(
    train_df: pd.DataFrame
):
    """
    Train Logistic Regression fraud model.
    """

    X_train = train_df[
        NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    ]

    y_train = train_df[TARGET]

    model_pipeline = create_logistic_model()

    model_pipeline.fit(
        X_train,
        y_train
    )

    return model_pipeline


if __name__ == "__main__":

    from src.data_ingestion.load_data import load_raw_data
    from src.data_cleaning.clean_data import clean_data
    from src.feature_engineering.build_features import create_features

    print("Loading sample data...")

    df = load_raw_data(nrows=10000)

    cleaned_df = clean_data(df)

    featured_df = create_features(cleaned_df)

    print("Training sample shape:", featured_df.shape)

    model = train_model(featured_df)

    model_path = MODEL_DIR / "fraud_model_pipeline.joblib"

    joblib.dump(
        model,
        model_path
    )

    print("\nModel training successful.")
    print("Model saved to:", model_path)