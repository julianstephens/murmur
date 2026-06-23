from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..models import NodeId


@dataclass(slots=True)
class AgentIdentity:
    agent_type: str
    instance_id: str


@dataclass(slots=True)
class LockRecord:
    locked_node_id: NodeId
    holder: AgentIdentity
    acquired_at: datetime
    expires_at: datetime
