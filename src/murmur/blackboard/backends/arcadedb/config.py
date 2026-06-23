from __future__ import annotations

from dataclasses import dataclass

from ..base import BackendConfig


@dataclass(slots=True)
class ArcadeDBConfig(BackendConfig):
    database_path: str = ""
    jvm_heap_size: str = "2g"
    wal_flush_mode: str = "yes_nometadata"
    read_your_writes: bool = True
