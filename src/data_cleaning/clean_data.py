import pandas as pd


EXPECTED_COLUMNS = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]


def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate that the dataset contains the expected columns.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}"
        )


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Return missing-value counts for each column.
    """

    return df.isna().sum()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean the transaction dataset.
    """

    validate_schema(df)

    cleaned_df = df.copy()

    # Remove completely duplicated transactions
    cleaned_df = cleaned_df.drop_duplicates()

    # Ensure numeric columns have numeric data types
    numeric_columns = [
        "step",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud",
        "isFlaggedFraud",
    ]

    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column],
            errors="coerce"
        )

    return cleaned_df


if __name__ == "__main__":
    from src.data_ingestion.load_data import load_raw_data

    df = load_raw_data(nrows=1000)

    print("Original shape:", df.shape)

    cleaned_df = clean_data(df)

    print("Cleaned shape:", cleaned_df.shape)

    print("\nMissing values:")
    print(check_missing_values(cleaned_df))

    print("\nData cleaning validation successful.")