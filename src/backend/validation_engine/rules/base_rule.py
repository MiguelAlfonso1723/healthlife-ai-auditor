"""Base class for all business rules."""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from ..models import ValidationAlert


class BaseRule(ABC):
    """Abstract base class for medical validation rules."""

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Identifier of the rule (e.g., BR-01)."""
        ...

    @abstractmethod
    def evaluate(self, record: Dict) -> Optional[ValidationAlert]:
        """Evaluate a record and return an alert if inconsistency found.

        Args:
            record: Dictionary containing the Master Dataset fields.

        Returns:
            ValidationAlert if inconsistency detected, None otherwise.
        """
        ...

    def _get_field(self, record: Dict, field: str, default=None):
        """Safely retrieve a field value from record."""
        value = record.get(field, default)
        if value is None or (isinstance(value, float) and str(value) == "nan"):
            return default
        return value
