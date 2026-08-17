from src.data_ingestion.load_data import load_raw_data
from src.data_cleaning.clean_data import clean_data
from src.feature_engineering.build_features import create_features
from src.modeling.train_model import train_model
from src.evaluation.evaluate_model import evaluate_model


SAMPLE_ROWS = 10_000


def main():

    print("=" * 60)
    print("FINANCIAL FRAUD RISK INTELLIGENCE PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # 1. DATA INGESTION
    # --------------------------------------------------

    print("\n[1/5] Loading raw data...")

    df = load_raw_data(
        nrows=SAMPLE_ROWS
    )

    print("Raw data shape:", df.shape)

    # --------------------------------------------------
    # 2. DATA CLEANING
    # --------------------------------------------------

    print("\n[2/5] Cleaning data...")

    cleaned_df = clean_data(df)

    print(
        "Cleaned data shape:",
        cleaned_df.shape
    )

    # --------------------------------------------------
    # 3. FEATURE ENGINEERING
    # --------------------------------------------------

    print("\n[3/5] Creating features...")

    featured_df = create_features(
        cleaned_df
    )

    print(
        "Featured data shape:",
        featured_df.shape
    )

    # --------------------------------------------------
    # 4. MODEL TRAINING
    # --------------------------------------------------

    print("\n[4/5] Training model...")

    model = train_model(
        featured_df
    )

    print(
        "Model trained:",
        type(model).__name__
    )

    # --------------------------------------------------
    # 5. MODEL EVALUATION
    # --------------------------------------------------

    print("\n[5/5] Evaluating model...")

    metrics = evaluate_model(
        model,
        featured_df
    )

    print("\nModel metrics:")

    for metric_name, value in metrics.items():

        print(
            f"{metric_name.upper():<10}: "
            f"{value:.4f}"
        )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()