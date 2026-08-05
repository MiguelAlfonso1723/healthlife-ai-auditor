"""Inference utilities for the trained Medical Digital Auditor models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd

from .modeling_config import MODELS_DIR, PROJECT_ROOT, TEXT_COLS
from .train_and_evaluate import build_text


class MedicalAuditorPredictor:
    """Loads the model registry and serves predictions for new records."""

    def __init__(self, registry_path: Path | None = None):
        self.registry_path = registry_path or MODELS_DIR / "model_registry.json"
        self.registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self.winner = self.registry["winner"]
        self.model_name = self.winner["name"]
        self.model_path = PROJECT_ROOT / self.winner["model_path"]
        self.classes = self.registry["classes"]
        self._embedding_model = None
        self._artifact = self._load_artifact()
        self._hybrid_builder = self._load_hybrid_builder()

    def predict_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        df = pd.DataFrame([record])
        return self.predict_dataframe(df)[0]

    def predict_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        df = df.copy()
        for col in TEXT_COLS:
            if col not in df.columns:
                df[col] = ""
        df["texto_clinico"] = build_text(df)

        if self.model_name in {"xgboost_hybrid_sentence", "lightgbm_hybrid_sentence"}:
            x = self._hybrid_matrix(df)
            model = self._artifact["model"]
            pred = model.predict(x).astype(int)
            probabilities = model.predict_proba(x)
            labels = self._load_label_encoder().inverse_transform(pred)
            return self._format_predictions(labels, probabilities)

        if self.model_name == "random_forest_calibrated":
            payload = self._artifact["payload"]
            cols = payload["numeric_cols"] + payload["categorical_cols"]
            labels = self._artifact["model"].predict(df[cols])
            probabilities = self._artifact["model"].predict_proba(df[cols])
            return self._format_predictions(labels, probabilities)

        raise NotImplementedError(f"Inference not implemented for winner {self.model_name}")

    def _load_artifact(self) -> Dict[str, Any]:
        if self.model_path.suffix == ".joblib":
            return joblib.load(self.model_path)
        raise NotImplementedError("Deployment wrapper currently expects a joblib winner.")

    def _load_hybrid_builder(self) -> Dict[str, Any] | None:
        path = MODELS_DIR / "artifacts" / "hybrid_feature_builder.joblib"
        if path.exists():
            return joblib.load(path)
        return None

    def _load_label_encoder(self):
        return joblib.load(MODELS_DIR / "artifacts" / "alert_label_encoder.joblib")

    def _hybrid_matrix(self, df: pd.DataFrame) -> np.ndarray:
        if not self._hybrid_builder:
            raise RuntimeError("Hybrid feature builder artifact is missing.")
        numeric = self._hybrid_builder["numeric_cols"]
        categorical = self._hybrid_builder["categorical_cols"]
        preprocessor = self._hybrid_builder["preprocessor"]
        tabular = preprocessor.transform(df[numeric + categorical])
        embeddings = self._sentence_embeddings(df["texto_clinico"])
        return np.hstack([tabular, embeddings])

    def _sentence_embeddings(self, texts: pd.Series) -> np.ndarray:
        source = self._hybrid_builder.get("embedding_source", "")
        if source.startswith("sentence-transformer-local"):
            if self._embedding_model is None:
                from sentence_transformers import SentenceTransformer

                rel_path = source.split(":", 1)[1]
                self._embedding_model = SentenceTransformer(str(PROJECT_ROOT / rel_path))
            return np.asarray(self._embedding_model.encode(texts.tolist(), batch_size=32, show_progress_bar=False))

        if source.startswith("sentence-transformer"):
            if self._embedding_model is None:
                from sentence_transformers import SentenceTransformer

                model_name = source.split(":", 1)[1]
                self._embedding_model = SentenceTransformer(model_name)
            return np.asarray(self._embedding_model.encode(texts.tolist(), batch_size=32, show_progress_bar=False))

        fallback = joblib.load(MODELS_DIR / "artifacts" / "sentence_embedding_fallback.joblib")
        return fallback["svd"].transform(fallback["tfidf"].transform(texts))

    def _format_predictions(self, labels, probabilities) -> List[Dict[str, Any]]:
        output = []
        for label, probs in zip(labels, probabilities):
            probability_map = {cls: float(prob) for cls, prob in zip(self.classes, probs)}
            output.append(
                {
                    "predicted_alert": str(label),
                    "predicted_status": "CONSISTENTE" if label == "CONSISTENTE" else "INCONSISTENTE",
                    "confidence": float(max(probability_map.values())),
                    "probabilities": probability_map,
                    "model": self.model_name,
                }
            )
        return output


def load_predictor() -> MedicalAuditorPredictor:
    return MedicalAuditorPredictor()
