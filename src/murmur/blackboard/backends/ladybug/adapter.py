from __future__ import annotations

from typing import Any

from ..base import BackendAdapter
from .config import LadybugConfig

_NOT_IMPLEMENTED = "LadybugDB backend is not yet implemented. Use the ArcadeDB backend."


class LadybugAdapter(BackendAdapter):
    def __init__(self, config: LadybugConfig) -> None:
        self.config = config

    def execute_write(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> None:
        """Execute a write statement when LadybugDB support is implemented."""
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def execute_read(
        self,
        statement: str,
        params: dict,
        connection_context: Any | None,
    ) -> list[dict]:
        """Execute a read statement when LadybugDB support is implemented."""
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def execute_transaction(
        self,
        operations: list[tuple[str, dict]],
        connection_context: Any | None,
    ) -> None:
        """Execute a transaction when LadybugDB support is implemented."""
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def check_health(self) -> tuple[bool, float]:
        """Check LadybugDB reachability when backend support is implemented."""
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def close(self) -> None:
        """Close LadybugDB resources when backend support is implemented."""
        raise NotImplementedError(_NOT_IMPLEMENTED)
