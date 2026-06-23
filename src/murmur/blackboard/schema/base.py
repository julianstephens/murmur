from __future__ import annotations

from datetime import datetime

from ..edges.registry import EdgeTypeDefinition
from ..edges.types import (
    ESCALATED_TO,
    HAS_APPROVAL,
    HAS_CONTEXT_PACK,
    HAS_EVIDENCE,
    HAS_EXECUTION,
    HAS_PROPOSAL,
    HAS_TASK,
    LOCKED_BY,
)
from ..nodes.registry import NodeTypeDefinition
from ..nodes.transitions import NODE_TRANSITION_GRAPHS
from ..nodes.types import (
    AGENT_LOCK_NODE,
    APPROVAL_NODE,
    CONTEXT_PACK_NODE,
    EVIDENCE_NODE,
    EXECUTION_NODE,
    MANUAL_REVIEW_NODE,
    PROPOSAL_NODE,
    TASK_NODE,
    WORKFLOW_NODE,
)
from .versions import CURRENT_VERSION

BASE_SCHEMA_VERSION = CURRENT_VERSION
RESERVED_PROPERTY_NAMES: set[str] = {
    "_node_id",
    "_murmur_type",
    "_schema_version",
    "_created_at",
    "_updated_at",
}


def build_base_node_type_definitions() -> list[NodeTypeDefinition]:
    return [
        NodeTypeDefinition(
            name=WORKFLOW_NODE,
            required_properties={"workflow_id": str},
            optional_properties={"name": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[WORKFLOW_NODE],
        ),
        NodeTypeDefinition(
            name=TASK_NODE,
            required_properties={"task_id": str},
            optional_properties={"priority": int},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[TASK_NODE],
        ),
        NodeTypeDefinition(
            name=AGENT_LOCK_NODE,
            required_properties={"expires_at": datetime},
            optional_properties={"holder": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[AGENT_LOCK_NODE],
        ),
        NodeTypeDefinition(
            name=EVIDENCE_NODE,
            required_properties={"kind": str},
            optional_properties={"uri": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[EVIDENCE_NODE],
        ),
        NodeTypeDefinition(
            name=CONTEXT_PACK_NODE,
            required_properties={"context_type": str},
            optional_properties={"summary": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[CONTEXT_PACK_NODE],
        ),
        NodeTypeDefinition(
            name=PROPOSAL_NODE,
            required_properties={"proposal_id": str},
            optional_properties={"summary": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[PROPOSAL_NODE],
        ),
        NodeTypeDefinition(
            name=APPROVAL_NODE,
            required_properties={"approver": str},
            optional_properties={"decision_notes": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[APPROVAL_NODE],
        ),
        NodeTypeDefinition(
            name=EXECUTION_NODE,
            required_properties={"execution_id": str},
            optional_properties={"executor": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[EXECUTION_NODE],
        ),
        NodeTypeDefinition(
            name=MANUAL_REVIEW_NODE,
            required_properties={"reason": str},
            optional_properties={"reviewer": str},
            system_properties=RESERVED_PROPERTY_NAMES,
            transition_graph=NODE_TRANSITION_GRAPHS[MANUAL_REVIEW_NODE],
        ),
    ]


def build_base_edge_type_definitions() -> list[EdgeTypeDefinition]:
    return [
        EdgeTypeDefinition(
            name=HAS_TASK,
            allowed_from_types={WORKFLOW_NODE},
            allowed_to_types={TASK_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=HAS_EVIDENCE,
            allowed_from_types={TASK_NODE, EXECUTION_NODE, PROPOSAL_NODE},
            allowed_to_types={EVIDENCE_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=HAS_CONTEXT_PACK,
            allowed_from_types={WORKFLOW_NODE, TASK_NODE},
            allowed_to_types={CONTEXT_PACK_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=HAS_PROPOSAL,
            allowed_from_types={TASK_NODE, WORKFLOW_NODE},
            allowed_to_types={PROPOSAL_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=HAS_APPROVAL,
            allowed_from_types={PROPOSAL_NODE, TASK_NODE},
            allowed_to_types={APPROVAL_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=HAS_EXECUTION,
            allowed_from_types={TASK_NODE, APPROVAL_NODE},
            allowed_to_types={EXECUTION_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=ESCALATED_TO,
            allowed_from_types={TASK_NODE},
            allowed_to_types={MANUAL_REVIEW_NODE},
            required_properties={},
            optional_properties={},
        ),
        EdgeTypeDefinition(
            name=LOCKED_BY,
            allowed_from_types={TASK_NODE, WORKFLOW_NODE},
            allowed_to_types={AGENT_LOCK_NODE},
            required_properties={"holder": str},
            optional_properties={"ttl_seconds": int},
        ),
    ]
