# open-env-commons

Open registry and protocols for sharing Real2Sim environments: contributor attribution, quality gates, and APIs — not a closed marketplace.

> **Status:** draft skeleton. Planned repo: `youseftrk/open-env-commons`. Do not treat this as a public release until the GitHub org is confirmed.  
> **Affiliation:** clean-room open source. Not affiliated with any proprietary Real2Sim vendor. Inspired by public Real2Sim product demos where noted.

## Why this exists

Captured and reconstructed sites are only useful at scale if others can find them, trust their quality, and reuse them under clear licenses. Env Commons defines open protocols and a registry so robot owners and individuals can publish scenes with attribution and quality gates.

## Quickstart

```bash
# After install (stub; GitHub org TBD)
envc init my-kitchen
# fill env.json (see capture block below), then:
envc validate .
envc publish .          # pack + add to local registry
envc list
envc get env:you/my-kitchen@0.0.1
```

CLI entry is **`envc`** (not `oec`). v0 registry is local filesystem + JSON index.

### `capture` block (from CAPTURE_BAG_v0)

Required on publish when linking a Capture session: `session_id`, `schema` (`open-real2sim.capture.manifest/0.1`), `capture_mode`, `license`, `attribution`, `session_mcap_sha256`, and package link/path. Strongly preferred: `purpose`, `duration_s`, `created_at`, `streams_present`, `calibration.rig_id` + `method`. Do not inline full calib or the bag — Reconstruct reads sensors from the session.

Device-class map (`capture_mode` → Env Commons class):

| Capture `capture_mode` | Env Commons class |
|------------------------|-------------------|
| `robot_ros2` | `robot_onboard` |
| `android` | `handheld_phone` |
| `tablet_android` | `handheld_tablet` |

Default category: `home_indoor`. Optional preview trio: point cloud / depth / photoreal. Quality gates **G0–G4** (schema → preview → collision → sim smoke → attribution). See [`docs/schemas.md`](docs/schemas.md) and [`ENV_MANIFEST_v0.md`](../../open-env-commons/ENV_MANIFEST_v0.md) (authoritative sketch).

## How it fits Open Real2Sim

```
open-real2sim-capture → open-real2sim-reconstruct → open-physical-sim
                              ↘                         ↕
                               open-env-commons
```

## Docs

| Doc | Purpose |
|-----|---------|
| [`ENV_MANIFEST_v0.md`](ENV_MANIFEST_v0.md) | Authoritative v0 sketch |
| [`docs/architecture.md`](docs/architecture.md) | Registry model, gates |
| [`docs/schemas.md`](docs/schemas.md) | `env.json` + capture block |
| [`docs/data-license.md`](docs/data-license.md) | CC-BY-4.0 default; CC0 allowed |
| [`docs/contributing.md`](docs/contributing.md) | PR bar |

## License

Code: [Apache-2.0](LICENSE).  
Environment / dataset contributions: **CC-BY-4.0** by default; **CC0** allowed — see [`docs/data-license.md`](docs/data-license.md).

## Contributing

Read [`docs/contributing.md`](docs/contributing.md) before opening a PR. No crypto or token reward language in v0 docs or UX copy.

## Security

See [`SECURITY.md`](SECURITY.md).
