from __future__ import annotations

from ...locks.models import AgentIdentity
from ...models import NodeId
from ...queries.activation import ActivationQueryDefinition


class CypherBuilder:
    @staticmethod
    def create_node(node_type: str, properties: dict) -> tuple[str, dict]:
        return f"CREATE (n:{node_type} $properties) RETURN n", {
            "properties": properties
        }

    @staticmethod
    def match_node_by_id(node_id: NodeId) -> tuple[str, dict]:
        return "MATCH (n {_node_id: $node_id}) RETURN n", {"node_id": str(node_id)}

    @staticmethod
    def update_node(node_id: NodeId, properties: dict) -> tuple[str, dict]:
        return "MATCH (n {_node_id: $node_id}) SET n += $properties RETURN n", {
            "node_id": str(node_id),
            "properties": properties,
        }

    @staticmethod
    def delete_node(node_id: NodeId) -> tuple[str, dict]:
        return "MATCH (n {_node_id: $node_id}) DETACH DELETE n", {
            "node_id": str(node_id)
        }

    @staticmethod
    def transition_node_status(
        node_id: NodeId,
        current_status: str,
        new_status: str,
    ) -> tuple[str, dict]:
        return (
            "MATCH (n {_node_id: $node_id, status: $current_status}) "
            "SET n.status = $new_status RETURN n",
            {
                "node_id": str(node_id),
                "current_status": current_status,
                "new_status": new_status,
            },
        )

    @staticmethod
    def create_edge(
        edge_type: str,
        from_id: NodeId,
        to_id: NodeId,
        properties: dict,
    ) -> tuple[str, dict]:
        return (
            "MATCH (from {_node_id: $from_id}), (to {_node_id: $to_id}) "
            f"CREATE (from)-[e:{edge_type} $properties]->(to) RETURN e",
            {"from_id": str(from_id), "to_id": str(to_id), "properties": properties},
        )

    @staticmethod
    def match_edges(from_id: NodeId, edge_type: str) -> tuple[str, dict]:
        return (
            f"MATCH (from {{_node_id: $from_id}})-[e:{edge_type}]->(to) RETURN e, to",
            {"from_id": str(from_id)},
        )

    @staticmethod
    def delete_edge(edge_type: str, from_id: NodeId, to_id: NodeId) -> tuple[str, dict]:
        return (
            (
                "MATCH (from {_node_id: $from_id})"
                f"-[e:{edge_type}]->(to {{_node_id: $to_id}}) DELETE e"
            ),
            {"from_id": str(from_id), "to_id": str(to_id)},
        )

    @staticmethod
    def acquire_lock(
        node_id: NodeId,
        agent_identity: AgentIdentity,
        ttl_seconds: int,
    ) -> tuple[str, dict]:
        return (
            "MATCH (n {_node_id: $node_id}) "
            "SET n._lock_holder = $holder, n._lock_ttl_seconds = $ttl_seconds RETURN n",
            {
                "node_id": str(node_id),
                "holder": f"{agent_identity.agent_type}:{agent_identity.instance_id}",
                "ttl_seconds": ttl_seconds,
            },
        )

    @staticmethod
    def release_lock(
        node_id: NodeId, agent_identity: AgentIdentity
    ) -> tuple[str, dict]:
        return (
            "MATCH (n {_node_id: $node_id, _lock_holder: $holder}) "
            "REMOVE n._lock_holder, n._lock_ttl_seconds RETURN n",
            {
                "node_id": str(node_id),
                "holder": f"{agent_identity.agent_type}:{agent_identity.instance_id}",
            },
        )

    @staticmethod
    def find_expired_locks() -> tuple[str, dict]:
        return "MATCH (n) WHERE n._lock_ttl_seconds IS NOT NULL RETURN n", {}

    @staticmethod
    def activation_query(definition: ActivationQueryDefinition) -> tuple[str, dict]:
        statement = f"MATCH (n:{definition.node_type}) RETURN n"
        return statement, {"limit": definition.limit}

    @staticmethod
    def traverse(
        node_id: NodeId, depth: int, edge_types: list[str]
    ) -> tuple[str, dict]:
        statement = (
            "MATCH path = (start {_node_id: $node_id})-[*1..$depth]->(end) "
            "RETURN nodes(path) AS nodes, relationships(path) AS edges"
        )
        return statement, {
            "node_id": str(node_id),
            "depth": depth,
            "edge_types": edge_types,
        }
