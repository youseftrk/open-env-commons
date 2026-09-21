> **Status:** draft — do not publish until the GitHub org (`youseftrk`) is confirmed.

# Data license — open-env-commons

## Defaults

| Kind | License |
|------|---------|
| **Code** | **Apache-2.0** |
| **Environment / dataset contributions** | **CC-BY-4.0** (default) or **CC0** |

Declare the choice in `env.json` → `license.code` (SPDX) and ship a top-level `LICENSE` in the package.

## CC-BY-4.0

Keep attribution (contributors + license notice) when you redistribute the env. Compatible with commercial sim use when the notes allow it; authors may add constraints in `license.notes` (for example “no unblurred faces”).

## CC0

Allowed when the contributor waives attribution. Still fill structured `attribution` when known for provenance; waiver does not erase history.

## What is not a data license

Runtime code, `envc`, and schema validators remain Apache-2.0. Do not paste Creative Commons onto Python packages.

## v0 policy

Marketplace incentive programs are deferred and out of scope for v0 public documentation. Publishing an env grants reuse under the declared CC-BY-4.0 or CC0 terms only.
