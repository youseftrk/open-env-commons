"""Validate env.json against schema + local quality gates G0/G1/G4."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from envc.device_map import CAPTURE_MODE_TO_DEVICE_CLASS, SCHEMA_ID

# schema lives at repo root schemas/; also copied next to package for installs
_SCHEMA_CANDIDATES = [
    Path(__file__).resolve().parents[2] / "schemas" / "env.manifest.0.1.json",
    Path(__file__).resolve().parent / "data" / "env.manifest.0.1.json",
]


def load_schema() -> dict[str, Any]:
    for path in _SCHEMA_CANDIDATES:
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    raise FileNotFoundError(
        "schemas/env.manifest.0.1.json not found; run from the open-env-commons checkout "
        "or install the package with schema data."
    )


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ValidationReport:
    path: Path
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    gates: list[GateResult] = field(default_factory=list)
    manifest: dict[str, Any] | None = None

    def summary_lines(self) -> list[str]:
        lines = [f"validate: {self.path}"]
        for g in self.gates:
            mark = "PASS" if g.passed else "FAIL"
            extra = f" — {g.detail}" if g.detail else ""
            lines.append(f"  [{mark}] {g.name}{extra}")
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARN: {w}")
        lines.append("OK" if self.ok else "FAILED")
        return lines


def _preview_paths(manifest: dict[str, Any], root: Path) -> list[Path]:
    previews = (manifest.get("assets") or {}).get("previews") or {}
    out: list[Path] = []
    for key in ("point_cloud_thumb", "depth_thumb", "photoreal_still"):
        rel = previews.get(key)
        if rel:
            out.append(root / rel)
    return out


def _package_link_ok(capture: dict[str, Any]) -> bool:
    pkg = capture.get("package") or {}
    path = pkg.get("path")
    uri = pkg.get("uri")
    return bool(path) or bool(uri)


def validate_env(path: Path | str) -> ValidationReport:
    root = Path(path).resolve()
    if root.is_file() and root.name == "env.json":
        env_path = root
        root = root.parent
    else:
        env_path = root / "env.json"

    report = ValidationReport(path=env_path, ok=False)
    if not env_path.is_file():
        report.errors.append(f"missing {env_path}")
        report.gates.append(GateResult("G0_schema", False, "env.json missing"))
        return report

    try:
        manifest = json.loads(env_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"invalid JSON: {exc}")
        report.gates.append(GateResult("G0_schema", False, "invalid JSON"))
        return report

    report.manifest = manifest
    schema = load_schema()
    validator = Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))
    for err in schema_errors:
        loc = ".".join(str(p) for p in err.path) or "(root)"
        report.errors.append(f"{loc}: {err.message}")

    # device-class map consistency
    capture = manifest.get("capture") or {}
    mode = capture.get("capture_mode")
    device = capture.get("capture_device_class")
    if mode in CAPTURE_MODE_TO_DEVICE_CLASS:
        expected = CAPTURE_MODE_TO_DEVICE_CLASS[mode]
        if device and device != expected:
            report.errors.append(
                f"capture.capture_device_class {device!r} does not match "
                f"capture_mode {mode!r} (expected {expected!r})"
            )
    if not _package_link_ok(capture):
        report.errors.append("capture.package must set path or uri")

    license_code = (manifest.get("license") or {}).get("code")
    license_ok = license_code in ("CC-BY-4.0", "CC0")
    if not license_ok:
        report.errors.append("license.code must be CC-BY-4.0 or CC0")

    g0_ok = len(report.errors) == 0
    report.gates.append(
        GateResult("G0_schema", g0_ok, "env.json + license" if g0_ok else "see errors")
    )

    # G1_preview: ≥1 preview thumb exists on disk
    preview_files = _preview_paths(manifest, root)
    existing = [p for p in preview_files if p.is_file()]
    g1_ok = len(existing) >= 1
    report.gates.append(
        GateResult(
            "G1_preview",
            g1_ok,
            f"{len(existing)}/{len(preview_files)} preview files present"
            if preview_files
            else "no preview paths declared",
        )
    )
    if not g1_ok:
        report.errors.append(
            "G1_preview: need ≥1 of point_cloud_thumb / depth_thumb / photoreal_still on disk"
        )

    # G4_attrib: contributors complete (name + role)
    contributors = (manifest.get("attribution") or {}).get("contributors") or []
    g4_ok = bool(contributors) and all(
        isinstance(c, dict) and c.get("name") and c.get("role") for c in contributors
    )
    report.gates.append(
        GateResult(
            "G4_attrib",
            g4_ok,
            f"{len(contributors)} contributor(s)" if contributors else "none",
        )
    )
    if not g4_ok:
        report.errors.append("G4_attrib: contributors must each have name and role")

    # G2/G3 deferred (collision load / sim smoke)
    report.warnings.append("G2_collision / G3_sim_smoke not enforced in v0 CLI")

    report.ok = g0_ok and g1_ok and g4_ok
    return report
