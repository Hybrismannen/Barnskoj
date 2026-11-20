#!/usr/bin/env python3
"""Read-only provenance audit; no source, identity or licence is auto-approved."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("images/requirements.csv", "images/staged_requirements.csv")
CONFIRMED = {"SOURCE_CONFIRMED", "RIGHTS_REVIEWED", "APPROVED_FOR_DESIGN"}

def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def audit():
    records = [r for path in SOURCES for r in rows(path)]
    targets = []
    for r in records:
        missing = []
        for field in ("image_page_url", "creator", "source_archive_reference"):
            if not r[field].strip():
                missing.append(field)
        if r["identity_confirmation"] != "CONFIRMED":
            missing.append("identity_confirmation")
        if r["source_examination"] != "VERIFIED":
            missing.append("source_examination")
        qualified = r["image_status"] in CONFIRMED and not missing
        rights_approved = (r["image_status"] == "APPROVED_FOR_DESIGN"
                          and r["rights_review"] == "APPROVED"
                          and bool(r["license_url"].strip()))
        targets.append({
            "target_id": r["target_id"],
            "image_status": r["image_status"],
            "source_page_present": bool(r["image_page_url"].strip()),
            "provenance_verified": qualified,
            "design_rights_approved": rights_approved,
            "missing_requirements": missing,
        })
    duplicates = [name for name, count in Counter(x["target_id"] for x in targets).items() if count != 1]
    counts = dict(sorted(Counter(x["image_status"] for x in targets).items()))
    ready = sum(r["provenance_verified"] for r in targets)
    return {
        "schema": "barnskoj.provenance-audit/v1",
        "read_only": True,
        "target_count": len(targets),
        "provenance_verified": ready,
        "provenance_unverified": len(targets) - ready,
        "design_rights_approved": sum(r["design_rights_approved"] for r in targets),
        "status_counts": counts,
        "duplicate_ids": sorted(duplicates),
        "targets": targets,
        "caveat": "A source-page lead is not a verified original, an image licence, or character reproduction permission."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--summary", action="store_true", help="Omit per-target details")
    p.add_argument("--require-complete", action="store_true", help="Exit 2 if provenance is not complete")
    args = p.parse_args()
    report = audit()
    if args.summary:
        report.pop("targets")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["duplicate_ids"]:
        return 1
    if args.require_complete and report["provenance_unverified"]:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
