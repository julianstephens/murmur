from __future__ import annotations

from ..backends.base import BackendAdapter
from ..models import LockResult, NodeId
from .models import AgentIdentity


class LockManager:
    def __init__(self, adapter: BackendAdapter) -> None:
        self._adapter = adapter

    def acquire(
        self, node_id: NodeId, holder: AgentIdentity, ttl_seconds: int
    ) -> LockResult:
        """Acquire a distributed lock for a node on behalf of an agent identity."""
        raise NotImplementedError

    def is_locked(self, node_id: NodeId) -> bool:
        """Check whether the given node currently has an active lock."""
        raise NotImplementedError

    def release(self, node_id: NodeId, holder: AgentIdentity) -> None:
        """Release a lock when held by the provided agent identity."""
        raise NotImplementedError

    def reclaim_expired(self) -> int:
        """Find and reclaim expired locks, returning count of reclaimed locks."""
        raise NotImplementedError
