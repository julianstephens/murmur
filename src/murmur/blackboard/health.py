from __future__ import annotations

from .backends.base import BackendAdapter
from .models import HealthStatus
from .schema.manager import SchemaManager


class HealthChecker:
    def __init__(self, adapter: BackendAdapter, schema_manager: SchemaManager) -> None:
        self._adapter = adapter
        self._schema_manager = schema_manager

    def check(self) -> HealthStatus:
        """Return aggregate backend and schema health information for the blackboard."""
        try:
            reachable, latency_ms = self._adapter.check_health()
        except Exception:
            return HealthStatus(
                reachable=False,
                schema_valid=False,
                backend_name=type(self._adapter).__name__,
                latency_ms=0.0,
            )

        try:
            schema_valid = self._schema_manager.validate_runtime()
        except Exception:
            schema_valid = False
            reachable = False

        return HealthStatus(
            reachable=reachable,
            schema_valid=schema_valid,
            backend_name=type(self._adapter).__name__,
            latency_ms=latency_ms,
        )
