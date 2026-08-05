"""
DP-02 — Integrate Healthcare Datasets into a Unified Structure.

Construye el Master Dataset integrando los cinco datasets procesados
siguiendo la estrategia de JOIN definida en AA-02 y DU-04.

Fase: Data Preparation
Proyecto: Healthcare AI Billing Auditor
Metodología: ASUM-DM
"""

import pandas as pd
import numpy as np
from pathlib import Path


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

DATA_PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed"
DATA_INTERMEDIATE_PATH = Path(__file__).parent.parent / "data" / "intermediate"
OUTPUT_FILENAME = "master_dataset.csv"


# =============================================================================
# 1. CARGA DE DATASETS
# =============================================================================

def load_processed_datasets(base_path: Path) -> dict:
    """Carga los cinco datasets procesados desde data/processed/.

    Verifica la existencia de cada archivo antes de cargarlo.
    Retorna un diccionario con los DataFrames.
    """
    files = {
        "pacientes": "01_pacientes.csv",
        "atenciones": "02_atenciones.csv",
        "historia_clinica": "03_historia_clinica_detalle.csv",
        "prefactura": "04_prefactura.csv",
        "cruce_validacion": "05_cruce_validacion.csv",
    }

    datasets = {}
    print("=== CARGA DE DATASETS ===\n")

    for name, filename in files.items():
        filepath = base_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

        datasets[name] = pd.read_csv(filepath)
        print(f"  ✅ {filename}: {datasets[name].shape[0]:,} registros, "
              f"{datasets[name].shape[1]} columnas")

    print(f"\n  Total datasets cargados: {len(datasets)}")
    return datasets


# =============================================================================
# 2. INTEGRACIÓN (JOINS)
# =============================================================================

def validate_join(df_before: pd.DataFrame, df_after: pd.DataFrame,
                  step_name: str, expected_rows: int = None):
    """Valida el resultado de un JOIN mostrando métricas clave."""
    rows_before = len(df_before)
    rows_after = len(df_after)
    lost = rows_before - rows_after
    dupes = df_after.duplicated().sum()

    print(f"\n  --- Validación: {step_name} ---")
    print(f"  Registros antes:  {rows_before:,}")
    print(f"  Registros después: {rows_after:,}")
    print(f"  Perdidos: {lost}")
    print(f"  Duplicados: {dupes}")

    if expected_rows is not None and rows_after != expected_rows:
        print(f"  ⚠️ ADVERTENCIA: Se esperaban {expected_rows:,} registros")

    if lost > 0:
        print(f"  ⚠️ Se perdieron {lost} registros en este paso")

    return rows_after


def step1_base_cruce(datasets: dict) -> pd.DataFrame:
    """Paso 1: Tomar cruce_validacion como dataset base (3,126 registros)."""
    df = datasets["cruce_validacion"].copy()
    print(f"\n{'=' * 60}")
    print("PASO 1: Base — cruce_validacion")
    print(f"{'=' * 60}")
    print(f"  Registros base: {len(df):,}")
    print(f"  Columnas: {list(df.columns)}")
    return df


def step2_join_atenciones(master: pd.DataFrame,
                          datasets: dict) -> pd.DataFrame:
    """Paso 2: INNER JOIN con atenciones usando id_atencion."""
    print(f"\n{'=' * 60}")
    print("PASO 2: INNER JOIN con atenciones (id_atencion)")
    print(f"{'=' * 60}")

    atenciones = datasets["atenciones"]
    result = master.merge(
        atenciones,
        on="id_atencion",
        how="inner",
        suffixes=("", "_at")
    )

    validate_join(master, result, "INNER JOIN atenciones", expected_rows=3126)
    return result


