"""Shared modeling configuration."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "master" / "master_dataset_features.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "docs" / "reports"
DIAGRAMS_DIR = PROJECT_ROOT / "docs" / "diagrams"

RANDOM_STATE = 42
TEST_SIZE = 0.20
VALIDATION_SIZE = 0.20

TARGET_COL = "tipo_alerta"
CONSISTENT_CLASS = "CONSISTENTE"

TEXT_COLS = [
    "descripcion_diagnostico",
    "descripcion",
    "descripcion_servicio_facturado",
]

ID_COLS = [
    "id_cruce",
    "id_atencion",
    "id_prefactura",
    "id_detalle_hc",
    "id_paciente",
    "id_atencion_hc",
]

TARGET_OR_LEAKAGE_COLS = [
    "resultado",
    "tipo_alerta",
    "severidad",
    "descripcion_alerta",
]

CATEGORICAL_COLS = [
    "tipo_atencion",
    "tipo_item",
    "tipo_afiliacion",
    "eps",
    "ciudad",
    "sede",
    "sexo",
    "tipo_documento",
    "diagnostico_principal_cie10",
    "codigo_cups",
    "codigo_cups_facturado",
    "soporte_clinico",
]

NUMERIC_COLS = [
    "edad",
    "cantidad_realizada",
    "cantidad_facturada",
    "valor_unitario",
    "valor_total",
    "cups_match",
    "tiene_soporte_clinico",
    "procedimiento_facturado",
    "procedimiento_registrado",
    "diagnostico_disponible",
    "len_descripcion_diagnostico",
    "len_descripcion_hc",
    "len_descripcion_servicio",
    "diferencia_cantidad",
    "cantidad_coincide",
    "valor_unitario_disponible",
    "valor_total_disponible",
    "servicio_facturado",
    "procedimiento_no_facturado",
    "anio_atencion",
    "mes_atencion",
    "trimestre",
    "dia_semana",
    "hora_registro",
    "dias_atencion_facturacion",
]

DATE_COLS = ["fecha_atencion", "fecha_registro", "fecha_facturacion"]

