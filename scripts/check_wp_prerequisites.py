#!/usr/bin/env python3
"""Pre-WP gate: Wiki remote verification and 100% original-image provenance.

Returns 0 in --check/--build for structurally valid BLOCKED state, but
--require-ready fails until all external prerequisites really exist.
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import re
from collections import Counter

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"devops/PRE_WP_STATUS.json"

def readcsv(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def build():
    images=readcsv("images/requirements.csv")+readcsv("images/staged_requirements.csv")
    sources=readcsv("sourcing/wiki_sources.csv")
    wiki=json.loads((ROOT/"devops/WIKI_PUBLICATION.json").read_text(encoding="utf-8"))
    franchise=readcsv("sourcing/franchises.csv")
    allowed={"SOURCE_CONFIRMED","RIGHTS_REVIEWED","APPROVED_FOR_DESIGN"}
    complete=[]
    for r in images:
        if (r["image_status"] in allowed and r["identity_confirmation"]=="CONFIRMED"
                and r["source_examination"]=="VERIFIED"
                and r["image_page_url"] and r["creator"] and r["source_archive_reference"]):
            complete.append(r["target_id"])
    wiki_ok=(wiki.get("published") is True
            and bool(re.fullmatch(r"[0-9a-f]{40}",str(wiki.get("remote_commit_sha") or "")))
            and bool(wiki.get("verified_at")) and bool(wiki.get("verified_by")))
    stats=Counter(x["image_status"] for x in images)
    blockers=[]
    if not wiki_ok:
        blockers.append("Wiki pages have not been published AND remote SHA independently recorded")
    if len(complete)<len(images):
        blockers.append(f"{len(images)-len(complete)} image provenance records remain unverified")
    if len(sources)<1 or not franchise:
        blockers.append("No registered universe source network")
    return {
      "schema":"barnskoj.pre_wp/v2","reference_date":"2026-11-20",
      "historical_wps":"Previously committed WP01–WP03 remain in Git history; this gate is prospective.",
      "prerequisite_scope":"wiki_then_all_images_then_new_WP_signoff",
      "wiki_prepared":(ROOT/"wiki-src/Home.md").is_file(),
      "wiki_remote_publication_verified":bool(wiki_ok),
      "wiki_remote_sha":wiki.get("remote_commit_sha") if wiki_ok else None,
      "original_image_requirements":len(images),
      "original_images_confirmed":len(complete),
      "image_status_counts":dict(sorted(stats.items())),
      "monitored_wiki_source_pages":len(sources),
      "franchise_families":len(franchise),
      "right_to_sell_granted_automatically":False,
      "automatic_private_use_permission":False,
      "readiness":"READY_FOR_HUMAN_WP_REVIEW" if not blockers else "BLOCKED",
      "blockers":blockers
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--require-ready",action="store_true")
    args=p.parse_args()
    summary=build()
    contents=json.dumps(summary,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.check:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8")!=contents:
            print(json.dumps({"result":"FAIL","reason":"Pre-WP state is stale","status":summary},
                             ensure_ascii=False,indent=2))
            return 1
    elif not args.require_ready:
        OUT.write_text(contents,encoding="utf-8")
    print(contents)
    if args.require_ready and summary["readiness"]!="READY_FOR_HUMAN_WP_REVIEW":
        return 2
    return 0

if __name__=="__main__":
    raise SystemExit(main())
