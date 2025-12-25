import pandas as pd
from sklearn.impute import SimpleImputer

def clean_csv(df: pd.DataFrame, steps: list[str]):
    applied = []

    # 1️⃣ REMOVE DUPLICATES
    if "remove_duplicates" in steps:
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        applied.append(f"Removed {before - after} duplicate rows")

    # 2️⃣ SMART MISSING VALUE HANDLING
    if "fill_missing_values" in steps:
        for col in df.columns:

            # Skip if no missing values
            if not df[col].isnull().any():
                continue

            # 🔢 NUMERIC COLUMNS
            if pd.api.types.is_numeric_dtype(df[col]):
                strategy = "median"  # safer than mean
                imputer = SimpleImputer(strategy=strategy)
                df[[col]] = imputer.fit_transform(df[[col]])
                applied.append(f"Filled numeric column '{col}' using {strategy}")

            # 📅 DATE / TIME COLUMNS
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].fillna(method="ffill")
                applied.append(f"Filled date column '{col}' using forward fill")

            # 🔤 TEXT / CATEGORICAL COLUMNS
            else:
                strategy = "most_frequent"
                imputer = SimpleImputer(strategy=strategy)
                df[[col]] = imputer.fit_transform(df[[col]])
                applied.append(f"Filled text column '{col}' using most frequent value")

    return df, applied
