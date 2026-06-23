from __future__ import annotations

from ..backends.base import BackendAdapter
from .activation import ActivationQueryDefinition, ActivationRunner
from .filters import FilterOperator, FilterRunner, PropertyFilter
from .traversal import TraversalRunner


class QueryEngine:
    def __init__(self, adapter: BackendAdapter) -> None:
        self.activation = ActivationRunner(adapter)
        self.traversal = TraversalRunner(adapter)
        self.filters = FilterRunner(adapter)


__all__ = [
    "ActivationQueryDefinition",
    "FilterOperator",
    "PropertyFilter",
    "QueryEngine",
]
