# QA-01 - Technical Audit Report

## Audit Result

Technical audit status: PASSED.

## Verified Items

| Check | Result |
|---|---|
| Python syntax compilation for `src`, `scripts`, `tests` | Passed |
| Validation engine unit tests | 13 passed |
| Required model artifacts exist | Passed |
| Model registry points to a real winner artifact | Passed |
| Model comparison contains all required metrics | Passed |
| Inference wrapper loads the winning model | Passed |
| API module imports successfully | Passed |

## Main Corrections Completed

- Replaced the misspelled `requeriments.txt` with `requirements.txt`.
- Corrected BR-01 to detect both missing billing and mismatched CUPS codes.
- Corrected BR-02 to detect billed services without clinical support or without HC detail.
- Reworked BR-03 into a traceable diagnosis/procedure compatibility validation.
- Built an executable model comparison pipeline outside notebooks.
- Trained all agreed model families with a shared split and shared metrics.
- Packaged the selected model through `model_registry.json`.
- Added offline inference support with a locally saved SentenceTransformer.
- Added FastAPI deployment entrypoint.

## Known Technical Interpretation

The CNN was implemented as a real text-sequence Conv1D model using tokenized clinical text. It was not the winning model, but it is now a valid CNN baseline. The winner outperformed it under the official selection score because the hybrid boosted model uses both tabular validation evidence and semantic text embeddings.

## Verification Commands

```powershell
.\.venv\Scripts\python.exe -m compileall src scripts tests
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe scripts\audit_project.py
```

