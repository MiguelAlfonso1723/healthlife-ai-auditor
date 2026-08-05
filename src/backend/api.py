"""FastAPI deployment entrypoint for the Medical Digital Auditor."""

from typing import Any, Dict

from fastapi import FastAPI

from src.ai.inference import load_predictor


app = FastAPI(title="Medical Digital Auditor API", version="1.0.0")
predictor = load_predictor()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "model": predictor.model_name}


@app.post("/predict")
def predict(record: Dict[str, Any]) -> Dict[str, Any]:
    return predictor.predict_record(record)

