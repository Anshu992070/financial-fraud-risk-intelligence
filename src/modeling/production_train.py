from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline

from src.modeling.train_model import (
    create_logistic_model,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


TRAIN_PATH = DATA_DIR / "train_features.parquet"
VALIDATION_PATH = DATA_DIR / "validation_features.parquet"


def load_training_data():

    train_df = pd.read_parquet(
        TRAIN_PATH
    )

    validation_df = pd.read_parquet(
        VALIDATION_PATH
    )

    return train_df, validation_df


def train_production_model():

    train_df, validation_df = load_training_data()

    features = (
        NUMERICAL_FEATURES
        + CATEGORICAL_FEATURES
    )

    X_train = train_df[features]
    y_train = train_df[TARGET]

    X_validation = validation_df[features]
    y_validation = validation_df[TARGET]

    print("Training data:", X_train.shape)
    print("Validation data:", X_validation.shape)

    model = create_logistic_model()

    print("\nTraining Logistic Regression...")

    model.fit(
        X_train,
        y_train
    )

    print("Training completed.")

    validation_probability = model.predict_proba(
        X_validation
    )[:, 1]

    validation_pr_auc = average_precision_score(
        y_validation,
        validation_probability
    )

    print(
        "\nValidation PR-AUC:",
        round(validation_pr_auc, 4)
    )

    model_path = (
        MODEL_DIR
        / "production_fraud_model.joblib"
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        "\nProduction model saved to:",
        model_path
    )

    return model, validation_pr_auc


if __name__ == "__main__":

    train_production_model()