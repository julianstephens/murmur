from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any

from .backends.base import BackendAdapter
from .errors import TransactionError


@dataclass(slots=True)
class TransactionContext:
    connection_context: Any
    is_nested: bool = False


class BlackboardTransaction:
    def __init__(self, adapter: BackendAdapter) -> None:
        self._adapter = adapter
        self._state = threading.local()

    def __enter__(self) -> TransactionContext:
        depth = getattr(self._state, "depth", 0)
        if depth > 0:
            self._state.depth = depth + 1
            return TransactionContext(
                connection_context=getattr(self._state, "connection_context", None),
                is_nested=True,
            )

        connection_context = None
        begin_transaction = getattr(self._adapter, "begin_transaction", None)
        if callable(begin_transaction):
            try:
                connection_context = begin_transaction()
            except Exception as exc:
                msg = "Failed to begin transaction"
                raise TransactionError(msg) from exc

        self._state.depth = 1
        self._state.connection_context = connection_context
        return TransactionContext(
            connection_context=connection_context, is_nested=False
        )

    def __exit__(self, exc_type, exc, tb) -> bool:
        depth = getattr(self._state, "depth", 0)
        if depth <= 0:
            return False

        self._state.depth = depth - 1
        if depth > 1:
            return False

        connection_context = getattr(self._state, "connection_context", None)
        try:
            if exc_type is None:
                commit_transaction = getattr(self._adapter, "commit_transaction", None)
                if callable(commit_transaction):
                    commit_transaction(connection_context)
            else:
                rollback_transaction = getattr(
                    self._adapter, "rollback_transaction", None
                )
                if callable(rollback_transaction):
                    rollback_transaction(connection_context)
        except Exception as transaction_exc:
            msg = "Transaction finalization failed"
            raise TransactionError(msg) from transaction_exc
        finally:
            self._state.connection_context = None
        return False
