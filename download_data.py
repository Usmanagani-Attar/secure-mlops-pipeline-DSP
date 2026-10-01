from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT = DATA_DIR / "rice.csv"

dataset = fetch_ucirepo(id=545)
X = dataset.data.features.copy()
y = dataset.data.targets.copy()

df = X.copy()
df["Class"] = y.iloc[:, 0].values
df.to_csv(OUTPUT, index=False)

print(f"Saved {len(df)} rows to {OUTPUT}")
print(df.head())
