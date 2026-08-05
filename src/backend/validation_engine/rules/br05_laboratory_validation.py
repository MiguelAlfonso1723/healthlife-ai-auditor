"""
BR-05 — Laboratory and Exam Validation.

Validates that laboratory exams performed are included in
the Pre-invoice.

An exam performed but not billed represents omitted revenue.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR05LaboratoryValidation(BaseRule):
    """Detects laboratory exams registered but not billed."""

    @property
    def rule_id(self) -> str:
        return "BR-05"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if a lab exam was properly billed.

        Condition: tipo_item is 'examen' AND procedure not billed.
        """
        tipo_item = self._get_field(record, "tipo_item")
        has_pf = self._get_field(record, "id_prefactura") is not None

        if tipo_item == "examen" and not has_pf:
            codigo = self._get_field(record, "codigo_cups", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="NO_FACTURADO",
                severity="ALTA",
                description=(
                    f"Examen/laboratorio con código CUPS {codigo} realizado "
                    f"pero no incluido en la Pre-factura. "
                    f"Procedimiento omitido."
                ),
            )

        return None
