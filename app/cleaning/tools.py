import pandas as pd

def analyze_csv(df: pd.DataFrame) -> dict:
    """
    Detect common data issues in a CSV file
    """
    report = {}

    # Missing values
    report["missing_values"] = df.isnull().sum().to_dict()

    # Duplicate rows
    report["duplicate_rows"] = int(df.duplicated().sum())

    # Column data types
    report["column_types"] = df.dtypes.astype(str).to_dict()

    # Empty columns
    report["empty_columns"] = [
        col for col in df.columns if df[col].isnull().all()
    ]

    return report
