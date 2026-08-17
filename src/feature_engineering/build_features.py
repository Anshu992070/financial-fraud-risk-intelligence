import numpy as np
import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create fraud-risk features from transaction data.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned transaction dataset.

    Returns
    -------
    pd.DataFrame
        Dataset containing original columns plus engineered features.
    """

    featured_df = df.copy()

    # Origin account balance change
    featured_df["origin_balance_change"] = (
        featured_df["oldbalanceOrg"]
        - featured_df["newbalanceOrig"]
    )

    # Destination account balance change
    featured_df["destination_balance_change"] = (
        featured_df["newbalanceDest"]
        - featured_df["oldbalanceDest"]
    )

    # Transaction amount relative to origin balance
    featured_df["amount_to_origin_balance_ratio"] = (
        featured_df["amount"]
        / featured_df["oldbalanceOrg"].replace(0, np.nan)
    )

    featured_df["amount_to_origin_balance_ratio"] = (
        featured_df["amount_to_origin_balance_ratio"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    # Whether origin account had zero balance before transaction
    featured_df["origin_balance_zero_flag"] = (
        featured_df["oldbalanceOrg"] == 0
    ).astype(int)

    # Whether transaction amount exceeds origin balance
    featured_df["amount_exceeds_origin_balance"] = (
        featured_df["amount"]
        > featured_df["oldbalanceOrg"]
    ).astype(int)

    return featured_df


if __name__ == "__main__":

    from src.data_ingestion.load_data import load_raw_data
    from src.data_cleaning.clean_data import clean_data

    df = load_raw_data(nrows=1000)

    cleaned_df = clean_data(df)

    featured_df = create_features(cleaned_df)

    print("Original shape:", cleaned_df.shape)
    print("Featured shape:", featured_df.shape)

    print("\nEngineered features:")

    engineered_columns = [
        "origin_balance_change",
        "destination_balance_change",
        "amount_to_origin_balance_ratio",
        "origin_balance_zero_flag",
        "amount_exceeds_origin_balance",
    ]

    print(engineered_columns)

    print("\nFeature preview:")
    print(
        featured_df[
            [
                "amount",
                "oldbalanceOrg",
                "newbalanceOrig",
                "origin_balance_change",
                "destination_balance_change",
                "amount_to_origin_balance_ratio",
                "origin_balance_zero_flag",
                "amount_exceeds_origin_balance",
            ]
        ].head()
    )

    print("\nMissing values in engineered features:")
    print(
        featured_df[engineered_columns].isna().sum()
    )

    print("\nFeature engineering validation successful.")