# DEP-01 - Deployment Readiness Report

## Scope

This report validates the technical deployment package for the Medical Digital Auditor after model comparison and winner selection.

## Packaged Components

| Component | Path | Status |
|---|---|---|
| Model registry | `models/model_registry.json` | Ready |
| Winning model | `models/artifacts/xgboost_hybrid_sentence.joblib` | Ready |
| Local SentenceTransformer | `models/artifacts/sentence_transformer_model` | Ready |
| Hybrid feature builder | `models/artifacts/hybrid_feature_builder.joblib` | Ready |
| Label encoder | `models/artifacts/alert_label_encoder.joblib` | Ready |
| Inference wrapper | `src/ai/inference.py` | Ready |
| FastAPI entrypoint | `src/backend/api.py` | Ready |

## Winner

The selected model is `xgboost_hybrid_sentence`, chosen by the official selection score:

`0.45 * macro_f1 + 0.35 * inconsistency_recall + 0.20 * balanced_accuracy`

This prioritizes multiclass quality and inconsistency detection over raw accuracy.

## API Contract

### Health Check

`GET /health`

Returns service status and active model name.

### Prediction

`POST /predict`

Accepts one record from the master dataset schema and returns:

- `predicted_alert`
- `predicted_status`
- `confidence`
- per-class `probabilities`
- active `model`

## Run Command

```powershell
.\.venv\Scripts\uvicorn.exe src.backend.api:app --host 127.0.0.1 --port 8000
```

## Deployment Notes

- The SentenceTransformer model is saved locally, so inference does not require internet.
- The dashboard can call the API directly once designed.
- The deployment package is currently local/MVP-ready, not hardened for authentication or cloud scaling.

