"""Final technical audit for the Capstone project."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "requirements.txt",
    "data/master/master_dataset_features.csv",
    "models/model_comparison.csv",
    "models/model_registry.json",
    "docs/reports/05-model-evaluation-report.md",
    "src/ai/train_and_evaluate.py",
    "src/ai/inference.py",
    "src/backend/api.py",
]


def main() -> int:
    failures = []
    for rel in REQUIRED_FILES:
        path = PROJECT_ROOT / rel
        if not path.exists() or path.stat().st_size == 0:
            failures.append(f"Missing or empty: {rel}")

    if (PROJECT_ROOT / "requeriments.txt").exists():
        failures.append("Legacy typo file still exists: requeriments.txt")

    if not failures:
        comparison = pd.read_csv(PROJECT_ROOT / "models" / "model_comparison.csv")
        if len(comparison) < 6:
            failures.append("Expected at least six model candidates in comparison.")
        required_metrics = {
            "name",
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "inconsistency_recall",
            "selection_score",
        }
        if not required_metrics.issubset(comparison.columns):
            failures.append("Model comparison is missing required metrics.")

        registry = json.loads((PROJECT_ROOT / "models" / "model_registry.json").read_text(encoding="utf-8"))
        winner_path = PROJECT_ROOT / registry["winner"]["model_path"]
        if not winner_path.exists():
            failures.append(f"Winner artifact not found: {winner_path}")

    if failures:
        print("TECHNICAL AUDIT FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("TECHNICAL AUDIT PASSED")
    print("All required artifacts are present and internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
