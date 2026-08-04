"""
BR-06 — Quantity Validation.

Validates that the quantity performed (registered in HC) matches
the quantity billed (in Pre-invoice).

A discrepancy in quantities may indicate overbilling or underbilling.
"""

from typing import Dict, Optional
from ..models import ValidationAlert
from .base_rule import BaseRule


class BR06QuantityValidation(BaseRule):
    """Detects discrepancies between performed and billed quantities."""

    @property
    def rule_id(self) -> str:
        return "BR-06"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if quantities match between HC and PF.

        Condition: Both quantities exist and they differ.
        """
        cant_realizada = self._get_field(record, "cantidad_realizada")
        cant_facturada = self._get_field(record, "cantidad_facturada")

        if cant_realizada is None or cant_facturada is None:
            return None

        try:
            realizada = int(float(cant_realizada))
            facturada = int(float(cant_facturada))
        except (ValueError, TypeError):
            return None

        if realizada != facturada:
            diferencia = realizada - facturada
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="CANTIDAD_DISCORDANTE",
                severity="MEDIA",
                description=(
                    f"Cantidad realizada ({realizada}) difiere de la "
                    f"cantidad facturada ({facturada}). "
                    f"Diferencia: {diferencia}."
                ),
            )

        return None