def step3_join_pacientes(master: pd.DataFrame,
                         datasets: dict) -> pd.DataFrame:
    """Paso 3: LEFT JOIN con pacientes usando id_paciente."""
    print(f"\n{'=' * 60}")
    print("PASO 3: LEFT JOIN con pacientes (id_paciente)")
    print(f"{'=' * 60}")

    pacientes = datasets["pacientes"]

    # id_paciente viene de atenciones tras el paso 2
    result = master.merge(
        pacientes,
        on="id_paciente",
        how="left",
        suffixes=("", "_pac")
    )

    validate_join(master, result, "LEFT JOIN pacientes", expected_rows=3126)

    unmatched = result["edad"].isna().sum()
    if unmatched > 0:
        print(f"  ⚠️ {unmatched} registros sin match en pacientes")
    else:
        print("  ✅ Todos los registros coinciden con pacientes")

    return result


def step4_join_historia_clinica(master: pd.DataFrame,
                                datasets: dict) -> pd.DataFrame:
    """Paso 4: LEFT JOIN con historia_clinica usando id_detalle_hc."""
    print(f"\n{'=' * 60}")
    print("PASO 4: LEFT JOIN con historia_clinica (id_detalle_hc = id_detalle)")
    print(f"{'=' * 60}")

    historia_clinica = datasets["historia_clinica"]

    result = master.merge(
        historia_clinica,
        left_on="id_detalle_hc",
        right_on="id_detalle",
        how="left",
        suffixes=("", "_hc")
    )

    validate_join(master, result, "LEFT JOIN historia_clinica",
                  expected_rows=3126)

    unmatched = result["id_detalle"].isna().sum()
    print(f"  Sin match en HC (esperado para alertas sin soporte): {unmatched}")

    return result


def step5_join_prefactura(master: pd.DataFrame,
                          datasets: dict) -> pd.DataFrame:
    """Paso 5: LEFT JOIN con prefactura usando id_prefactura."""
    print(f"\n{'=' * 60}")
    print("PASO 5: LEFT JOIN con prefactura (id_prefactura)")
    print(f"{'=' * 60}")

    prefactura = datasets["prefactura"]

    result = master.merge(
        prefactura,
        on="id_prefactura",
        how="left",
        suffixes=("", "_pf")
    )

    validate_join(master, result, "LEFT JOIN prefactura", expected_rows=3126)

    unmatched = result["codigo_cups_facturado"].isna().sum()
    print(f"  Sin match en PF (esperado para NO_FACTURADO): {unmatched}")

    return result


def build_master_dataset(datasets: dict) -> pd.DataFrame:
    """Ejecuta la integración completa en 5 pasos."""
    print("\n" + "=" * 60)
    print(" CONSTRUCCIÓN DEL MASTER DATASET")
    print("=" * 60)

    master = step1_base_cruce(datasets)
    master = step2_join_atenciones(master, datasets)
    master = step3_join_pacientes(master, datasets)
    master = step4_join_historia_clinica(master, datasets)
    master = step5_join_prefactura(master, datasets)

    return master


# =============================================================================
# 4. LIMPIEZA DE COLUMNAS REDUNDANTES
# =============================================================================

def remove_redundant_columns(master: pd.DataFrame) -> pd.DataFrame:
    """Elimina columnas redundantes del Master Dataset.

    Columnas eliminadas:
    - id_paciente_at / _pf: redundante (ya existe id_paciente)
    - eps_at / eps_pac / eps_pf: redundante (conservar eps de atenciones)
    - id_atencion_hc / _pf: redundante
    - id_detalle: duplicado de id_detalle_hc
    - Sufijos _at, _pac, _pf redundantes
    """
    print(f"\n{'=' * 60}")
    print("LIMPIEZA DE COLUMNAS REDUNDANTES")
    print(f"{'=' * 60}")

    cols_before = master.columns.tolist()

    # Identificar columnas con sufijos redundantes
    cols_to_drop = []
    for col in master.columns:
        # Columnas con sufijos de merge que son redundantes
        if col.endswith("_at") or col.endswith("_pac") or col.endswith("_pf"):
            cols_to_drop.append(col)

    # id_detalle es redundante con id_detalle_hc
    if "id_detalle" in master.columns:
        cols_to_drop.append("id_detalle")

    # Eliminar solo las que existen
    cols_to_drop = [c for c in cols_to_drop if c in master.columns]

    if cols_to_drop:
        master = master.drop(columns=cols_to_drop)
        print(f"  Columnas eliminadas ({len(cols_to_drop)}):")
        for col in sorted(cols_to_drop):
            print(f"    - {col}")
    else:
        print("  No se encontraron columnas redundantes.")

    print(f"\n  Columnas antes: {len(cols_before)}")
    print(f"  Columnas después: {len(master.columns)}")
    print(f"  Columnas finales: {list(master.columns)}")

    return master


