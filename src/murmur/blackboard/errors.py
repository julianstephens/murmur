from __future__ import annotations

from murmur.errors import MurmurError


class BlackboardError(MurmurError):
    """Base exception for blackboard package errors."""


class NodeNotFoundError(BlackboardError):
    """Raised when a requested node cannot be found."""


class EdgeNotFoundError(BlackboardError):
    """Raised when a requested edge cannot be found."""


class LockAcquisitionError(BlackboardError):
    """Raised when lock acquisition fails."""


class LockNotHeldError(BlackboardError):
    """Raised when trying to release a lock not held by caller."""


class InvalidStatusTransitionError(BlackboardError):
    """Raised when a node status transition is not allowed."""


class SchemaConflictError(BlackboardError):
    """Raised when schema extensions conflict with existing schema."""


class SchemaVersionError(BlackboardError):
    """Raised when schema version constraints are violated."""


class BackendConnectionError(BlackboardError):
    """Raised when backend connection management fails."""


class ConnectionPoolExhaustedError(BlackboardError):
    """Raised when no backend connection can be acquired in time."""


class TransactionError(BlackboardError):
    """Raised when transaction lifecycle operations fail."""


class InvalidQueryError(BlackboardError):
    """Raised when a query cannot be validated or constructed."""


class TypeConversionError(BlackboardError):
    """Raised when value conversion between Python and backend types fails."""
