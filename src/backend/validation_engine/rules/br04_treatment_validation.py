"""
BR-04 — Treatment Validation.

Validates that treatments registered in the Clinical History
are considered during the billing process.

A treatment performed but not billed represents a potential
economic loss.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR04TreatmentValidation(BaseRule):
    """Detects treatments registered but not billed."""

    @property
    def rule_id(self) -> str:
        return "BR-04"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if a treatment was properly billed.

        Condition: tipo_item is 'tratamiento' AND procedure not billed.
        """
        tipo_item = self._get_field(record, "tipo_item")
        has_pf = self._get_field(record, "id_prefactura") is not None

        if tipo_item == "tratamiento" and not has_pf:
            codigo = self._get_field(record, "codigo_cups", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="NO_FACTURADO",
                severity="MEDIA",
                description=(
                    f"Tratamiento con código CUPS {codigo} registrado en "
                    f"Historia Clínica pero no facturado. "
                    f"Posible pérdida económica."
                ),
            )

        return None
