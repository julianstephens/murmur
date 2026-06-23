from __future__ import annotations

from typing import Any

from ..base import BackendAdapter
from .config import ArcadeDBConfig
from .connection import ConnectionPool
from .conversion import TypeConverter
from .cypher import CypherBuilder


class ArcadeDBAdapter(BackendAdapter):
    def __init__(self, config: ArcadeDBConfig, database_path: str) -> None:
        self.config = config
        self.database_path = database_path
        self.pool = ConnectionPool(config)
        self.converter = TypeConverter()
        self.cypher_builder = CypherBuilder()

    def execute_write(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> None:
        """Execute one write statement using an acquired ArcadeDB connection context."""
        raise NotImplementedError

    def execute_read(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> list[dict]:
        """Execute a read statement and return converted row dictionaries."""
        raise NotImplementedError

    def execute_transaction(
        self,
        operations: list[tuple[str, dict]],
        connection_context: Any | None,
    ) -> None:
        """Execute a sequence of operations in one ArcadeDB transaction context."""
        raise NotImplementedError

    def check_health(self) -> tuple[bool, float]:
        """Check ArcadeDB availability and return reachability and latency."""
        raise NotImplementedError

    def close(self) -> None:
        """Close all pooled ArcadeDB connections and release backend resources."""
        raise NotImplementedError
