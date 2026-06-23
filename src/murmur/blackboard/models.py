from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, NewType

if TYPE_CHECKING:
    from .locks.models import AgentIdentity

type PropertyValue = str | int | float | bool | datetime | list[Any] | None

NodeId = NewType("NodeId", str)
EdgeId = NewType("EdgeId", str)


@dataclass(slots=True)
class Node:
    id: NodeId
    node_type: str
    properties: dict[str, PropertyValue] = field(default_factory=dict)
    status: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(datetime.UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(datetime.UTC))


@dataclass(slots=True)
class Edge:
    id: EdgeId
    edge_type: str
    from_node_id: NodeId
    to_node_id: NodeId
    properties: dict[str, PropertyValue] = field(default_factory=dict)


@dataclass(slots=True)
class Subgraph:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)


@dataclass(slots=True)
class LockResult:
    acquired: bool
    holder: AgentIdentity | None
    ttl_seconds: int | None


@dataclass(slots=True)
class HealthStatus:
    reachable: bool
    schema_valid: bool
    backend_name: str
    latency_ms: float


@dataclass(slots=True)
class StatusTransition:
    from_status: str
    to_status: str
