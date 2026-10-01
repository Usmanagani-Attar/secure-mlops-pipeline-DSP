import pandas as pd
from src.validate_data import FEATURES, validate_dataframe

def valid_dataframe():
    return pd.DataFrame({
        **{feature: [1.0, 2.0] for feature in FEATURES},
        "Eccentricity": [0.5, 0.6],
        "Extent": [0.5, 0.6],
        "Class": ["Cammeo", "Osmancik"],
    })

def test_valid_data():
    assert validate_dataframe(valid_dataframe()) == []

def test_missing_value_rejected():
    df = valid_dataframe()
    df.loc[0, "Area"] = None
    assert "Missing values detected" in validate_dataframe(df)

def test_invalid_eccentricity_rejected():
    df = valid_dataframe()
    df.loc[0, "Eccentricity"] = 1.5
    assert "Eccentricity must be between 0 and 1" in validate_dataframe(df)
