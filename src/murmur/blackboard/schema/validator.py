from __future__ import annotations

from ..edges.registry import EdgeTypeDefinition
from ..errors import SchemaConflictError
from ..nodes.registry import NodeTypeDefinition


class SchemaValidator:
    def validate(
        self,
        extensions_nodes: list[NodeTypeDefinition],
        extension_edges: list[EdgeTypeDefinition],
        existing_types: set[str],
    ) -> None:
        seen: set[str] = set(existing_types)
        for definition in extensions_nodes:
            if definition.name in seen:
                msg = f"Node type already exists: {definition.name}"
                raise SchemaConflictError(msg)
            seen.add(definition.name)

        seen_edges = set(existing_types)
        for definition in extension_edges:
            if definition.name in seen_edges:
                msg = f"Edge type already exists: {definition.name}"
                raise SchemaConflictError(msg)
            seen_edges.add(definition.name)
