from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from validate_data import FEATURES, validate_dataframe

DATA_PATH = Path("data/rice.csv")
MODEL_DIR = Path("model")
MODEL_PATH = MODEL_DIR / "rice_model.pkl"

df = pd.read_csv(DATA_PATH)
errors = validate_dataframe(df)
if errors:
    raise ValueError("Dataset validation failed: " + "; ".join(errors))

X = df[FEATURES]
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

MODEL_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, predictions))
print(f"Model saved to {MODEL_PATH}")
