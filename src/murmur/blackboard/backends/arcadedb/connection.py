from __future__ import annotations

import threading
from dataclasses import dataclass
from importlib import import_module
from types import TracebackType
from typing import Any

from ...errors import BackendConnectionError, ConnectionPoolExhaustedError
from .config import ArcadeDBConfig


@dataclass(slots=True)
class ThreadLocalConnection:
    """Context manager over a thread-local ArcadeDB Database instance."""

    database: Any

    def __enter__(self) -> Any:
        return self.database

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        return False


class ConnectionPool:
    def __init__(self, config: ArcadeDBConfig) -> None:
        self._config = config
        self._local = threading.local()
        self._connections: list[Any] = []
        self._lock = threading.RLock()

    def acquire(self) -> ThreadLocalConnection:
        with self._lock:
            db = getattr(self._local, "database", None)
            if db is not None:
                return ThreadLocalConnection(db)
            if len(self._connections) >= self._config.max_connections:
                msg = "ArcadeDB connection pool exhausted"
                raise ConnectionPoolExhaustedError(msg)
            db = self._create_database()
            self._connections.append(db)
            self._local.database = db
            return ThreadLocalConnection(self._local.database)

    def _create_database(self) -> Any:
        try:
            module = import_module("arcadedb")
        except Exception as exc:
            msg = "ArcadeDB client library is not installed"
            raise BackendConnectionError(msg) from exc

        database_class = getattr(module, "Database", None)
        if database_class is None:
            msg = "ArcadeDB Database class was not found in the installed package"
            raise BackendConnectionError(msg)

        return database_class(self._config.database_path)

    def close_all(self) -> None:
        with self._lock:
            for connection in self._connections:
                close = getattr(connection, "close", None)
                if callable(close):
                    close()
            self._connections.clear()
            if hasattr(self._local, "database"):
                del self._local.database

    def connection_count(self) -> int:
        with self._lock:
            return len(self._connections)
