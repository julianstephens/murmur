from __future__ import annotations

from dataclasses import dataclass

from ..base import BackendConfig


@dataclass(slots=True)
class LadybugConfig(BackendConfig):
    database_path: str = ""
