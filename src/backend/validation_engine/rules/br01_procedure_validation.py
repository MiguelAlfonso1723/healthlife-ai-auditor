"""BR-01 - Procedure billing and CUPS code validation."""

from typing import Dict, Optional

from ..models import ValidationAlert
from .base_rule import BaseRule


class BR01ProcedureValidation(BaseRule):
    """Detects missing billing records and mismatched billed CUPS codes."""

    @property
    def rule_id(self) -> str:
        return "BR-01"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate whether a clinical procedure was billed correctly."""
        has_hc = self._get_field(record, "id_detalle_hc") is not None
        has_pf = self._get_field(record, "id_prefactura") is not None

        if has_hc and not has_pf:
            codigo = self._get_field(record, "codigo_cups", "N/A")
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="NO_FACTURADO",
                severity="ALTA",
                description=(
                    f"Procedimiento con codigo CUPS {codigo} registrado en "
                    f"Historia Clinica pero no incluido en la Pre-factura. "
                    f"Posible fuga de ingresos."
                ),
            )

        codigo_hc = self._get_field(record, "codigo_cups")
        codigo_pf = self._get_field(record, "codigo_cups_facturado")
        if has_hc and has_pf and codigo_hc and codigo_pf and codigo_hc != codigo_pf:
            return ValidationAlert(
                rule=self.rule_id,
                alert_type="CODIGO_NO_COINCIDE",
                severity="ALTA",
                description=(
                    f"Codigo CUPS registrado en Historia Clinica ({codigo_hc}) "
                    f"no coincide con el codigo facturado ({codigo_pf}). "
                    f"Requiere revision de codificacion antes de facturar."
                ),
            )

        return None
