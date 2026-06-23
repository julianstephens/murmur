from __future__ import annotations

from ..backends.base import BackendAdapter
from ..models import NodeId, Subgraph


class TraversalRunner:
    def __init__(self, adapter: BackendAdapter, max_depth: int = 5) -> None:
        self._adapter = adapter
        self._max_depth = max_depth

    def traverse(self, node_id: NodeId, depth: int, edge_types: list[str]) -> Subgraph:
        """Traverse outward from a node and return a bounded subgraph result."""
        raise NotImplementedError
