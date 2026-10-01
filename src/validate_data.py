from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/rice.csv")

FEATURES = [
    "Area",
    "Perimeter",
    "Major_Axis_Length",
    "Minor_Axis_Length",
    "Eccentricity",
    "Convex_Area",
    "Extent",
]

def validate_dataframe(df: pd.DataFrame) -> list[str]:
    errors = []

    missing_columns = [c for c in FEATURES + ["Class"] if c not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
        return errors

    if df[FEATURES].isnull().any().any():
        errors.append("Missing values detected")

    if not df[FEATURES].apply(lambda s: pd.api.types.is_numeric_dtype(s)).all():
        errors.append("Non-numeric feature detected")

    if (df["Area"] <= 0).any() or (df["Perimeter"] <= 0).any():
        errors.append("Area and Perimeter must be positive")

    if ((df["Eccentricity"] < 0) | (df["Eccentricity"] > 1)).any():
        errors.append("Eccentricity must be between 0 and 1")

    if ((df["Extent"] < 0) | (df["Extent"] > 1)).any():
        errors.append("Extent must be between 0 and 1")

    if df.duplicated().any():
        errors.append("Duplicate records detected")

    if df["Class"].nunique() < 2:
        errors.append("At least two target classes are required")

    return errors

if __name__ == "__main__":
    if not DATA_PATH.exists():
        raise SystemExit("Dataset not found. Run: python download_data.py")

    data = pd.read_csv(DATA_PATH)
    errors = validate_dataframe(data)

    if errors:
        print("DATA VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("DATA VALIDATION PASSED")
    print(f"Rows: {len(data)}")
    print(f"Features: {len(FEATURES)}")
    print(f"Classes: {sorted(data['Class'].unique())}")
