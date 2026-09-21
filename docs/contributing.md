> **Status:** draft — do not publish until the GitHub org (`youseftrk`) is confirmed.

# Contributing — open-env-commons

## Do not publish yet

Placeholder org: `youseftrk`. Do not publish until the GitHub organization is confirmed.

## Code vs data

| Contribution | License |
|--------------|---------|
| Code (`envc`, schemas-as-code, registry) | **Apache-2.0** only |
| Environment packages / assets | **CC-BY-4.0** default; **CC0** allowed |

No copyleft. DCO-style expectation for code PRs.

## PR bar

1. Manifest changes must keep `schema: open-real2sim.env.manifest/0.1` field names and the Capture device-class map.
2. CLI user-facing name stays **`envc`**.
3. Gates G0–G4 remain progressive; G4 means **attribution completeness** only in public docs.
4. Do not add marketplace checkout, payments, or public incentive copy in v0.
5. Env packages must declare a data license (CC-BY-4.0 or CC0) and pass `envc validate`.
6. Clean-room messaging: describe Open Real2Sim on its own terms.

## License checklist

- [ ] Code Apache-2.0; no copyleft deps.
- [ ] New example envs ship `LICENSE` with CC-BY-4.0 or CC0.
- [ ] `capture.session_mcap_sha256` and package link present when claiming a Capture session.
- [ ] No PII in previews or provenance notes.
