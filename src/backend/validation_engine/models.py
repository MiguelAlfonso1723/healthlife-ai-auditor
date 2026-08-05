"""
Data models for the Medical Validation Engine.

Defines the structure of alerts and validation results
produced by the business rules engine.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationAlert:
    """Represents a single inconsistency detected by a business rule."""

    rule: str
    alert_type: str
    severity: str
    description: str


@dataclass
class ValidationResult:
    """Represents the complete validation result for a single record."""

    id_cruce: str
    status: str
    alerts: List[ValidationAlert] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id_cruce": self.id_cruce,
            "status": self.status,
            "alerts": [
                {
                    "rule": a.rule,
                    "type": a.alert_type,
                    "severity": a.severity,
                    "description": a.description,
                }
                for a in self.alerts
            ],
        }
