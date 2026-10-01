from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "rice_model.pkl"
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Secure Rice Classification API",
    version="1.0"
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
model = joblib.load(MODEL_PATH)

class RiceInput(BaseModel):
    Area: float = Field(gt=0)
    Perimeter: float = Field(gt=0)
    Major_Axis_Length: float = Field(gt=0)
    Minor_Axis_Length: float = Field(gt=0)
    Eccentricity: float = Field(ge=0, le=1)
    Convex_Area: float = Field(gt=0)
    Extent: float = Field(ge=0, le=1)

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/predict")
def predict(data: RiceInput):
    try:
        values = [[
            data.Area,
            data.Perimeter,
            data.Major_Axis_Length,
            data.Minor_Axis_Length,
            data.Eccentricity,
            data.Convex_Area,
            data.Extent,
        ]]
        prediction = model.predict(values)[0]
        return {"prediction": str(prediction)}
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Prediction request rejected"
        ) from exc
