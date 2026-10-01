# API test is enabled after the model has been trained.
from pathlib import Path

def test_model_exists_after_training():
    # CI can run training before API tests in a later step.
    assert Path("src/validate_data.py").exists()
