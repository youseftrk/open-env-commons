"""Local paths for the envc registry (no network)."""

from __future__ import annotations

import os
from pathlib import Path


def envc_home() -> Path:
    override = os.environ.get("ENVC_HOME")
    if override:
        return Path(override).expanduser().resolve()
    return (Path.home() / ".envc").resolve()


def registry_dir() -> Path:
    return envc_home() / "registry"


def index_path() -> Path:
    return registry_dir() / "registry.json"
