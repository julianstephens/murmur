from __future__ import annotations

from ..backends.base import BackendAdapter


class SchemaManager:
    def __init__(self, adapter: BackendAdapter) -> None:
        self._adapter = adapter

    def initialize(
        self, application_node_extensions, application_edge_extensions
    ) -> None:
        """Initialize backend schema and register application-specific extensions."""
        raise NotImplementedError

    def version(self) -> str:
        """Return the active blackboard schema version reported by the backend."""
        raise NotImplementedError

    def validate_runtime(self) -> bool:
        """Validate backend schema compatibility for runtime operations."""
        raise NotImplementedError
