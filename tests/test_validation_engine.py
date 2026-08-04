"""
Unit tests for the Medical Validation Engine (M-01).

Tests all business rules BR-01 to BR-06 including:
- Individual rule tests
- Consistent record (no alerts)
- Multiple alerts on single record
- Incomplete data handling
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.validation_engine import MedicalValidationEngine, ValidationAlert, ValidationResult


# =============================================================================
# FIXTURES
# =============================================================================

def make_consistent_record():
    """Create a fully consistent record (no alerts expected)."""
    return {
        "id_cruce": "CRZ-TEST001",
        "id_atencion": "ATN-000001",
        "id_prefactura": "PF-0000001",
        "id_detalle_hc": "DET-0000001",
        "id_paciente": "PAC-00001",
        "resultado": "CONSISTENTE",
        "tipo_alerta": "CONSISTENTE",
        "severidad": "NINGUNA",
        "codigo_cups": "890201",
        "codigo_cups_facturado": "890201",
        "soporte_clinico": "SI",
        "tipo_item": "consulta",
        "cantidad_realizada": 1,
        "cantidad_facturada": 1,
        "diagnostico_principal_cie10": "I219",
    }


def make_no_facturado_record():
    """Record with procedure registered but not billed (BR-01)."""
    return {
        "id_cruce": "CRZ-TEST002",
        "id_atencion": "ATN-000002",
        "id_prefactura": None,
        "id_detalle_hc": "DET-0000002",
        "codigo_cups": "391201",
        "codigo_cups_facturado": None,
        "soporte_clinico": "SI",
        "tipo_item": "tratamiento",
        "cantidad_realizada": 1,
        "cantidad_facturada": None,
        "diagnostico_principal_cie10": "J449",
    }


def make_sin_soporte_record():
    """Record with billed procedure but no clinical support (BR-02)."""
    return {
        "id_cruce": "CRZ-TEST003",
        "id_atencion": "ATN-000003",
        "id_prefactura": "PF-0000003",
        "id_detalle_hc": "DET-0000003",
        "codigo_cups": "890201",
        "codigo_cups_facturado": "890201",
        "soporte_clinico": "NO",
        "tipo_item": "consulta",
        "cantidad_realizada": 1,
        "cantidad_facturada": 1,
        "diagnostico_principal_cie10": "J449",
    }


def make_diagnostico_no_relacionado_record():
    """Record with HC entry but no diagnosis available (BR-03).

    A clinical procedure is registered but the attending diagnosis
    is missing, so coherence between procedure and diagnosis
    cannot be verified.
    """
    return {
        "id_cruce": "CRZ-TEST004",
        "id_atencion": "ATN-000004",
        "id_prefactura": "PF-0000004",
        "id_detalle_hc": "DET-0000004",
        "codigo_cups": "890201",
        "codigo_cups_facturado": "890201",
        "soporte_clinico": "SI",
        "tipo_item": "consulta",
        "cantidad_realizada": 1,
        "cantidad_facturada": 1,
        "diagnostico_principal_cie10": None,   # Diagnosis missing → BR-03 fires
    }


def make_treatment_not_billed_record():
    """Treatment registered but not billed (BR-04)."""
    return {
        "id_cruce": "CRZ-TEST005",
        "id_atencion": "ATN-000005",
        "id_prefactura": None,
        "id_detalle_hc": "DET-0000005",
        "codigo_cups": "391201",
        "codigo_cups_facturado": None,
        "soporte_clinico": "SI",
        "tipo_item": "tratamiento",
        "cantidad_realizada": 1,
        "cantidad_facturada": None,
        "diagnostico_principal_cie10": "I219",
    }


def make_lab_not_billed_record():
    """Lab exam registered but not billed (BR-05)."""
    return {
        "id_cruce": "CRZ-TEST006",
        "id_atencion": "ATN-000006",
        "id_prefactura": None,
        "id_detalle_hc": "DET-0000006",
        "codigo_cups": "890701",
        "codigo_cups_facturado": None,
        "soporte_clinico": "SI",
        "tipo_item": "examen",
        "cantidad_realizada": 1,
        "cantidad_facturada": None,
        "diagnostico_principal_cie10": "E119",
    }


def make_quantity_mismatch_record():
    """Record with quantity discrepancy (BR-06)."""
    return {
        "id_cruce": "CRZ-TEST007",
        "id_atencion": "ATN-000007",
        "id_prefactura": "PF-0000007",
        "id_detalle_hc": "DET-0000007",
        "codigo_cups": "890201",
        "codigo_cups_facturado": "890201",
        "soporte_clinico": "SI",
        "tipo_item": "consulta",
        "cantidad_realizada": 2,
        "cantidad_facturada": 1,
        "diagnostico_principal_cie10": "J449",
    }


def make_multiple_alerts_record():
    """Record triggering multiple rules simultaneously.

    - BR-02: billed but no clinical support
    - BR-06: quantity discrepancy
    - BR-03: no diagnosis available for the HC entry
    """
    return {
        "id_cruce": "CRZ-TEST008",
        "id_atencion": "ATN-000008",
        "id_prefactura": "PF-0000008",
        "id_detalle_hc": "DET-0000008",
        "codigo_cups": "890201",
        "codigo_cups_facturado": "890201",
        "soporte_clinico": "NO",           # BR-02
        "tipo_item": "consulta",
        "cantidad_realizada": 2,
        "cantidad_facturada": 1,           # BR-06
        "diagnostico_principal_cie10": None,  # BR-03
    }


def make_incomplete_record():
    """Record with minimal data (many fields missing)."""
    return {
        "id_cruce": "CRZ-TEST009",
        "id_atencion": "ATN-000009",
        "id_prefactura": None,
        "id_detalle_hc": None,
        "codigo_cups": None,
        "codigo_cups_facturado": None,
        "soporte_clinico": None,
        "tipo_item": None,
        "cantidad_realizada": None,
        "cantidad_facturada": None,
        "diagnostico_principal_cie10": None,
    }


# =============================================================================
# TESTS
# =============================================================================

class TestMedicalValidationEngine:
    """Test suite for the Medical Validation Engine."""

    def setup_method(self):
        """Initialize engine before each test."""
        self.engine = MedicalValidationEngine()

    def test_engine_has_six_rules(self):
        """Engine should have exactly 6 registered rules."""
        assert len(self.engine.rules) == 6

    def test_consistent_record(self):
        """A fully consistent record should produce no alerts."""
        record = make_consistent_record()
        result = self.engine.validate(record)

        assert result.status == "CONSISTENTE"
        assert len(result.alerts) == 0
        assert result.id_cruce == "CRZ-TEST001"

    def test_br01_procedure_not_billed(self):
        """BR-01: Procedure registered without billing should alert."""
        record = make_no_facturado_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br01_alerts = [a for a in result.alerts if a.rule == "BR-01"]
        assert len(br01_alerts) >= 1
        assert br01_alerts[0].alert_type == "NO_FACTURADO"
        assert br01_alerts[0].severity == "ALTA"

    def test_br02_no_clinical_support(self):
        """BR-02: Billed procedure without clinical support should alert."""
        record = make_sin_soporte_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br02_alerts = [a for a in result.alerts if a.rule == "BR-02"]
        assert len(br02_alerts) == 1
        assert br02_alerts[0].alert_type == "SIN_SOPORTE_CLINICO"
        assert br02_alerts[0].severity == "ALTA"

    def test_br03_missing_diagnosis(self):
        """BR-03: HC record without diagnosis should alert (DIAGNOSTICO_NO_RELACIONADO)."""
        record = make_diagnostico_no_relacionado_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br03_alerts = [a for a in result.alerts if a.rule == "BR-03"]
        assert len(br03_alerts) == 1
        assert br03_alerts[0].alert_type == "DIAGNOSTICO_NO_RELACIONADO"
        assert br03_alerts[0].severity == "MEDIA"

    def test_br03_does_not_fire_without_hc(self):
        """BR-03: Records without HC entry should not trigger diagnosis alert."""
        record = {
            "id_cruce": "CRZ-TEST004B",
            "id_atencion": "ATN-000004",
            "id_prefactura": None,
            "id_detalle_hc": None,           # No HC record
            "codigo_cups": None,
            "codigo_cups_facturado": None,
            "soporte_clinico": None,
            "tipo_item": None,
            "cantidad_realizada": None,
            "cantidad_facturada": None,
            "diagnostico_principal_cie10": None,
        }
        result = self.engine.validate(record)
        br03_alerts = [a for a in result.alerts if a.rule == "BR-03"]
        assert len(br03_alerts) == 0

    def test_br04_treatment_not_billed(self):
        """BR-04: Treatment registered but not billed should alert."""
        record = make_treatment_not_billed_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br04_alerts = [a for a in result.alerts if a.rule == "BR-04"]
        assert len(br04_alerts) == 1
        assert br04_alerts[0].alert_type == "NO_FACTURADO"
        assert br04_alerts[0].severity == "MEDIA"

    def test_br05_lab_not_billed(self):
        """BR-05: Lab exam not billed should alert."""
        record = make_lab_not_billed_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br05_alerts = [a for a in result.alerts if a.rule == "BR-05"]
        assert len(br05_alerts) == 1
        assert br05_alerts[0].alert_type == "NO_FACTURADO"
        assert br05_alerts[0].severity == "ALTA"

    def test_br06_quantity_mismatch(self):
        """BR-06: Quantity discrepancy should alert."""
        record = make_quantity_mismatch_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        br06_alerts = [a for a in result.alerts if a.rule == "BR-06"]
        assert len(br06_alerts) == 1
        assert br06_alerts[0].alert_type == "CANTIDAD_DISCORDANTE"
        assert br06_alerts[0].severity == "MEDIA"

    def test_multiple_alerts(self):
        """Record with multiple issues should produce multiple alerts."""
        record = make_multiple_alerts_record()
        result = self.engine.validate(record)

        assert result.status == "INCONSISTENTE"
        assert len(result.alerts) >= 2

        rules_triggered = {a.rule for a in result.alerts}
        assert "BR-02" in rules_triggered  # No soporte
        assert "BR-03" in rules_triggered  # Diagnóstico no disponible
        assert "BR-06" in rules_triggered  # Cantidad discordante

    def test_incomplete_data(self):
        """Incomplete records should not crash the engine."""
        record = make_incomplete_record()
        result = self.engine.validate(record)

        # Should not raise any exception
        assert result.id_cruce == "CRZ-TEST009"
        assert result.status in ("CONSISTENTE", "INCONSISTENTE")

    def test_result_to_dict(self):
        """ValidationResult.to_dict() should produce correct structure."""
        record = make_sin_soporte_record()
        result = self.engine.validate(record)
        result_dict = result.to_dict()

        assert "id_cruce" in result_dict
        assert "status" in result_dict
        assert "alerts" in result_dict
        assert isinstance(result_dict["alerts"], list)
        if result_dict["alerts"]:
            alert = result_dict["alerts"][0]
            assert "rule" in alert
            assert "type" in alert
            assert "severity" in alert
            assert "description" in alert

    def test_batch_validation(self):
        """Batch validation should process multiple records."""
        records = [
            make_consistent_record(),
            make_no_facturado_record(),
            make_sin_soporte_record(),
        ]
        results = self.engine.validate_batch(records)

        assert len(results) == 3
        assert results[0].status == "CONSISTENTE"
        assert results[1].status == "INCONSISTENTE"
        assert results[2].status == "INCONSISTENTE"
