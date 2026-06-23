from __future__ import annotations

from ..backends.base import BackendAdapter
from ..models import Node, NodeId, PropertyValue
from .registry import NodeTypeRegistry
from .transitions import TransitionValidator


class NodeOperations:
    def __init__(
        self,
        adapter: BackendAdapter,
        registry: NodeTypeRegistry,
        transition_validator: TransitionValidator,
    ) -> None:
        self._adapter = adapter
        self._registry = registry
        self._transition_validator = transition_validator

    def create(
        self,
        node_type: str,
        properties: dict[str, PropertyValue],
        status: str | None = None,
    ) -> Node:
        """Create a node after validating node type and property contract."""
        raise NotImplementedError

    def get(self, node_id: NodeId) -> Node:
        """Fetch a node by identifier and return it as a typed model."""
        raise NotImplementedError

    def update(self, node_id: NodeId, properties: dict[str, PropertyValue]) -> Node:
        """Update mutable node properties and return the updated node."""
        raise NotImplementedError

    def delete(self, node_id: NodeId) -> None:
        """Delete a node and any backend-specific relationships."""
        raise NotImplementedError

    def transition_status(
        self, node_id: NodeId, from_status: str, to_status: str
    ) -> Node:
        """Validate and apply a node status transition atomically."""
        raise NotImplementedError
