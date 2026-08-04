"""
BR-03 — Diagnosis Validation.

Validates coherence between the registered diagnosis (CIE-10)
and the procedures registered in the Clinical History.

According to BU-03, the fields involved are:
    - diagnostico_principal_cie10  (from atenciones)
    - descripcion_diagnostico      (from atenciones)
    - codigo_cups                  (from historia_clinica)

An inconsistency is flagged when a clinical record exists but
the associated diagnosis is unavailable, making it impossible
to verify whether the procedure is medically justified.

NOTE: Comparison between codigo_cups and codigo_cups_facturado
belongs to BR-01 (billing completeness), not BR-03.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR03DiagnosisValidation(BaseRule):
    """Detects missing or unavailable diagnosis for registered procedures."""

    @property
    def rule_id(self) -> str:
        return "BR-03"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate diagnosis availability for clinical records.

        Condition: A clinical record (id_detalle_hc) exists but the
        associated diagnosis (diagnostico_principal_cie10) is missing,
        making it impossible to confirm that the procedure is
        consistent with the patient's diagnosis.

        This differs from BR-01 (procedure not billed) and BR-02
        (no clinical support for a billed procedure).
        """
        has_hc = self._get_field(record, "id_detalle_hc") is not None
        diagnostico = self._get_field(record, "diagnostico_principal_cie10")

        # Only evaluate when there is a clinical record to validate
        if not has_hc:
            return None

        if diagnostico is None:
            codigo = self._get_field(record, "codigo_cups", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="DIAGNOSTICO_NO_RELACIONADO",
                severity="MEDIA",
                description=(
                    f"Procedimiento con código CUPS {codigo} registrado en "
                    f"Historia Clínica sin diagnóstico principal disponible. "
                    f"No es posible verificar la pertinencia médica del procedimiento."
                ),
            )

        return None
