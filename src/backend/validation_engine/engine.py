"""
Medical Validation Engine.

Orchestrates the execution of all business rules (BR-01 to BR-06)
against a single record from the Master Dataset.

This is the first validation layer of the Digital Medical Auditor.
It handles deterministic validations only — no ML/AI involved.
"""

from typing import Dict, List
from .models import ValidationAlert, ValidationResult
from .rules import (
    BR01ProcedureValidation,
    BR02ClinicalSupport,
    BR03DiagnosisValidation,
    BR04TreatmentValidation,
    BR05LaboratoryValidation,
    BR06QuantityValidation,
)
from .rules.base_rule import BaseRule


class MedicalValidationEngine:
    """Executes all medical business rules on a record.

    The engine processes each rule sequentially and collects
    all alerts generated. If no alerts are produced, the record
    is classified as CONSISTENTE.
    """

    def __init__(self):
        """Initialize the engine with all registered business rules."""
        self._rules: List[BaseRule] = [
            BR01ProcedureValidation(),
            BR02ClinicalSupport(),
            BR03DiagnosisValidation(),
            BR04TreatmentValidation(),
            BR05LaboratoryValidation(),
            BR06QuantityValidation(),
        ]

    @property
    def rules(self) -> List[BaseRule]:
        """Return the list of registered rules."""
        return self._rules

    def validate(self, record: Dict) -> ValidationResult:
        """Execute all business rules on a single record.

        Args:
            record: Dictionary with fields from the Master Dataset.

        Returns:
            ValidationResult with status and list of alerts.
        """
        id_cruce = record.get("id_cruce", "UNKNOWN")
        alerts: List[ValidationAlert] = []

        for rule in self._rules:
            alert = rule.evaluate(record)
            if alert is not None:
                alerts.append(alert)

        status = "INCONSISTENTE" if alerts else "CONSISTENTE"

        return ValidationResult(
            id_cruce=id_cruce,
            status=status,
            alerts=alerts,
        )

    def validate_batch(self, records: List[Dict]) -> List[ValidationResult]:
        """Execute validation on a batch of records.

        Args:
            records: List of dictionaries from the Master Dataset.

        Returns:
            List of ValidationResult objects.
        """
        return [self.validate(record) for record in records]
