from __future__ import annotations

from typing import Any

from ..base import BackendAdapter
from .store import MemoryStore


class MemoryAdapter(BackendAdapter):
    def __init__(self) -> None:
        self.store = MemoryStore()

    def execute_write(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> None:
        """Execute a write statement when memory query parsing is implemented."""
        raise NotImplementedError("Memory backend query execution not yet implemented")

    def execute_read(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> list[dict]:
        """Execute a read statement when memory query parsing is implemented."""
        raise NotImplementedError("Memory backend query execution not yet implemented")

    def execute_transaction(
        self,
        operations: list[tuple[str, dict]],
        connection_context: Any | None,
    ) -> None:
        """Execute operations atomically once memory transactions are implemented."""
        raise NotImplementedError("Memory backend query execution not yet implemented")

    def check_health(self) -> tuple[bool, float]:
        """Return a healthy status for in-memory backend availability."""
        return True, 0.0

    def close(self) -> None:
        """Clear in-memory state and release memory backend resources."""
        self.store.clear()
