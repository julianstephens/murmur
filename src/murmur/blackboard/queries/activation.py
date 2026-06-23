from __future__ import annotations

from dataclasses import dataclass, field

from ..backends.base import BackendAdapter
from ..models import Node
from .filters import PropertyFilter


@dataclass(slots=True)
class ActivationQueryDefinition:
    node_type: str
    required_status: set[str] = field(default_factory=set)
    excluded_status: set[str] = field(default_factory=set)
    property_conditions: list[PropertyFilter] = field(default_factory=list)
    order_by: str | None = None
    limit: int = 100


class ActivationRunner:
    def __init__(self, adapter: BackendAdapter) -> None:
        self._adapter = adapter

    def run(self, definition: ActivationQueryDefinition) -> list[Node]:
        """Execute an activation query and return matching nodes."""
        raise NotImplementedError