# =============================================================================
# 5. VALIDACIÓN DEL MASTER DATASET
# =============================================================================

def validate_master_dataset(master: pd.DataFrame):
    """Realiza validación final del Master Dataset."""
    print(f"\n{'=' * 60}")
    print("VALIDACIÓN DEL MASTER DATASET")
    print(f"{'=' * 60}")

    print(f"\n  Shape: {master.shape}")
    print(f"  Registros: {master.shape[0]:,}")
    print(f"  Columnas: {master.shape[1]}")
    print(f"  Duplicados: {master.duplicated().sum()}")

    print(f"\n  --- Nulos por columna ---")
    nulls = master.isnull().sum()
    cols_with_nulls = nulls[nulls > 0]
    if len(cols_with_nulls) > 0:
        for col, count in cols_with_nulls.items():
            pct = count / len(master) * 100
            print(f"    {col}: {count} ({pct:.1f}%)")
    else:
        print("    Sin nulos")

    print(f"\n  --- Tipos de datos ---")
    print(master.dtypes.to_string())

    print(f"\n  --- Primeros registros ---")
    print(master.head(3).to_string())


# =============================================================================
# 6. EXPORTACIÓN
# =============================================================================

def export_master_dataset(master: pd.DataFrame, output_path: Path,
                          filename: str):
    """Exporta el Master Dataset a CSV."""
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename

    master.to_csv(filepath, index=False)

    print(f"\n{'=' * 60}")
    print("EXPORTACIÓN")
    print(f"{'=' * 60}")
    print(f"  ✅ Master Dataset guardado: {filepath}")
    print(f"  Registros: {len(master):,}")
    print(f"  Columnas: {master.shape[1]}")
    print(f"  Tamaño: {filepath.stat().st_size / 1024:.1f} KB")


# =============================================================================
# 7. RESUMEN EJECUTIVO
# =============================================================================

def print_summary(master: pd.DataFrame):
    """Muestra resumen ejecutivo de la integración."""
    print(f"\n{'=' * 60}")
    print(" RESUMEN EJECUTIVO")
    print(f"{'=' * 60}")

    print(f"""
  Número final de registros: {master.shape[0]:,}
  Número final de columnas:  {master.shape[1]}

  JOINs realizados:
    1. cruce_validacion (base)         → 3,126 registros
    2. INNER JOIN atenciones           → id_atencion
    3. LEFT JOIN pacientes             → id_paciente
    4. LEFT JOIN historia_clinica      → id_detalle_hc = id_detalle
    5. LEFT JOIN prefactura            → id_prefactura

  Registros perdidos: 0
  Duplicados: {master.duplicated().sum()}

  ✅ Master Dataset listo para Feature Engineering (DP-03).
""")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Ejecuta el pipeline completo de integración."""
    # 1. Cargar datasets
    datasets = load_processed_datasets(DATA_PROCESSED_PATH)

    # 2. Construir Master Dataset
    master = build_master_dataset(datasets)

    # 3. Eliminar columnas redundantes
    master = remove_redundant_columns(master)

    # 4. Validar
    validate_master_dataset(master)

    # 5. Exportar
    export_master_dataset(master, DATA_INTERMEDIATE_PATH, OUTPUT_FILENAME)

    # 6. Resumen
    print_summary(master)

    return master


if __name__ == "__main__":
    main()
