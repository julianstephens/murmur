from __future__ import annotations

from dataclasses import dataclass

from ..errors import InvalidQueryError


@dataclass(slots=True)
class EdgeTypeDefinition:
    name: str
    allowed_from_types: set[str]
    allowed_to_types: set[str]
    required_properties: dict[str, type]
    optional_properties: dict[str, type]


class EdgeTypeRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, EdgeTypeDefinition] = {}

    def register(self, definition: EdgeTypeDefinition) -> None:
        self._definitions[definition.name] = definition

    def get(self, name: str) -> EdgeTypeDefinition:
        self.validate_type(name)
        return self._definitions[name]

    def validate_type(self, name: str) -> None:
        if name not in self._definitions:
            msg = f"Unknown edge type: {name}"
            raise InvalidQueryError(msg)

    def validate_endpoints(
        self,
        edge_type: str,
        from_node_type: str,
        to_node_type: str,
    ) -> None:
        definition = self.get(edge_type)
        if from_node_type not in definition.allowed_from_types:
            msg = f"Edge {edge_type} cannot originate from node type {from_node_type}"
            raise InvalidQueryError(msg)
        if to_node_type not in definition.allowed_to_types:
            msg = f"Edge {edge_type} cannot target node type {to_node_type}"
            raise InvalidQueryError(msg)
