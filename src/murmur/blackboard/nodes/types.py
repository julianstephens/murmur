from __future__ import annotations

from enum import StrEnum

WORKFLOW_NODE = "WorkflowNode"
TASK_NODE = "TaskNode"
AGENT_LOCK_NODE = "AgentLockNode"
EVIDENCE_NODE = "EvidenceNode"
CONTEXT_PACK_NODE = "ContextPackNode"
PROPOSAL_NODE = "ProposalNode"
APPROVAL_NODE = "ApprovalNode"
EXECUTION_NODE = "ExecutionNode"
MANUAL_REVIEW_NODE = "ManualReviewNode"


class WorkflowStatus(StrEnum):
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    LOCKED = "LOCKED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class ProposalStatus(StrEnum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ExecutionStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ApprovalStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
