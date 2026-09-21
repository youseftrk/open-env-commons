"""Filesystem registry under ~/.envc/registry (or $ENVC_HOME/registry)."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from envc.paths import index_path, registry_dir
from envc.validate import validate_env


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_registry() -> Path:
    root = registry_dir()
    root.mkdir(parents=True, exist_ok=True)
    idx = index_path()
    if not idx.is_file():
        idx.write_text(json.dumps({"schema": "envc.registry/0.1", "entries": []}, indent=2) + "\n", encoding="utf-8")
    return root


def load_index() -> dict[str, Any]:
    ensure_registry()
    return json.loads(index_path().read_text(encoding="utf-8"))


def save_index(data: dict[str, Any]) -> None:
    ensure_registry()
    index_path().write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _safe_id_dirname(env_id: str) -> str:
    # env:org/slug@1.2.3 → org__slug__1.2.3
    assert env_id.startswith("env:")
    body = env_id[4:]
    org, rest = body.split("/", 1)
    slug, ver = rest.rsplit("@", 1)
    return f"{org}__{slug}__{ver}"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _maybe_fill_mcap_hash(manifest: dict[str, Any], root: Path) -> str | None:
    """If package.path points at a local .mcap (or dir with one), hash it; else leave as-is."""
    capture = manifest.get("capture") or {}
    existing = capture.get("session_mcap_sha256")
    if existing and len(existing) == 64 and all(c in "0123456789abcdefABCDEF" for c in existing):
        return None
    pkg = capture.get("package") or {}
    rel = pkg.get("path")
    if not rel:
        return None
    target = (root / rel).resolve()
    mcap: Path | None = None
    if target.is_file() and target.suffix == ".mcap":
        mcap = target
    elif target.is_dir():
        matches = list(target.glob("*.mcap"))
        if len(matches) == 1:
            mcap = matches[0]
    if mcap is None:
        return None
    digest = _sha256_file(mcap)
    capture["session_mcap_sha256"] = digest
    return digest


def publish(path: Path | str) -> dict[str, Any]:
    root = Path(path).resolve()
    if root.is_file() and root.name == "env.json":
        root = root.parent
    report = validate_env(root)
    if not report.ok or report.manifest is None:
        raise ValueError("publish blocked: validation failed\n" + "\n".join(report.summary_lines()))

    manifest = json.loads((root / "env.json").read_text(encoding="utf-8"))
    filled = _maybe_fill_mcap_hash(manifest, root)
    if filled:
        (root / "env.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    env_id = manifest["id"]
    dest = ensure_registry() / _safe_id_dirname(env_id)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        root,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".venv"),
    )

    # bump quality status locally
    published_manifest = json.loads((dest / "env.json").read_text(encoding="utf-8"))
    quality = published_manifest.setdefault("quality", {})
    gates = list(quality.get("gates_passed") or [])
    for g in ("G0_schema", "G1_preview", "G4_attrib"):
        if g not in gates:
            gates.append(g)
    quality["gates_passed"] = gates
    if quality.get("status") == "draft":
        quality["status"] = "local_ok"
    (dest / "env.json").write_text(json.dumps(published_manifest, indent=2) + "\n", encoding="utf-8")

    idx = load_index()
    entries = [e for e in idx.get("entries", []) if e.get("id") != env_id]
    entry = {
        "id": env_id,
        "name": published_manifest.get("name"),
        "category": published_manifest.get("category"),
        "path": str(dest),
        "published_at": _now_iso(),
        "quality_status": published_manifest.get("quality", {}).get("status"),
    }
    entries.append(entry)
    entries.sort(key=lambda e: e["id"])
    idx["entries"] = entries
    idx["updated_at"] = _now_iso()
    save_index(idx)
    return entry


def list_entries() -> list[dict[str, Any]]:
    return list(load_index().get("entries") or [])


def get_entry(env_id: str) -> dict[str, Any]:
    for entry in list_entries():
        if entry.get("id") == env_id:
            path = Path(entry["path"])
            manifest = json.loads((path / "env.json").read_text(encoding="utf-8"))
            return {"entry": entry, "manifest": manifest, "path": str(path)}
    raise KeyError(f"not found in local registry: {env_id}")


def export_index() -> Path:
    ensure_registry()
    return index_path()
