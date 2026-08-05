"""BR-03 - Diagnosis/procedure consistency validation."""

from typing import Dict, Optional

from ..models import ValidationAlert
from .base_rule import BaseRule


class BR03DiagnosisValidation(BaseRule):
    """Detects missing or incompatible diagnosis/procedure pairs."""

    DIAGNOSIS_ALLOWED_CUPS = {
        "A090": {"890415", "890301", "902210", "890201", "890201-M"},
        "C349": {"871111", "890415", "890301", "930601", "890201"},
        "E119": {"890415", "903841", "890301", "902210", "890201"},
        "F411": {"990601", "890201", "890301", "890415"},
        "H269": {"890201", "391013", "890301", "890415"},
        "I10X": {"890415", "890301", "902210", "890201", "890701"},
        "I219": {"890415", "890301", "902210", "890201", "890701", "391201"},
        "J189": {"871111", "890415", "890301", "902210", "890201", "930601"},
        "K358": {"890415", "890301", "890201", "881201", "391121"},
        "M545": {"890201", "890301", "890415"},
        "N390": {"903875", "890415", "890301", "890201", "881201"},
        "O800": {"739001", "890415", "881332", "890301", "890201"},
        "R073": {"871111", "890415", "890301", "890201", "890701"},
        "S824": {"930878", "890201", "890301", "890415"},
        "Z348": {"881332", "890201", "890301", "890415"},
    }

    @property
    def rule_id(self) -> str:
        return "BR-03"

    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate clinical coherence between diagnosis and procedure."""
        has_hc = self._get_field(record, "id_detalle_hc") is not None
        if not has_hc:
            return None

        diagnostico = self._get_field(record, "diagnostico_principal_cie10")
        codigo = self._get_field(record, "codigo_cups")

        if diagnostico is None:
            return self._alert(codigo or "N/A", "sin diagnostico principal disponible")

        allowed = self.DIAGNOSIS_ALLOWED_CUPS.get(str(diagnostico))
        if allowed is not None and codigo is not None and str(codigo) not in allowed:
            return self._alert(
                str(codigo),
                f"no esta en la matriz de compatibilidad del diagnostico {diagnostico}",
            )

        return None

    def _alert(self, codigo: str, reason: str) -> ValidationAlert:
        return ValidationAlert(
            rule=self.rule_id,
            alert_type="DIAGNOSTICO_NO_RELACIONADO",
            severity="MEDIA",
            description=(
                f"Procedimiento con codigo CUPS {codigo} {reason}. "
                f"Requiere validacion de pertinencia medica."
            ),
        )
