"""
DP-05 — Data Preprocessing Pipeline.

Pipeline automatizado que ejecuta de forma reproducible todas las etapas
de preparación de datos: limpieza, integración, validación y feature engineering.

Reutiliza exactamente las transformaciones de DP-01, DP-02, DP-03 y DP-04.

Fase: Data Preparation
Proyecto: Healthcare AI Billing Auditor
Metodología: ASUM-DM

Uso:
    python src/data/preprocessing_pipeline.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
DATA_MASTER_PATH = PROJECT_ROOT / "data" / "master"

DATASET_FILES = [
    "01_pacientes.csv",
    "02_atenciones.csv",
    "03_historia_clinica_detalle.csv",
    "04_prefactura.csv",
    "05_cruce_validacion.csv",
]

PK_MAP = {
    "01_pacientes": "id_paciente",
    "02_atenciones": "id_atencion",
    "03_historia_clinica_detalle": "id_detalle",
    "04_prefactura": "id_prefactura",
    "05_cruce_validacion": "id_cruce",
}


# =============================================================================
# STAGE 1: DATA CLEANING (DP-01)
# =============================================================================

def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia columnas de texto: strip y doble espacio."""
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)
        df[col] = df[col].replace("nan", np.nan)
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Estandariza nombres de columnas a snake_case minúsculas."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df


def normalize_types(datasets: dict) -> dict:
    """Normaliza tipos de datos según esquema definido en DP-01."""
    # Pacientes
    df = datasets["01_pacientes"]
    df["edad"] = df["edad"].astype(int)
    df["id_paciente"] = df["id_paciente"].astype(str)

    # Atenciones
    df = datasets["02_atenciones"]
    df["fecha_atencion"] = pd.to_datetime(df["fecha_atencion"])
    df["id_atencion"] = df["id_atencion"].astype(str)
    df["id_paciente"] = df["id_paciente"].astype(str)

    # Historia Clinica
    df = datasets["03_historia_clinica_detalle"]
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    df["cantidad_realizada"] = df["cantidad_realizada"].astype(int)
    df["id_detalle"] = df["id_detalle"].astype(str)
    df["id_atencion"] = df["id_atencion"].astype(str)

    # Prefactura
    df = datasets["04_prefactura"]
    df["fecha_facturacion"] = pd.to_datetime(df["fecha_facturacion"])
    df["cantidad_facturada"] = df["cantidad_facturada"].astype(int)
    df["valor_unitario"] = df["valor_unitario"].astype(int)
    df["valor_total"] = df["valor_total"].astype(int)
    df["id_prefactura"] = df["id_prefactura"].astype(str)
    df["id_atencion"] = df["id_atencion"].astype(str)
    df["id_paciente"] = df["id_paciente"].astype(str)

    # Cruce Validacion
    df = datasets["05_cruce_validacion"]
    df["id_cruce"] = df["id_cruce"].astype(str)
    df["id_atencion"] = df["id_atencion"].astype(str)

    return datasets


def stage_cleaning(base_path: Path) -> dict:
    """Stage 1: Carga y limpieza de datasets (DP-01)."""
    datasets = {}

    for filename in DATASET_FILES:
        filepath = base_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Dataset no encontrado: {filepath}")

        name = filename.replace(".csv", "")
        df = pd.read_csv(filepath)
        df = standardize_column_names(df)
        df = clean_string_columns(df)
        df = df.dropna(how="all")
        df = df.drop_duplicates()
        datasets[name] = df

    datasets = normalize_types(datasets)
    return datasets


# =============================================================================
# STAGE 2: DATA INTEGRATION (DP-02)
# =============================================================================

def stage_integration(datasets: dict) -> pd.DataFrame:
    """Stage 2: Integración de datasets en Master Dataset (DP-02)."""
    # Paso 1: Base cruce_validacion
    master = datasets["05_cruce_validacion"].copy()

    # Paso 2: INNER JOIN atenciones
    master = master.merge(
        datasets["02_atenciones"],
        on="id_atencion",
        how="inner",
        suffixes=("", "_at"),
    )

    # Paso 3: LEFT JOIN pacientes
    master = master.merge(
        datasets["01_pacientes"],
        on="id_paciente",
        how="left",
        suffixes=("", "_pac"),
    )

    # Paso 4: LEFT JOIN historia_clinica
    master = master.merge(
        datasets["03_historia_clinica_detalle"],
        left_on="id_detalle_hc",
        right_on="id_detalle",
        how="left",
        suffixes=("", "_hc"),
    )

    # Paso 5: LEFT JOIN prefactura
    master = master.merge(
        datasets["04_prefactura"],
        on="id_prefactura",
        how="left",
        suffixes=("", "_pf"),
    )

    # Eliminar columnas redundantes
    cols_to_drop = [c for c in master.columns if c.endswith(("_at", "_pac", "_pf"))]
    if "id_detalle" in master.columns:
        cols_to_drop.append("id_detalle")
    cols_to_drop = [c for c in cols_to_drop if c in master.columns]
    master = master.drop(columns=cols_to_drop)

    return master


# =============================================================================
# STAGE 3: VALIDATION (DP-03)
# =============================================================================

def stage_validation(master: pd.DataFrame) -> bool:
    """Stage 3: Validación del Master Dataset (DP-03)."""
    errors = []

    if len(master) != 3126:
        errors.append(f"Registros esperados: 3126, encontrados: {len(master)}")

    if master["id_cruce"].duplicated().sum() > 0:
        errors.append("PK duplicada en id_cruce")

    if master.duplicated().sum() > 0:
        errors.append("Filas duplicadas detectadas")

    if "resultado" not in master.columns:
        errors.append("Variable objetivo 'resultado' no encontrada")

    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        return False

    return True


