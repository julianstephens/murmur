from __future__ import annotations

import threading


class MemoryStore:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: dict[tuple[str, str, str], dict] = {}
        self._lock = threading.RLock()

    def get_node(self, node_id: str) -> dict | None:
        with self._lock:
            return self.nodes.get(node_id)

    def put_node(self, node_id: str, data: dict) -> None:
        with self._lock:
            self.nodes[node_id] = dict(data)

    def delete_node(self, node_id: str) -> None:
        with self._lock:
            self.nodes.pop(node_id, None)

    def get_edges(self, from_id: str, edge_type: str) -> list[dict]:
        with self._lock:
            result: list[dict] = []
            for (stored_from_id, stored_edge_type, _), edge_data in self.edges.items():
                if stored_from_id == from_id and stored_edge_type == edge_type:
                    result.append(dict(edge_data))
            return result

    def put_edge(self, from_id: str, edge_type: str, to_id: str, data: dict) -> None:
        with self._lock:
            self.edges[(from_id, edge_type, to_id)] = dict(data)

    def delete_edge(self, from_id: str, edge_type: str, to_id: str) -> None:
        with self._lock:
            self.edges.pop((from_id, edge_type, to_id), None)

    def clear(self) -> None:
        with self._lock:
            self.nodes.clear()
            self.edges.clear()
