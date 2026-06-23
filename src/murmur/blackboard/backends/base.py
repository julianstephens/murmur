from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class BackendConfig:
    max_connections: int = 10
    acquire_timeout_seconds: float = 5.0
    query_timeout_seconds: float = 30.0


class BackendAdapter(ABC):
    @abstractmethod
    def execute_write(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> None:
        """Execute a mutating statement with backend-specific parameter binding."""

    @abstractmethod
    def execute_read(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> list[dict]:
        """Execute a read statement and return backend rows as dictionaries."""

    @abstractmethod
    def execute_transaction(
        self,
        operations: list[tuple[str, dict]],
        connection_context: Any | None,
    ) -> None:
        """Execute an ordered list of write operations atomically."""

    @abstractmethod
    def check_health(self) -> tuple[bool, float]:
        """Return backend reachability and latency in milliseconds."""

    @abstractmethod
    def close(self) -> None:
        """Release all backend resources and close open connections."""
