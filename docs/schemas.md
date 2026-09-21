> **Status:** public early draft — live under [`youseftrk`](https://github.com/youseftrk).

# Schemas — open-env-commons

This is for how a published room copy is described so others can find and credit it.

Authoritative sketch: `ENV_MANIFEST_v0.md`. Field names below are locked for public docs; do not invent alternate ids.

Schema id: `open-real2sim.env.manifest/0.1`

## Capture mode → device class

| Capture `capture_mode` | Env `capture_device_class` |
|------------------------|----------------------------|
| `robot_ros2` | `robot_onboard` |
| `android` | `handheld_phone` |
| `tablet_android` | `handheld_tablet` |
| `ios_later` | `handheld_phone` (v0 treat as phone path) |

Default category: **`home_indoor`**.

## `env.json` (public-safe example)

Incentive / rewards hook fields from internal sketches are **omitted** here — deferred; out of scope for v0.

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
  }
}
```

### `capture` block — required vs preferred

**Required on env publish:** `session_id`, `schema`, `capture_mode` (+ derived `capture_device_class`), env `license`, env `attribution`, `session_mcap_sha256`, `package.path` or `package.uri`.

**Strongly preferred:** `purpose`, `duration_s`, `created_at`, `streams_present` (`depth` / `imu` / `lidar` / `pose`), `calibration.rig_id` + `calibration.method`.

Do **not** inline full `sensors.json` or the bag.

### Attribution roles

| Role | Meaning |
|------|---------|
| `scene_owner` | Hosts the physical site / grants capture rights |
| `capture` | Ran the device/robot capture |
| `reconstruct` | Built the twin assets |
| `curator` | Packaged, licensed, QA'd the env |
| `other` | Free-text via notes on the contributor object |

`share` values should be non-negative when present; summing to 1.0 is recommended for clean attribution splits.

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

Optional preview trio: point cloud / depth / photoreal (`assets.previews.*`). G1 requires ≥1 thumb.

## CLI (`envc`)

```
envc init <slug>
envc validate [path]
envc publish [path]     # validate + hash mcap if needed + pack + add to ~/.envc/registry/
envc list
envc get <id>
envc export-index       # registry.json for mirrors / CI
```

v0 registry = filesystem + JSON index.

## Quality gates

| Gate | Check |
|------|--------|
| `G0_schema` | Manifest validates; data license CC-BY-4.0 or CC0 |
| `G1_preview` | ≥1 of preview_pc / preview_depth / preview_rgb |
| `G2_collision` | Collision loads; `sim.units` / `up_axis` match |
| `G3_sim_smoke` | Loads in ≥1 of `sim.targets` |
| `G4_attrib` | Attribution completeness (contributors filled) |

## Open API stubs (not implemented in v0)

Documented for forge-friendly mirrors later: `GET /v0/envs`, `GET /v0/envs/{id}`, etc. Content-addressed asset URIs preferred (`sha256:…` + optional HTTP locator).
