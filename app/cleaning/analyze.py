import pandas as pd

def analyze_csv(df: pd.DataFrame) -> dict:
    return {
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_types": df.dtypes.astype(str).to_dict(),
    }
