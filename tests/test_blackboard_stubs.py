from __future__ import annotations

from murmur.blackboard import (
    ActivationQueryDefinition,
    AgentIdentity,
    Blackboard,
    BlackboardConfig,
    EdgeTypeDefinition,
    FilterOperator,
    NodeTypeDefinition,
    PropertyFilter,
    TransitionGraph,
)
from murmur.blackboard.backends.base import BackendConfig
from murmur.blackboard.schema.base import (
    build_base_edge_type_definitions,
    build_base_node_type_definitions,
)


def test_public_exports_are_importable() -> None:
    definition = ActivationQueryDefinition(node_type="TaskNode")
    condition = PropertyFilter(
        property="priority", operator=FilterOperator.EQUALS, value=1
    )
    identity = AgentIdentity(agent_type="worker", instance_id="a1")
    transition_graph = TransitionGraph({"A": {"B"}})
    node_type = NodeTypeDefinition("CustomNode", {}, {}, set(), transition_graph)
    edge_type = EdgeTypeDefinition("CUSTOM_EDGE", {"A"}, {"B"}, {}, {})

    assert definition.node_type == "TaskNode"
    assert condition.value == 1
    assert identity.instance_id == "a1"
    assert node_type.name == "CustomNode"
    assert edge_type.name == "CUSTOM_EDGE"


def test_base_schema_definitions_have_framework_types() -> None:
    assert len(build_base_node_type_definitions()) == 9
    assert len(build_base_edge_type_definitions()) == 8


def test_blackboard_memory_health_fails_gracefully_for_stub_schema_manager() -> None:
    blackboard = Blackboard(
        BlackboardConfig(backend="memory", connection=BackendConfig())
    )

    try:
        status = blackboard.health()
        assert status.reachable is False
        assert status.schema_valid is False
    finally:
        blackboard.close()
