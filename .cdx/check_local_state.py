#!/usr/bin/env python3
"""Barnskoj local CDX standing guard; complement to upstream reference anchor-check."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
a = json.loads((ROOT / ".cdx/anchor.json").read_text(encoding="utf-8"))
assert a["governed_surface"]["identity"] == "Hybrismannen/Barnskoj"
assert a["governed_surface"]["repository"] == "Hybrismannen/Barnskoj"
assert a["binding_mode"] == "PINNED_RELEASE"
assert a["policy_pin"] == {
    "ref_type": "RELEASE",
    "ref": "1.0.0",
    "digest": "git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0",
}
assert a["binding_state"] == "ANCHOR_DECLARED", "Central CDX verification is not admitted yet"
assert a["verification"]["verification_state"] == "NOT_VERIFIED"
assert a["verification"]["last_verified_at"] is None
assert a["conformance"]["runtime_state"] == "NOT_REQUIRED_BY_CURRENT_ROLE_STATIC_DATASET"
assert a["local_enforcement"]["fail_closed_for_consequential_effects"] is True
assert a["evidence"]["spetl_required"] is False, "No SPETL runtime is deployed"
print("PASS: pinned CDX declaration intact; admission/runtime NOT claimed")
