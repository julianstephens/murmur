from __future__ import annotations

from dataclasses import dataclass

from ..errors import InvalidQueryError
from .transitions import TransitionGraph


@dataclass(slots=True)
class NodeTypeDefinition:
    name: str
    required_properties: dict[str, type]
    optional_properties: dict[str, type]
    system_properties: set[str]
    transition_graph: TransitionGraph | None


class NodeTypeRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, NodeTypeDefinition] = {}

    def register(self, definition: NodeTypeDefinition) -> None:
        self._definitions[definition.name] = definition

    def get(self, name: str) -> NodeTypeDefinition:
        self.validate_type(name)
        return self._definitions[name]

    def validate_type(self, name: str) -> None:
        if name not in self._definitions:
            msg = f"Unknown node type: {name}"
            raise InvalidQueryError(msg)

    def all_types(self) -> list[NodeTypeDefinition]:
        return list(self._definitions.values())
