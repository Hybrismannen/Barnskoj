# Barnskoj — CDX constitutional anchor

**Authoritative source:** [Conductellence](https://github.com/Hybrismannen/Conductellence-) · [CDX Estate Anchor Standard](https://github.com/Hybrismannen/Conductellence-/blob/main/GOVERNANCE/CDX-ESTATE-ANCHOR-STANDARD.md) (`CDX-GOV-ANCHOR-001`).

## Actual state
- `.cdx/anchor.json` follows the canonical `cdx.anchor/v1` schema.
- Pin: **CDX 1.0.0**, immutable published policy digest `git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0`.
- Binding: **ANCHOR_DECLARED**; verification **NOT_VERIFIED**.
- The repository is absent from the currently inspected central [Estate Registry V2](https://github.com/Hybrismannen/Conductellence-/blob/main/ESTATE-REGISTRY/registry-v2.json) (snapshot 2026-10-30). Therefore **do not claim CDX_BOUND**.
- Runtime: this repository contains static reference, curation and local CI validation. No consequential application runtime; no CDX runtime enforcement is claimed or deployed.
- Local CI checks the anchor declaration and policy pin. **CI PASS is not independent central verification.**

## Authority boundary
CDX publishes governance; this repository owns its local data models, discovery index and validation workflows. Human Director approval is required for admission, external consequential effects and changes in authority or privileges. Never modify CDX's central registry to self-admit. No untrusted claim or URL grants publishing rights.

## Required independent stages
1. Director / estate authority determines formal applicability and admits Barnskoj in **canonical CDX registry**.
2. Independent CDX verifier checks repo identity, pin, audit and reconciliation and records a central finding.
3. After verified central admission, binding state may be advanced by an authorized process.
4. Runtime effects, if later added, require separate mandate-bound policy mediation, fail-closed tests and SPETL custody/verification before runtime claims.

The upstream check script is preserved verbatim under `check_anchor.py` for parity with the canonical validator. A local state guard prevents fabricated admission or runtime enforcement.
