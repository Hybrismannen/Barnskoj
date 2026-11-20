#!/usr/bin/env python3
"""Barnskoj production gate: no licensed images, print sheets or rights invented."""
import csv
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
def load(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
def fail(msg):
    ERRORS.append(msg)
def run():
    activities = load("production/activities.csv")
    assets = load("production/assets.csv")
    motifs = {m["id"] for m in json.loads((ROOT / "creative/motifs.json").read_text(encoding="utf-8"))}
    formats = {f["id"] for f in json.loads((ROOT / "creative/formats.json").read_text(encoding="utf-8"))}
    aids = set()
    file_ids = set()
    for a in assets:
        ident = a["asset_id"]
        if not ident or ident in file_ids:
            fail("Duplicate/blank asset ID: " + ident)
        file_ids.add(ident)
        if a["activity_id"] and not any(x["activity_id"] == a["activity_id"] for x in activities):
            fail("Orphan asset: " + ident)
        if a["source_path"] and not (ROOT / a["source_path"]).is_file():
            fail("Missing asset source file: " + ident)
        if a["rights_status"] == "CLEARED" and not a["license_basis"]:
            fail("Cleared asset with no documented licence basis: " + ident)
    asset_lookup = {a["asset_id"]: a for a in assets}
    for a in activities:
        id = a["activity_id"]
        if not id or id in aids:
            fail("Duplicate/blank activity ID: " + id)
        aids.add(id)
        if a["motif_id"] not in motifs:
            fail("Unknown motif ID: " + id)
        if a["format_id"] not in formats:
            fail("Unknown format ID: " + id)
        if a["status"] not in {"prototype", "tested", "published"}:
            fail("Invalid production status: " + id)
        if a["status"] == "published":
            for name in ("rights_review", "print_review", "accessibility_review", "human_review"):
                if a[name] != "PASS":
                    fail("Publication missing " + name + ": " + id)
            ids = [a["asset_id"]]
            if a["requires_solution"] == "yes":
                ids.append(a["solution_asset_id"])
            for asset_id in ids:
                asset = asset_lookup.get(asset_id)
                if not asset:
                    fail("Missing required published asset: " + id)
                elif (asset["rights_status"] != "CLEARED" or
                      asset["technical_qa"] != "PASS" or asset["accessibility_qa"] != "PASS" or
                      not asset["source_path"]):
                    fail("Published asset not cleared/QA verified: " + asset_id)
            if not a["published_at"]:
                fail("Publication missing date: " + id)
    report = {"result": "FAIL" if ERRORS else "PASS", "activities": len(activities),
              "assets": len(assets), "published": sum(a["status"] == "published" for a in activities),
              "errors": ERRORS}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if ERRORS else 0
if __name__ == "__main__":
    sys.exit(run())
