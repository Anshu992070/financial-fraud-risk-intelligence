from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "PS_20174392719_1491204439457_log.csv"
)


def load_raw_data(
    nrows: int | None = None
) -> pd.DataFrame:
    """
    Load the PaySim transaction dataset.

    Parameters
    ----------
    nrows : int | None
        Number of rows to load.
        If None, load the complete dataset.

    Returns
    -------
    pd.DataFrame
        Raw transaction dataset.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    return pd.read_csv(
        RAW_DATA_PATH,
        nrows=nrows
    )


if __name__ == "__main__":
    df = load_raw_data(nrows=5)

    print("Dataset loaded successfully.")
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nPreview:")
    print(df.head())