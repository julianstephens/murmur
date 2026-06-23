from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import InvalidStatusTransitionError
from .types import (
    AGENT_LOCK_NODE,
    APPROVAL_NODE,
    CONTEXT_PACK_NODE,
    EVIDENCE_NODE,
    EXECUTION_NODE,
    MANUAL_REVIEW_NODE,
    PROPOSAL_NODE,
    TASK_NODE,
    WORKFLOW_NODE,
    ApprovalStatus,
    ExecutionStatus,
    ProposalStatus,
    TaskStatus,
    WorkflowStatus,
)

if TYPE_CHECKING:
    from .registry import NodeTypeRegistry


class TransitionGraph:
    def __init__(self, transitions: dict[str, set[str]]) -> None:
        self._transitions = transitions

    def is_valid(self, from_status: str, to_status: str) -> bool:
        return to_status in self._transitions.get(from_status, set())


class TransitionValidator:
    def __init__(self, registry: NodeTypeRegistry) -> None:
        self._registry = registry

    def validate(self, node_type: str, from_status: str, to_status: str) -> None:
        definition = self._registry.get(node_type)
        transition_graph = definition.transition_graph
        if transition_graph is None or not transition_graph.is_valid(
            from_status, to_status
        ):
            msg = f"Invalid transition for {node_type}: {from_status} -> {to_status}"
            raise InvalidStatusTransitionError(msg)


WORKFLOW_TRANSITIONS = TransitionGraph(
    {
        WorkflowStatus.RECEIVED.value: {
            WorkflowStatus.RUNNING.value,
            WorkflowStatus.FAILED.value,
        },
        WorkflowStatus.RUNNING.value: {
            WorkflowStatus.WAITING_APPROVAL.value,
            WorkflowStatus.COMPLETED.value,
            WorkflowStatus.FAILED.value,
        },
        WorkflowStatus.WAITING_APPROVAL.value: {
            WorkflowStatus.RUNNING.value,
            WorkflowStatus.COMPLETED.value,
            WorkflowStatus.FAILED.value,
        },
    }
)

TASK_TRANSITIONS = TransitionGraph(
    {
        TaskStatus.PENDING.value: {
            TaskStatus.LOCKED.value,
            TaskStatus.MANUAL_REVIEW.value,
            TaskStatus.FAILED.value,
        },
        TaskStatus.LOCKED.value: {
            TaskStatus.RUNNING.value,
            TaskStatus.PENDING.value,
            TaskStatus.FAILED.value,
        },
        TaskStatus.RUNNING.value: {
            TaskStatus.COMPLETED.value,
            TaskStatus.MANUAL_REVIEW.value,
            TaskStatus.FAILED.value,
        },
        TaskStatus.MANUAL_REVIEW.value: {
            TaskStatus.PENDING.value,
            TaskStatus.COMPLETED.value,
            TaskStatus.FAILED.value,
        },
    }
)

PROPOSAL_TRANSITIONS = TransitionGraph(
    {
        ProposalStatus.DRAFT.value: {
            ProposalStatus.PENDING_APPROVAL.value,
            ProposalStatus.REJECTED.value,
        },
        ProposalStatus.PENDING_APPROVAL.value: {
            ProposalStatus.APPROVED.value,
            ProposalStatus.REJECTED.value,
        },
    }
)

EXECUTION_TRANSITIONS = TransitionGraph(
    {
        ExecutionStatus.PENDING.value: {
            ExecutionStatus.RUNNING.value,
            ExecutionStatus.FAILED.value,
        },
        ExecutionStatus.RUNNING.value: {
            ExecutionStatus.COMPLETED.value,
            ExecutionStatus.FAILED.value,
        },
    }
)

APPROVAL_TRANSITIONS = TransitionGraph(
    {
        ApprovalStatus.PENDING.value: {
            ApprovalStatus.APPROVED.value,
            ApprovalStatus.REJECTED.value,
        }
    }
)

AGENT_LOCK_TRANSITIONS = TransitionGraph({})
EVIDENCE_TRANSITIONS = TransitionGraph({})
CONTEXT_PACK_TRANSITIONS = TransitionGraph({})
MANUAL_REVIEW_TRANSITIONS = TransitionGraph({})

NODE_TRANSITION_GRAPHS = {
    WORKFLOW_NODE: WORKFLOW_TRANSITIONS,
    TASK_NODE: TASK_TRANSITIONS,
    AGENT_LOCK_NODE: AGENT_LOCK_TRANSITIONS,
    EVIDENCE_NODE: EVIDENCE_TRANSITIONS,
    CONTEXT_PACK_NODE: CONTEXT_PACK_TRANSITIONS,
    PROPOSAL_NODE: PROPOSAL_TRANSITIONS,
    APPROVAL_NODE: APPROVAL_TRANSITIONS,
    EXECUTION_NODE: EXECUTION_TRANSITIONS,
    MANUAL_REVIEW_NODE: MANUAL_REVIEW_TRANSITIONS,
}
