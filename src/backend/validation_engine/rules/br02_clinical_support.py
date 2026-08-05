"""BR-02 - Clinical support validation."""

from typing import Dict, Optional

from ..models import ValidationAlert
from .base_rule import BaseRule


class BR02ClinicalSupport(BaseRule):
    """Detects billed services without clinical support."""

    @property
    def rule_id(self) -> str:
        return "BR-02"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate if a billed procedure has clinical support."""
        has_pf = self._get_field(record, "id_prefactura") is not None
        has_hc = self._get_field(record, "id_detalle_hc") is not None
        soporte = self._get_field(record, "soporte_clinico")

        if has_pf and (not has_hc or soporte != "SI"):
            codigo = self._get_field(record, "codigo_cups_facturado", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="SIN_SOPORTE_CLINICO",
                severity="ALTA",
                description=(
                    f"Procedimiento facturado con codigo CUPS {codigo} no "
                    f"cuenta con soporte clinico documentado. "
                    f"Riesgo de glosa por falta de evidencia."
                ),
            )

        return None
