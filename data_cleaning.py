"""
Task 1: Data Cleaning and Preprocessing
Dataset: Customer Personality Analysis (Kaggle)

Run:
    python data_cleaning.py

The Kaggle file is normally tab-separated. If your CSV is comma-separated,
change sep="\t" to sep="," in load_dataset().
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "dataset" / "marketing_campaign.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "cleaned_dataset.csv"
SUMMARY_FILE = OUTPUT_DIR / "cleaning_summary.txt"


def load_dataset(path: Path) -> pd.DataFrame:
    """Load the Kaggle Customer Personality Analysis dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Download marketing_campaign.csv from Kaggle and place it in the dataset folder."
        )
    # The original Kaggle file is tab-separated despite its .csv extension.
    return pd.read_csv(path, sep="\t")


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Use lowercase, underscores, and remove special characters in headers."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df


def clean_data(df: pd.DataFrame):
    """Clean missing values, duplicates, text, dates, and data types."""
    report = {}
    report["rows_before"] = len(df)
    report["columns_before"] = len(df.columns)
    report["missing_before"] = int(df.isna().sum().sum())
    report["duplicates_before"] = int(df.duplicated().sum())

    # Remove exact duplicate rows (keep the first occurrence).
    df = df.drop_duplicates().copy()
    report["duplicates_removed"] = report["duplicates_before"]

    # Standardize whitespace in text columns. Preserve missing values.
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    for col in text_cols:
        df[col] = df[col].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Convert known numeric columns when present.
    for col in ["income", "year_birth", "recency", "kidhome", "teenhome",
                "mntwines", "mntfruits", "mntmeatproducts", "mntfishproducts",
                "mntsweetproducts", "mntgoldprods", "numdealspurchases",
                "numwebpurchases", "numcatalogpurchases", "numstorepurchases",
                "numwebvisitsmonth", "acceptedcmp1", "acceptedcmp2",
                "acceptedcmp3", "acceptedcmp4", "acceptedcmp5",
                "complain", "z_costcontact", "z_revenue", "response", "id"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert date column if present. Invalid dates become missing values.
    if "dt_customer" in df.columns:
        df["dt_customer"] = pd.to_datetime(
            df["dt_customer"], errors="coerce", dayfirst=True
        )

    # Standardize categorical text without changing the meaning of values.
    # Example: "  graduate " -> "Graduate".
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    for col in text_cols:
        df[col] = df[col].apply(
            lambda value: value.title() if isinstance(value, str) else value
        )

    # Fill numeric missing values with median; categorical with mode.
    # ID is an identifier, so do not invent/fill missing IDs.
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    for col in numeric_cols:
        if col.lower() == "id":
            continue
        if df[col].isna().any():
            median_value = df[col].median()
            if pd.notna(median_value):
                df[col] = df[col].fillna(median_value)

    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    for col in categorical_cols:
        if df[col].isna().any():
            modes = df[col].mode(dropna=True)
            if not modes.empty:
                df[col] = df[col].fillna(modes.iloc[0])

    report["missing_after"] = int(df.isna().sum().sum())
    report["rows_after"] = len(df)
    report["columns_after"] = len(df.columns)
    report["duplicates_after"] = int(df.duplicated().sum())
    return df, report


def save_outputs(df: pd.DataFrame, report: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save dates in a readable, consistent YYYY-MM-DD format.
    export_df = df.copy()
    for col in export_df.select_dtypes(include=["datetime64[ns]"]).columns:
        export_df[col] = export_df[col].dt.strftime("%Y-%m-%d")

    export_df.to_csv(OUTPUT_FILE, index=False)

    summary = f"""DATA CLEANING SUMMARY
=====================

Dataset: Customer Personality Analysis
Rows before cleaning: {report['rows_before']}
Columns before cleaning: {report['columns_before']}
Missing values before cleaning: {report['missing_before']}
Duplicate rows found: {report['duplicates_before']}
Duplicate rows removed: {report['duplicates_removed']}

Rows after cleaning: {report['rows_after']}
Columns after cleaning: {report['columns_after']}
Missing values after cleaning: {report['missing_after']}
Duplicate rows after cleaning: {report['duplicates_after']}

Operations performed:
1. Checked missing values.
2. Removed exact duplicate rows.
3. Trimmed unnecessary leading/trailing spaces in text.
4. Standardized text capitalization.
5. Converted known numeric fields to numeric data types.
6. Converted Dt_Customer to datetime when present.
7. Filled numeric missing values with the median (except ID).
8. Filled categorical missing values with the most frequent value (mode).
9. Standardized column names to lowercase_with_underscores.
10. Exported the cleaned dataset as cleaned_dataset.csv.

Important:
Review the data and this summary before submission. Imputation choices should
be justified for the specific dataset. Missing identifier values are not filled.
"""
    SUMMARY_FILE.write_text(summary, encoding="utf-8")
    print(f"\nCleaned dataset saved to: {OUTPUT_FILE}")
    print(f"Cleaning summary saved to: {SUMMARY_FILE}")


def main():
    print("TASK 1: DATA CLEANING AND PREPROCESSING")
    df = load_dataset(INPUT_FILE)
    df = clean_column_names(df)

    print("\n--- BEFORE CLEANING ---")
    print("Shape:", df.shape)
    print("\nMissing values by column:\n", df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nData types:\n", df.dtypes)

    cleaned_df, report = clean_data(df)

    print("\n--- AFTER CLEANING ---")
    print("Shape:", cleaned_df.shape)
    print("\nMissing values by column:\n", cleaned_df.isna().sum())
    print("\nDuplicate rows:", cleaned_df.duplicated().sum())
    print("\nData types:\n", cleaned_df.dtypes)

    save_outputs(cleaned_df, report)
    print("\nTask completed successfully.")


if __name__ == "__main__":
    main()
