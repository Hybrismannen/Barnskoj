#!/usr/bin/env python3
"""Read-only Barnskoj production preflight; never promotes a WP or activity."""
import argparse
import csv
import json
from pathlib import Path
from check_wp_prerequisites import build as prerequisite_status

ROOT = Path(__file__).resolve().parents[1]

def csvrows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def preflight():
    upstream = prerequisite_status()
    activities = csvrows("production/activities.csv")
    decisions = csvrows("rights/decisions.csv")
    unresolved = [
        r["activity_id"] for r in activities
        if r["rights_review"] != "PASS"
        or r["print_review"] != "PASS"
        or r["accessibility_review"] != "PASS"
        or r["human_review"] != "PASS"
    ]
    external_ready = upstream["readiness"] == "READY_FOR_HUMAN_WP_REVIEW"
    return {
        "schema": "barnskoj.production-preflight/v1",
        "mode": "READ_ONLY",
        "prerequisite_status": upstream["readiness"],
        "prerequisite_blockers": upstream["blockers"],
        "wiki_remote_verified": upstream["wiki_remote_publication_verified"],
        "image_provenance_verified": upstream["original_images_confirmed"],
        "image_provenance_required": upstream["original_image_requirements"],
        "activity_count": len(activities),
        "activities_without_all_four_human_reviews": len(unresolved),
        "unreviewed_activity_ids": unresolved,
        "human_rights_decisions_recorded": len(decisions),
        "new_WP_eligible_for_human_review": external_ready,
        "activity_publication_approved": False,
        "central_CDX_admission_verified_by_this_script": False,
        "note": "READY_FOR_HUMAN_WP_REVIEW never means licensed, published, or approved for commercial distribution."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--require-ready", action="store_true")
    args = p.parse_args()
    result = preflight()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.require_ready and not result["new_WP_eligible_for_human_review"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
