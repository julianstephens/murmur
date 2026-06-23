from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..backends.base import BackendAdapter
from ..models import Node, PropertyValue


class FilterOperator(StrEnum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    IN = "IN"
    NOT_IN = "NOT_IN"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    IS_NULL = "IS_NULL"
    IS_NOT_NULL = "IS_NOT_NULL"


@dataclass(slots=True)
class PropertyFilter:
    property: str
    operator: FilterOperator
    value: PropertyValue | list[PropertyValue] | None


class FilterRunner:
    def __init__(self, adapter: BackendAdapter) -> None:
        self._adapter = adapter

    def filter_nodes(
        self,
        node_type: str,
        conditions: list[PropertyFilter],
        limit: int = 100,
    ) -> list[Node]:
        """Filter nodes by property conditions and return matching typed nodes."""
        raise NotImplementedError
