# Secure MLOps Pipeline for AI Model Deployment

DSP Micro Project – Data Security and Privacy (22AI73)

## Project
A small academic MLOps prototype that trains a Random Forest classifier on the UCI Rice (Cammeo and Osmancik) dataset and adds basic security controls across the ML lifecycle.

## Pipeline
Dataset → Validation → Training → Testing → FastAPI → Docker → GitHub Actions

## Security controls
- Dataset validation
- Prediction input validation
- No hardcoded application secrets
- Python security scanning with Bandit
- Dependency vulnerability scanning with pip-audit
- Basic repository secret-pattern check
- Non-root Docker container

## Run locally

```bash
pip install -r requirements.txt
python download_data.py
python src/validate_data.py
python src/train.py
uvicorn api.app:app --reload
```

Open http://127.0.0.1:8000/docs

## Dataset
UCI Rice (Cammeo and Osmancik), dataset ID 545.
Source: https://archive.ics.uci.edu/dataset/545/rice+cammeo+and+osmancik
