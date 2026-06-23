from __future__ import annotations

from ..backends.base import BackendAdapter
from ..models import Edge, NodeId, PropertyValue
from .registry import EdgeTypeRegistry


class EdgeOperations:
    def __init__(self, adapter: BackendAdapter, registry: EdgeTypeRegistry) -> None:
        self._adapter = adapter
        self._registry = registry

    def create(
        self,
        edge_type: str,
        from_node_id: NodeId,
        to_node_id: NodeId,
        properties: dict[str, PropertyValue],
    ) -> Edge:
        """Create an edge after validating edge type and endpoint constraints."""
        raise NotImplementedError

    def get(self, from_node_id: NodeId, edge_type: str) -> list[Edge]:
        """Fetch edges of a given type originating from the specified node."""
        raise NotImplementedError

    def delete(self, edge_type: str, from_node_id: NodeId, to_node_id: NodeId) -> None:
        """Delete the specified edge if it exists in the backend."""
        raise NotImplementedError
