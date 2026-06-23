from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from .backends.base import BackendAdapter, BackendConfig
from .edges.operations import EdgeOperations
from .edges.registry import EdgeTypeDefinition, EdgeTypeRegistry
from .health import HealthChecker
from .locks.manager import LockManager
from .models import HealthStatus
from .nodes.operations import NodeOperations
from .nodes.registry import NodeTypeDefinition, NodeTypeRegistry
from .nodes.transitions import TransitionValidator
from .queries import QueryEngine
from .schema.base import (
    build_base_edge_type_definitions,
    build_base_node_type_definitions,
)
from .schema.manager import SchemaManager
from .transaction import BlackboardTransaction

if TYPE_CHECKING:
    from .backends.arcadedb.config import ArcadeDBConfig
    from .backends.ladybug.config import LadybugConfig


@dataclass(slots=True)
class BlackboardConfig:
    backend: Literal["arcadedb", "ladybug", "memory"]
    connection: ArcadeDBConfig | LadybugConfig | BackendConfig
    schema_node_extensions: list[NodeTypeDefinition] = field(default_factory=list)
    schema_edge_extensions: list[EdgeTypeDefinition] = field(default_factory=list)
    lock_ttl_seconds: int = 60
    lock_reclaim_interval_seconds: int = 30
    query_timeout_seconds: float = 30.0


class Blackboard:
    def __init__(self, config: BlackboardConfig) -> None:
        self.config = config
        self.adapter = self._build_adapter()

        node_registry = NodeTypeRegistry()
        edge_registry = EdgeTypeRegistry()
        for definition in build_base_node_type_definitions():
            node_registry.register(definition)
        for definition in config.schema_node_extensions:
            node_registry.register(definition)

        for definition in build_base_edge_type_definitions():
            edge_registry.register(definition)
        for definition in config.schema_edge_extensions:
            edge_registry.register(definition)

        transition_validator = TransitionValidator(node_registry)
        self.nodes = NodeOperations(self.adapter, node_registry, transition_validator)
        self.edges = EdgeOperations(self.adapter, edge_registry)
        self.locks = LockManager(self.adapter)
        self.queries = QueryEngine(self.adapter)
        self.schema = SchemaManager(self.adapter)
        self._health_checker = HealthChecker(self.adapter, self.schema)

    def _build_adapter(self) -> BackendAdapter:
        config = self.config
        if config.backend == "arcadedb":
            from .backends.arcadedb.adapter import ArcadeDBAdapter
            from .backends.arcadedb.config import ArcadeDBConfig

            if not isinstance(config.connection, ArcadeDBConfig):
                msg = "ArcadeDB backend requires ArcadeDBConfig"
                raise TypeError(msg)
            return ArcadeDBAdapter(config.connection, config.connection.database_path)

        if config.backend == "ladybug":
            from .backends.ladybug.adapter import LadybugAdapter
            from .backends.ladybug.config import LadybugConfig

            if not isinstance(config.connection, LadybugConfig):
                msg = "Ladybug backend requires LadybugConfig"
                raise TypeError(msg)
            return LadybugAdapter(config.connection)

        if config.backend == "memory":
            from .backends.memory.adapter import MemoryAdapter

            return MemoryAdapter()

        msg = f"Unsupported backend type: {config.backend}"
        raise ValueError(msg)

    def transaction(self) -> BlackboardTransaction:
        """Create a transaction context manager bound to this blackboard backend."""
        return BlackboardTransaction(self.adapter)

    def health(self) -> HealthStatus:
        """Return health details for backend connectivity and schema validity."""
        return self._health_checker.check()

    def close(self) -> None:
        """Close blackboard resources and backend connections."""
        self.adapter.close()
