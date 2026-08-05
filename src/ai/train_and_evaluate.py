"""Train and compare all Capstone AI models.

This script is intentionally executable outside notebooks. It produces the
official model comparison, model registry, saved winner, classification reports,
and confusion matrices used by the evaluation/deployment phases.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib_cache").resolve()))

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from lightgbm import LGBMClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.decomposition import TruncatedSVD
from xgboost import XGBClassifier

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from .modeling_config import (
    CATEGORICAL_COLS,
    CONSISTENT_CLASS,
    DATA_PATH,
    DIAGRAMS_DIR,
    MODELS_DIR,
    NUMERIC_COLS,
    PROJECT_ROOT,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET_COL,
    TEST_SIZE,
    TEXT_COLS,
)


@dataclass
class ModelResult:
    name: str
    family: str
    model_path: str
    embedding_source: str
    fit_seconds: float
    accuracy: float
    balanced_accuracy: float
    macro_f1: float
    weighted_f1: float
    inconsistency_recall: float
    inconsistency_precision: float
    selection_score: float


def ensure_dirs() -> None:
    for path in [
        MODELS_DIR,
        REPORTS_DIR,
        DIAGRAMS_DIR,
        MODELS_DIR / "artifacts",
        REPORTS_DIR / "model_reports",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    missing = [c for c in [TARGET_COL, *TEXT_COLS] if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    return df


def build_text(df: pd.DataFrame) -> pd.Series:
    return (
        df[TEXT_COLS]
        .fillna("")
        .astype(str)
        .agg(" | ".join, axis=1)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def get_feature_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    numeric = [c for c in NUMERIC_COLS if c in df.columns]
    categorical = [c for c in CATEGORICAL_COLS if c in df.columns]
    return numeric, categorical


def make_tabular_preprocessor(numeric: List[str], categorical: List[str]) -> ColumnTransformer:
    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric),
            ("cat", categorical_pipe, categorical),
        ],
        remainder="drop",
        sparse_threshold=0.0,
    )


def metrics_for(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    classes: List[str],
    name: str,
    family: str,
    model_path: str,
    fit_seconds: float,
    embedding_source: str = "none",
) -> ModelResult:
    inconsistent_true = y_true != CONSISTENT_CLASS
    inconsistent_pred = y_pred != CONSISTENT_CLASS
    inc_recall = recall_score(inconsistent_true, inconsistent_pred, zero_division=0)
    inc_precision = precision_score(inconsistent_true, inconsistent_pred, zero_division=0)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    selection_score = (0.45 * macro_f1) + (0.35 * inc_recall) + (0.20 * bal_acc)

    report = classification_report(
        y_true,
        y_pred,
        labels=classes,
        output_dict=True,
        zero_division=0,
    )
    report_path = REPORTS_DIR / "model_reports" / f"{name}_classification_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    cm = confusion_matrix(y_true, y_pred, labels=classes)
    cm_df = pd.DataFrame(cm, index=classes, columns=classes)
    cm_df.to_csv(REPORTS_DIR / "model_reports" / f"{name}_confusion_matrix.csv")
    plot_confusion_matrix(cm_df, name)

    return ModelResult(
        name=name,
        family=family,
        model_path=model_path,
        embedding_source=embedding_source,
        fit_seconds=fit_seconds,
        accuracy=accuracy_score(y_true, y_pred),
        balanced_accuracy=bal_acc,
        macro_f1=macro_f1,
        weighted_f1=f1_score(y_true, y_pred, average="weighted", zero_division=0),
        inconsistency_recall=inc_recall,
        inconsistency_precision=inc_precision,
        selection_score=selection_score,
    )


def plot_confusion_matrix(cm_df: pd.DataFrame, name: str) -> None:
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(f"Confusion Matrix - {name}")
    plt.ylabel("Real")
    plt.xlabel("Predicted")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(DIAGRAMS_DIR / f"{name}_confusion_matrix.png", dpi=160)
    plt.close()


def save_joblib_model(model: Any, name: str, payload: Optional[Dict[str, Any]] = None) -> str:
    path = MODELS_DIR / "artifacts" / f"{name}.joblib"
    joblib.dump({"model": model, "payload": payload or {}}, path)
    return str(path.relative_to(PROJECT_ROOT))


def train_random_forest(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    y_train: np.ndarray,
    y_test: np.ndarray,
    classes: List[str],
) -> ModelResult:
    numeric, categorical = get_feature_columns(train_df)
    pipeline = Pipeline(
        steps=[
            ("preprocess", make_tabular_preprocessor(numeric, categorical)),
            (
                "model",
                CalibratedClassifierCV(
                    estimator=RandomForestClassifier(
                        n_estimators=350,
                        max_depth=None,
                        min_samples_leaf=2,
                        class_weight="balanced_subsample",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                    method="sigmoid",
                    cv=3,
                ),
            ),
        ]
    )
    start = time.time()
    pipeline.fit(train_df[numeric + categorical], y_train)
    pred = pipeline.predict(test_df[numeric + categorical])
    elapsed = time.time() - start
    path = save_joblib_model(
        pipeline,
        "random_forest_calibrated",
        {"numeric_cols": numeric, "categorical_cols": categorical},
    )
    return metrics_for(y_test, pred, classes, "random_forest_calibrated", "tabular", path, elapsed)


def train_tfidf_models(
    train_text: pd.Series,
    test_text: pd.Series,
    y_train: np.ndarray,
    y_test: np.ndarray,
    classes: List[str],
) -> List[ModelResult]:
    results = []
    candidates = {
        "tfidf_logistic_regression": LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=2.0,
            random_state=RANDOM_STATE,
        ),
        "tfidf_linear_svm": CalibratedClassifierCV(
            estimator=LinearSVC(class_weight="balanced", C=1.0, random_state=RANDOM_STATE),
            method="sigmoid",
            cv=3,
        ),
    }
    for name, clf in candidates.items():
        pipeline = Pipeline(
            steps=[
                (
                    "tfidf",
                    TfidfVectorizer(
                        ngram_range=(1, 3),
                        min_df=1,
                        max_features=4000,
                        strip_accents="unicode",
                        sublinear_tf=True,
                    ),
                ),
                ("clf", clf),
            ]
        )
        start = time.time()
        pipeline.fit(train_text, y_train)
        pred = pipeline.predict(test_text)
        elapsed = time.time() - start
        path = save_joblib_model(pipeline, name, {"text_cols": TEXT_COLS})
        results.append(metrics_for(y_test, pred, classes, name, "nlp_tfidf", path, elapsed))
    return results


def sentence_embeddings(train_text: pd.Series, test_text: pd.Series) -> Tuple[np.ndarray, np.ndarray, str]:
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        local_model_dir = MODELS_DIR / "artifacts" / "sentence_transformer_model"
        model.save(str(local_model_dir))
        x_train = model.encode(train_text.tolist(), batch_size=32, show_progress_bar=False)
        x_test = model.encode(test_text.tolist(), batch_size=32, show_progress_bar=False)
        return np.asarray(x_train), np.asarray(x_test), f"sentence-transformer-local:{local_model_dir.relative_to(PROJECT_ROOT)}"
    except Exception as exc:
        print(f"[WARN] SentenceTransformer unavailable, using TF-IDF SVD fallback: {exc}")
        tfidf = TfidfVectorizer(ngram_range=(1, 3), max_features=4000, strip_accents="unicode")
        train_tfidf = tfidf.fit_transform(train_text)
        test_tfidf = tfidf.transform(test_text)
        n_components = min(384, train_tfidf.shape[1] - 1, train_tfidf.shape[0] - 1)
        svd = TruncatedSVD(n_components=max(2, n_components), random_state=RANDOM_STATE)
        x_train = svd.fit_transform(train_tfidf)
        x_test = svd.transform(test_tfidf)
        joblib.dump({"tfidf": tfidf, "svd": svd}, MODELS_DIR / "artifacts" / "sentence_embedding_fallback.joblib")
        return x_train, x_test, "tfidf-svd-fallback"


def train_sentence_classifier(
    x_train_emb: np.ndarray,
    x_test_emb: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    classes: List[str],
    embedding_source: str,
) -> List[ModelResult]:
    results = []
    candidates = {
        "sentence_logistic_regression": LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=2.0,
            random_state=RANDOM_STATE,
        ),
        "sentence_linear_svm": CalibratedClassifierCV(
            estimator=LinearSVC(class_weight="balanced", C=1.0, random_state=RANDOM_STATE),
            method="sigmoid",
            cv=3,
        ),
    }
    for name, clf in candidates.items():
        start = time.time()
        clf.fit(x_train_emb, y_train)
        pred = clf.predict(x_test_emb)
        elapsed = time.time() - start
        path = save_joblib_model(clf, name, {"embedding_source": embedding_source})
        results.append(
            metrics_for(y_test, pred, classes, name, "sentence_embedding_classifier", path, elapsed, embedding_source)
        )
    return results


def make_hybrid_matrix(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    x_train_emb: np.ndarray,
    x_test_emb: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, ColumnTransformer, List[str], List[str]]:
    numeric, categorical = get_feature_columns(train_df)
    preprocessor = make_tabular_preprocessor(numeric, categorical)
    x_train_tab = preprocessor.fit_transform(train_df[numeric + categorical])
    x_test_tab = preprocessor.transform(test_df[numeric + categorical])
    return (
        np.hstack([x_train_tab, x_train_emb]),
        np.hstack([x_test_tab, x_test_emb]),
        preprocessor,
        numeric,
        categorical,
    )


def train_mlp_hybrid(
    x_train: np.ndarray,
    x_test: np.ndarray,
    y_train_enc: np.ndarray,
    y_test: np.ndarray,
    label_encoder: LabelEncoder,
    classes: List[str],
    embedding_source: str,
) -> ModelResult:
    tf.keras.utils.set_random_seed(RANDOM_STATE)
    model = keras.Sequential(
        [
            layers.Input(shape=(x_train.shape[1],)),
            layers.BatchNormalization(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.35),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.25),
            layers.Dense(64, activation="relu"),
            layers.Dense(len(classes), activation="softmax"),
        ]
    )
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    class_weights = class_weight_dict(y_train_enc)
    start = time.time()
    model.fit(
        x_train,
        y_train_enc,
        validation_split=0.2,
        epochs=60,
        batch_size=32,
        class_weight=class_weights,
        callbacks=[keras.callbacks.EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True)],
        verbose=0,
    )
    pred_enc = np.argmax(model.predict(x_test, verbose=0), axis=1)
    pred = label_encoder.inverse_transform(pred_enc)
    elapsed = time.time() - start
    model_path = MODELS_DIR / "artifacts" / "mlp_hybrid_sentence.keras"
    model.save(model_path)
    return metrics_for(
        y_test,
        pred,
        classes,
        "mlp_hybrid_sentence",
        "hybrid_deep_learning",
        str(model_path.relative_to(PROJECT_ROOT)),
        elapsed,
        embedding_source,
    )


def train_cnn_text(
    train_text: pd.Series,
    test_text: pd.Series,
    y_train_enc: np.ndarray,
    y_test: np.ndarray,
    label_encoder: LabelEncoder,
    classes: List[str],
) -> ModelResult:
    tf.keras.utils.set_random_seed(RANDOM_STATE)
    max_tokens = 5000
    sequence_length = 64
    vectorizer = layers.TextVectorization(
        max_tokens=max_tokens,
        output_mode="int",
        output_sequence_length=sequence_length,
        standardize="lower_and_strip_punctuation",
    )
    vectorizer.adapt(train_text.to_numpy())
    model = keras.Sequential(
        [
            layers.Input(shape=(1,), dtype=tf.string),
            vectorizer,
            layers.Embedding(max_tokens, 96),
            layers.Conv1D(128, 3, padding="same", activation="relu"),
            layers.BatchNormalization(),
            layers.Conv1D(96, 5, padding="same", activation="relu"),
            layers.GlobalMaxPooling1D(),
            layers.Dropout(0.35),
            layers.Dense(96, activation="relu"),
            layers.Dropout(0.25),
            layers.Dense(len(classes), activation="softmax"),
        ]
    )
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    start = time.time()
    model.fit(
        train_text.to_numpy(),
        y_train_enc,
        validation_split=0.2,
        epochs=70,
        batch_size=32,
        class_weight=class_weight_dict(y_train_enc),
        callbacks=[keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)],
        verbose=0,
    )
    pred_enc = np.argmax(model.predict(test_text.to_numpy(), verbose=0), axis=1)
    pred = label_encoder.inverse_transform(pred_enc)
    elapsed = time.time() - start
    model_path = MODELS_DIR / "artifacts" / "cnn_1d_textual_real.keras"
    model.save(model_path)
    return metrics_for(
        y_test,
        pred,
        classes,
        "cnn_1d_textual_real",
        "cnn_text",
        str(model_path.relative_to(PROJECT_ROOT)),
        elapsed,
        "keras_text_vectorization",
    )


def class_weight_dict(y_enc: np.ndarray) -> Dict[int, float]:
    values, counts = np.unique(y_enc, return_counts=True)
    total = len(y_enc)
    return {int(v): float(total / (len(values) * c)) for v, c in zip(values, counts)}


def train_boosting_hybrid(
    x_train: np.ndarray,
    x_test: np.ndarray,
    y_train_enc: np.ndarray,
    y_test: np.ndarray,
    label_encoder: LabelEncoder,
    classes: List[str],
    embedding_source: str,
) -> List[ModelResult]:
    results = []
    candidates = {
        "xgboost_hybrid_sentence": XGBClassifier(
            objective="multi:softprob",
            num_class=len(classes),
            n_estimators=220,
            max_depth=4,
            learning_rate=0.045,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="mlogloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "lightgbm_hybrid_sentence": LGBMClassifier(
            objective="multiclass",
            num_class=len(classes),
            n_estimators=280,
            learning_rate=0.045,
            num_leaves=31,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=-1,
        ),
    }
    sample_weight = np.asarray([class_weight_dict(y_train_enc)[int(y)] for y in y_train_enc])
    for name, model in candidates.items():
        start = time.time()
        if name.startswith("xgboost"):
            model.fit(x_train, y_train_enc, sample_weight=sample_weight)
        else:
            model.fit(x_train, y_train_enc)
        pred_enc = model.predict(x_test)
        pred = label_encoder.inverse_transform(pred_enc.astype(int))
        elapsed = time.time() - start
        path = save_joblib_model(model, name, {"embedding_source": embedding_source})
        results.append(metrics_for(y_test, pred, classes, name, "hybrid_boosting", path, elapsed, embedding_source))
    return results


def write_evaluation_report(results_df: pd.DataFrame, registry: Dict[str, Any]) -> None:
    winner = registry["winner"]
    ranking_table = results_df.to_csv(index=False)
    lines = [
        "# EV-01 - Model Evaluation Report",
        "",
        "## Evaluation Protocol",
        "",
        f"- Target: `{TARGET_COL}` multiclass alert classification.",
        f"- Test split: {TEST_SIZE:.0%}, stratified, random_state={RANDOM_STATE}.",
        "- Selection score: 45% macro-F1, 35% inconsistency recall, 20% balanced accuracy.",
        "- Target leakage columns excluded: resultado, tipo_alerta, severidad, descripcion_alerta.",
        "",
        "## Final Ranking",
        "",
        "```csv",
        ranking_table.strip(),
        "```",
        "",
        "## Winner",
        "",
        f"Selected model: `{winner['name']}`.",
        f"Model path: `{winner['model_path']}`.",
        f"Selection score: {winner['selection_score']:.4f}.",
        "",
        "## Deployment Notes",
        "",
        "- Use the registry file `models/model_registry.json` to load the winning artifact.",
        "- The CNN was trained as a real text-sequence Conv1D model using tokenized text, not global embeddings.",
        "- Sentence embedding models use SentenceTransformer when available and fall back to TF-IDF+SVD only if model download/runtime fails.",
    ]
    (REPORTS_DIR / "05-model-evaluation-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    df = load_dataset()
    df["texto_clinico"] = build_text(df)
    y = df[TARGET_COL].astype(str).to_numpy()
    classes = sorted(df[TARGET_COL].astype(str).unique().tolist())

    train_df, test_df, y_train, y_test = train_test_split(
        df,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )
    train_text = train_df["texto_clinico"]
    test_text = test_df["texto_clinico"]

    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    joblib.dump(label_encoder, MODELS_DIR / "artifacts" / "alert_label_encoder.joblib")

    results: List[ModelResult] = []
    results.append(train_random_forest(train_df, test_df, y_train, y_test, classes))
    results.extend(train_tfidf_models(train_text, test_text, y_train, y_test, classes))

    x_train_emb, x_test_emb, embedding_source = sentence_embeddings(train_text, test_text)
    np.save(MODELS_DIR / "artifacts" / "train_sentence_embeddings.npy", x_train_emb)
    np.save(MODELS_DIR / "artifacts" / "test_sentence_embeddings.npy", x_test_emb)
    results.extend(train_sentence_classifier(x_train_emb, x_test_emb, y_train, y_test, classes, embedding_source))

    x_train_hybrid, x_test_hybrid, hybrid_preprocessor, numeric, categorical = make_hybrid_matrix(
        train_df,
        test_df,
        x_train_emb,
        x_test_emb,
    )
    joblib.dump(
        {
            "preprocessor": hybrid_preprocessor,
            "numeric_cols": numeric,
            "categorical_cols": categorical,
            "embedding_source": embedding_source,
        },
        MODELS_DIR / "artifacts" / "hybrid_feature_builder.joblib",
    )
    results.append(
        train_mlp_hybrid(x_train_hybrid, x_test_hybrid, y_train_enc, y_test, label_encoder, classes, embedding_source)
    )
    results.append(train_cnn_text(train_text, test_text, y_train_enc, y_test, label_encoder, classes))
    results.extend(
        train_boosting_hybrid(x_train_hybrid, x_test_hybrid, y_train_enc, y_test, label_encoder, classes, embedding_source)
    )

    results_df = pd.DataFrame([r.__dict__ for r in results]).sort_values(
        ["selection_score", "macro_f1", "inconsistency_recall"],
        ascending=False,
    )
    comparison_path = MODELS_DIR / "model_comparison.csv"
    results_df.to_csv(comparison_path, index=False)

    winner = results_df.iloc[0].to_dict()
    registry = {
        "created_at": pd.Timestamp.now(tz="UTC").isoformat(),
        "target": TARGET_COL,
        "classes": classes,
        "selection_metric": "0.45*macro_f1 + 0.35*inconsistency_recall + 0.20*balanced_accuracy",
        "winner": winner,
        "models": results_df.to_dict(orient="records"),
        "data_path": str(DATA_PATH.relative_to(PROJECT_ROOT)),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    (MODELS_DIR / "model_registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    write_evaluation_report(results_df, registry)
    print(results_df.to_string(index=False))
    print(f"\nWinner: {winner['name']} ({winner['selection_score']:.4f})")


if __name__ == "__main__":
    main()
