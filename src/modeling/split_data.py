import pandas as pd


def temporal_split(
    df: pd.DataFrame,
    train_end: int = 323,
    validation_end: int = 378,
):
    """
    Split transaction data chronologically using the step column.

    Train:
        step <= train_end

    Validation:
        train_end < step <= validation_end

    Test:
        step > validation_end
    """

    train = df[
        df["step"] <= train_end
    ].copy()

    validation = df[
        (df["step"] > train_end)
        & (df["step"] <= validation_end)
    ].copy()

    test = df[
        df["step"] > validation_end
    ].copy()

    return train, validation, test


def validate_temporal_split(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
):
    """
    Verify that the three datasets do not overlap temporally.
    """

    train_max = train["step"].max()
    validation_min = validation["step"].min()
    validation_max = validation["step"].max()
    test_min = test["step"].min()

    print("Train:")
    print(train["step"].min(), "→", train_max)

    print("\nValidation:")
    print(validation_min, "→", validation_max)

    print("\nTest:")
    print(test_min, "→", test["step"].max())

    assert train_max < validation_min
    assert validation_max < test_min

    print("\nTemporal split validation successful.")