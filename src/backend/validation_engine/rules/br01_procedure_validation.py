"""
BR-01 — Procedure Billing Validation.

Validates that procedures registered in the Clinical History
have been included in the Pre-invoice.

A procedure registered but NOT billed represents a potential
revenue leakage for the organization.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR01ProcedureValidation(BaseRule):
    """Detects procedures registered in HC but not billed in PF."""

    @property
    def rule_id(self) -> str:
        return "BR-01"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if a registered procedure was billed.

        Condition: id_detalle_hc exists but id_prefactura is missing.
        This means the clinical record exists but no billing was generated.
        """
        has_hc = self._get_field(record, "id_detalle_hc") is not None
        has_pf = self._get_field(record, "id_prefactura") is not None

        if has_hc and not has_pf:
            codigo = self._get_field(record, "codigo_cups", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="NO_FACTURADO",
                severity="ALTA",
                description=(
                    f"Procedimiento con código CUPS {codigo} registrado en "
                    f"Historia Clínica pero no incluido en la Pre-factura. "
                    f"Posible fuga de ingresos."
                ),
            )

        return None
