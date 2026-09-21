# open-env-commons

I built a shared library so people can publish room copies and get credit.

Local registry CLI (`envc`) + `env.json` manifest schema for Real2Sim environment packages. Apache-2.0 code; environment data defaults to **CC-BY-4.0** (CC0 ok). Filesystem registry only in v0 — no accounts, no network.

## Install

```bash
cd open-env-commons
pip install -e .
```

## Quickstart

```bash
envc init my-kitchen --org you
# edit env.json (capture session + attribution), then:
envc validate ./my-kitchen
envc publish ./my-kitchen
envc list
envc get env:you/my-kitchen@0.1.0
```

Registry root: `~/.envc/registry/` (or `$ENVC_HOME/registry`).

Try the bundled example:

```bash
envc validate examples/bedroom-phone-scan
envc publish examples/bedroom-phone-scan
envc list
envc get env:you/bedroom-phone-scan@0.1.0
```

## Manifest sketch

Schema id: `open-real2sim.env.manifest/0.1` — see [`ENV_MANIFEST_v0.md`](ENV_MANIFEST_v0.md) and [`schemas/env.manifest.0.1.json`](schemas/env.manifest.0.1.json).

Capture mode → device class: `robot_ros2`→`robot_onboard`, `android`/`ios_later`→`handheld_phone`, `tablet_android`→`handheld_tablet`. Default category: `home_indoor`.

Local gates enforced by `envc validate` / `publish`: **G0_schema**, **G1_preview**, **G4_attrib**. G2/G3 deferred.

## License

Code: [Apache-2.0](LICENSE). Data contributions: CC-BY-4.0 default — see [`docs/data-license.md`](docs/data-license.md).
