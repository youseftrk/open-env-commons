# open-env-commons — v0 sketch

Apache-2.0 code. Data: **CC-BY-4.0** default (CC0 ok). Open protocols/APIs, not a closed marketplace. Token/crypto rewards are **hooks only** in v0 (no public copy).

Aligned with Capture Lead `CAPTURE_BAG_v0` + CTO demo notes (2026-09-21).

## Why this exists

Capture → Reconstruct → Sim Runtime need a shared way to name, package, attribute, and discover deployment-site twins. Env Commons owns that layer: **manifest schema + local registry CLI + quality gates**.

Sister projects:
- `open-real2sim-capture` — bags / sessions that feed reconstruction
- `open-physical-sim` — loads scene packages into Isaac Lab / MuJoCo / Genesis

## Environment ID

```
env:<org_or_user>/<slug>@<semver>
```

Immutable once published to a registry index. Mutations = new semver.

## Manifest (`env.json`)

### Capture mode → device class map

| Capture `capture_mode` | Env `capture_device_class` |
|------------------------|----------------------------|
| `robot_ros2` | `robot_onboard` |
| `android` | `handheld_phone` |
| `tablet_android` | `handheld_tablet` |
| `ios_later` | `handheld_phone` (v0 treat as phone path) |

Default contribution category for v0: **`home_indoor`**.

```json
{
  "schema": "open-real2sim.env.manifest/0.1",
  "id": "env:you/bedroom-phone-scan@0.1.0",
  "name": "Bedroom phone scan",
  "summary": "Indoor bedroom, handheld RGB(+depth).",
  "category": "home_indoor",
  "created_at": "2026-09-21T17:00:00Z",
  "license": {
    "code": "CC-BY-4.0",
    "url": null,
    "notes": "No PII / faces unblurred."
  },
  "attribution": {
    "contributors": [
      {
        "name": "Site Owner",
        "role": "scene_owner",
        "contact": "",
        "share": 0.5
      },
      {
        "name": "Sam",
        "role": "capture",
        "contact": "https://github.com/sam",
        "share": 0.5
      }
    ],
    "derived_from": []
  },
  "capture": {
    "session_id": "uuid-from-capture-manifest",
    "schema": "open-real2sim.capture.manifest/0.1",
    "capture_mode": "android",
    "capture_device_class": "handheld_phone",
    "package": {
      "path": "../captures/session_<uuid>/",
      "uri": null
    },
    "session_mcap_sha256": "hex-from-checksums.sha256-or-computed-on-publish",
    "purpose": "scene",
    "duration_s": 42.0,
    "created_at": "2026-09-21T16:50:00Z",
    "streams_present": ["rgb", "depth", "imu"],
    "calibration": {
      "rig_id": "phone_default",
      "method": "factory"
    }
  },
  "assets": {
    "visual": { "format": "3dgs", "path": "assets/visual/" },
    "collision": { "format": "mesh_urdf", "path": "assets/collision/" },
    "semantics": { "format": "openusd_labels", "path": "assets/semantics/", "optional": true },
    "previews": {
      "point_cloud_thumb": "assets/preview_pc.jpg",
      "depth_thumb": "assets/preview_depth.jpg",
      "photoreal_still": "assets/preview_rgb.jpg"
    }
  },
  "sim": {
    "targets": ["isaac_lab", "mujoco"],
    "units": "meters",
    "up_axis": "z",
    "origin": "capture_rig"
  },
  "quality": {
    "status": "draft",
    "tags": [],
    "gates_passed": [],
    "notes": ""
  },
  "rewards_hooks": {
    "enabled": false,
    "scheme": null,
    "reputation_weight": null
  }
}
```

### Required vs preferred (capture block)

**Required on env publish:** `session_id`, `schema`, `capture_mode` (+ derived `capture_device_class`), env `license`, env `attribution`, `session_mcap_sha256`, `package.path` or `package.uri`.

**Strongly preferred:** `purpose`, `duration_s`, `created_at`, `streams_present` (`depth`/`imu`/`lidar`/`pose`), `calibration.rig_id` + `calibration.method`.

Do **not** inline full `sensors.json` or the bag — Reconstruct reads those from the Capture session.

## Package layout

```
bedroom-phone-scan/
  env.json
  LICENSE
  NOTICE
  assets/
    preview_pc.jpg
    preview_depth.jpg
    preview_rgb.jpg
    visual/
    collision/
  checksums.sha256
```

## Local registry CLI (`envc`)

Matches CTO 48h: **publish / list / get**. Authoring helpers: `init`, `validate`.

```
envc init <slug>
envc validate [path]
envc publish [path]     # validate + hash mcap if needed + pack + add to ~/.envc/registry/
envc list
envc get <id>
envc export-index       # registry.json for mirrors / CI
```

v0 = filesystem + JSON index. No accounts, no payments.

## Quality gates

| Gate | Check |
|------|--------|
| `G0_schema` | `env.json` validates; data license present (CC-BY-4.0/CC0) |
| `G1_preview` | ≥1 of the three preview thumbs exists |
| `G2_collision` | collision mesh loads; units/up-axis match |
| `G3_sim_smoke` | empty-policy load in ≥1 declared sim target |
| `G4_attrib` | contributors complete (before any rewards hooks) |

`quality.status`: `draft` → `local_ok` → `sim_ok` → `published`.

## Docs gaps for OSS Docs README

- CLI name: **`envc`** (not `oec`)
- Quickstart should show `envc publish` / `list` / `get`
- Document `capture` block + device-class map
- Gate names G0–G4 + preview asset trio
- Default category `home_indoor`
- Reputation / optional bounty hooks only — never “token”

## Non-goals (v0)

- Closed marketplace
- On-chain / token rewards (hook fields only)
- Inlining Capture calib/bag
- Cloning proprietary InvLambda code
