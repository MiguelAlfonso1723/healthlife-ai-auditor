"""
BR-02 — Clinical Support Validation.

Validates that every billed procedure has clinical evidence
supporting its execution in the Clinical History.

A billed procedure without clinical support may result in
claim denials (glosas) from the payer.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR02ClinicalSupport(BaseRule):
    """Detects billed procedures without clinical support."""

    @property
    def rule_id(self) -> str:
        return "BR-02"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if a billed procedure has clinical support.

        Condition: id_prefactura exists but soporte_clinico is not 'SI'.
        """
        has_pf = self._get_field(record, "id_prefactura") is not None
        soporte = self._get_field(record, "soporte_clinico")

        if has_pf and soporte != "SI":
            codigo = self._get_field(record, "codigo_cups_facturado", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="SIN_SOPORTE_CLINICO",
                severity="ALTA",
                description=(
                    f"Procedimiento facturado con código CUPS {codigo} no "
                    f"cuenta con soporte clínico documentado. "
                    f"Riesgo de glosa por falta de evidencia."
                ),
            )

        return None
