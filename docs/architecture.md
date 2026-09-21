> **Status:** draft — do not publish until the GitHub org (`youseftrk`) is confirmed.

# Architecture — open-env-commons

Env Commons owns the **naming, packaging, attribution, and local discovery** layer for deployment-site twins. It is open protocols and a filesystem registry — not a closed marketplace.

Code: Apache-2.0. Environment data: **CC-BY-4.0** default (**CC0** allowed).

## Role in Open Real2Sim

```
open-real2sim-capture → open-real2sim-reconstruct → open-physical-sim
                              ↘                ↕
                               open-env-commons (discover / share)
```

- **Does not replace** Capture bag format or Reconstruct exporters — manifests **reference** capture sessions and point at visual/collision assets those crews emit.
- **Physical Sim** loads an Env Commons package root (`env.json` + `assets/`) as one supported input beside Reconstruct `scene.json`.
- Locked public repos (CTO): capture, reconstruct, physical-sim, env-commons (see umbrella `DOC_MAP.md`).

## Components

| Component | Responsibility |
|-----------|----------------|
| `env.json` manifest | Identity, license, attribution, capture link, assets, sim targets, quality |
| Package layout | Preview thumbs, visual/, collision/, checksums |
| CLI **`envc`** | `init`, `validate`, `publish`, `list`, `get`, `export-index` |
| Local registry | `~/.envc/registry/` + JSON index (v0: no accounts, no remote push) |
| Quality gates G0–G4 | Progressive checks from schema → usable / attribution-complete |

CLI entry is **`envc`** (not `oec`).

## Data flow

1. Author runs `envc init <slug>` and fills `env.json` (including `capture` block when linking a session).
2. `envc validate` checks schema, license, required capture fields.
3. `envc publish` validates, hashes MCAP if needed, packs, and adds to the local registry.
4. `envc list` / `envc get <id>` resolve local records for Sim Runtime / CI.
5. Optional `envc export-index` writes `registry.json` for mirrors.

## Environment ID

```
env:<org_or_user>/<slug>@<semver>
```

Immutable once published to a registry index. Mutations require a new semver.

Default contribution **category** for v0: `home_indoor`.

## Capture linkage

Env packages that come from a real site link a Capture session via the `capture` block (session id, schema, mode, package path/uri, `session_mcap_sha256`). Device class is derived from Capture `capture_mode` (see [`schemas.md`](schemas.md)). Do **not** inline full `sensors.json` or the bag — Reconstruct reads those from the session.

## Quality gates (progressive)

| Gate | Check |
|------|--------|
| `G0_schema` | `env.json` validates; data license present (CC-BY-4.0 / CC0) |
| `G1_preview` | ≥1 of the three preview thumbs exists (pc / depth / photoreal) |
| `G2_collision` | Collision mesh loads; units / up-axis match |
| `G3_sim_smoke` | Empty-policy load in ≥1 declared sim target |
| `G4_attrib` | Contributors complete (**attribution completeness** — required before any future incentive hooks; those hooks are deferred and out of scope for v0 public docs) |

`quality.status`: `draft` → `local_ok` → `sim_ok` → `published` (mirror-ready, still not a marketplace).

## Ownership

| Surface | Owner |
|---------|-------|
| `env.json`, `envc`, gates, local registry | Env Commons |
| Capture session IDs + bag hashes | Capture Lead |
| `assets.visual` / `collision` format enums actually emitted | Reconstruct Eng |
| Loader for `sim.targets` | Sim Runtime |

## Non-goals (v0)

- Closed marketplace UX or exclusive hosting.
- Payments, accounts, or remote authenticated publish.
- On-chain or other incentive schemes in public docs (deferred; out of scope for v0).
- Inlining Capture calibration or MCAP into the env package.
- Replacing Capture or Reconstruct schemas.