# =============================================================================
# STAGE 4: FEATURE ENGINEERING (DP-04)
# =============================================================================

def stage_feature_engineering(master: pd.DataFrame) -> pd.DataFrame:
    """Stage 4: Creación de features derivadas (DP-04)."""
    # --- Features Clínicas ---
    master["cups_match"] = (
        master["codigo_cups"].fillna("") == master["codigo_cups_facturado"].fillna("")
    ).astype(int)
    master.loc[
        master["codigo_cups"].isna() & master["codigo_cups_facturado"].isna(),
        "cups_match",
    ] = 0

    master["tiene_soporte_clinico"] = (master["soporte_clinico"] == "SI").astype(int)
    master["procedimiento_facturado"] = master["id_prefactura"].notna().astype(int)
    master["procedimiento_registrado"] = master["id_detalle_hc"].notna().astype(int)
    master["diagnostico_disponible"] = master["diagnostico_principal_cie10"].notna().astype(int)

    master["len_descripcion_diagnostico"] = master["descripcion_diagnostico"].fillna("").str.len()
    master["len_descripcion_hc"] = master["descripcion"].fillna("").str.len()
    master["len_descripcion_servicio"] = master["descripcion_servicio_facturado"].fillna("").str.len()

    # --- Features de Facturación ---
    master["diferencia_cantidad"] = (
        master["cantidad_realizada"].fillna(0) - master["cantidad_facturada"].fillna(0)
    ).astype(int)

    master["cantidad_coincide"] = (master["diferencia_cantidad"] == 0).astype(int)
    master.loc[
        master["cantidad_realizada"].isna() & master["cantidad_facturada"].isna(),
        "cantidad_coincide",
    ] = 0

    master["valor_unitario_disponible"] = master["valor_unitario"].notna().astype(int)
    master["valor_total_disponible"] = master["valor_total"].notna().astype(int)
    master["servicio_facturado"] = master["procedimiento_facturado"]
    master["procedimiento_no_facturado"] = (
        (master["procedimiento_registrado"] == 1) & (master["procedimiento_facturado"] == 0)
    ).astype(int)

    # --- Features Temporales ---
    master["fecha_atencion"] = pd.to_datetime(master["fecha_atencion"], errors="coerce")
    master["fecha_registro"] = pd.to_datetime(master["fecha_registro"], errors="coerce")
    master["fecha_facturacion"] = pd.to_datetime(master["fecha_facturacion"], errors="coerce")

    master["anio_atencion"] = master["fecha_atencion"].dt.year
    master["mes_atencion"] = master["fecha_atencion"].dt.month
    master["trimestre"] = master["fecha_atencion"].dt.quarter
    master["dia_semana"] = master["fecha_atencion"].dt.dayofweek
    master["hora_registro"] = master["fecha_registro"].dt.hour
    master["dias_atencion_facturacion"] = (
        master["fecha_facturacion"] - master["fecha_atencion"]
    ).dt.days

    return master


# =============================================================================
# STAGE 5: EXPORT
# =============================================================================

def stage_export(master: pd.DataFrame, output_path: Path):
    """Stage 5: Exportación del dataset final."""
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / "master_dataset_features.csv"
    master.to_csv(csv_path, index=False)

    parquet_path = output_path / "master_dataset_features.parquet"
    master.to_parquet(parquet_path, index=False)

    return csv_path, parquet_path


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def main():
    """Ejecuta el pipeline completo de Data Preparation."""
    print("\n" + "=" * 50)
    print(" DATA PREPROCESSING PIPELINE")
    print("=" * 50)

    try:
        # Stage 1: Cleaning
        print("\n[1/5] Data Cleaning...")
        datasets = stage_cleaning(DATA_PROCESSED_PATH)
        print("  ✓ Data Cleaning completed")

        # Stage 2: Integration
        print("\n[2/5] Data Integration...")
        master = stage_integration(datasets)
        print(f"  ✓ Data Integration completed ({len(master):,} records)")

        # Stage 3: Validation
        print("\n[3/5] Master Dataset Validation...")
        is_valid = stage_validation(master)
        if not is_valid:
            print("  ✗ Validation FAILED. Pipeline aborted.")
            sys.exit(1)
        print("  ✓ Master Dataset validated")

        # Stage 4: Feature Engineering
        print("\n[4/5] Feature Engineering...")
        master = stage_feature_engineering(master)
        print(f"  ✓ Feature Engineering completed ({master.shape[1]} columns)")

        # Stage 5: Export
        print("\n[5/5] Exporting...")
        csv_path, parquet_path = stage_export(master, DATA_MASTER_PATH)
        print(f"  ✓ Dataset exported")
        print(f"    CSV: {csv_path}")
        print(f"    Parquet: {parquet_path}")

        # Summary
        print("\n" + "=" * 50)
        print(" PIPELINE SUMMARY")
        print("=" * 50)
        print(f"\n  Final Dataset:")
        print(f"    Records: {master.shape[0]:,}")
        print(f"    Columns: {master.shape[1]}")
        print(f"    Original columns: 35")
        print(f"    New features: {master.shape[1] - 35}")
        print(f"\n  ✓ Pipeline finished successfully.")

    except FileNotFoundError as e:
        print(f"\n  ✗ ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n  ✗ UNEXPECTED ERROR: {e}")
        raise

    return master


if __name__ == "__main__":
    main()
