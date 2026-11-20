#!/usr/bin/env python3
"""HARP-style source model integrity check; no factual or legal auto-approval."""
import csv
import json
import pathlib
import urllib.parse
from collections import Counter

ROOT=pathlib.Path(__file__).resolve().parents[1]
errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

def read(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def unique(rows,key,what):
    ids=[r[key] for r in rows]
    check(len(ids)==len(set(ids)) and all(ids),"Duplicate/blank "+what)
    return set(ids)

def main():
    entities=read("catalog/entities.csv")
    motifs=json.loads((ROOT/"creative/motifs.json").read_text(encoding="utf-8"))
    franchises=read("sourcing/franchises.csv")
    sources=read("sourcing/wiki_sources.csv")
    staged=read("sourcing/staged_entities.csv")
    links=read("sourcing/entity_source_links.csv")
    images=read("images/requirements.csv")
    staged_images=read("images/staged_requirements.csv")
    ledger=read("rights/ledger.csv")
    decisions=read("rights/decisions.csv")
    source_state=json.loads((ROOT/"sourcing/watch-state.json").read_text(encoding="utf-8"))
    backlog=read("sourcing/change-backlog.csv")
    franchise_ids=unique(franchises,"franchise_id","franchise")
    source_ids=unique(sources,"source_id","wiki source")
    entity_ids=unique(entities,"entity_id","canonical entity")
    stage_ids=unique(staged,"candidate_id","staged candidate")
    motif_ids=unique(motifs,"id","motif")
    image_ids=unique(images,"target_id","image requirement")
    stage_image_ids=unique(staged_images,"target_id","staged image requirement")
    rights_ids=unique(ledger,"target_id","rights decision target")
    check(stage_ids.isdisjoint(entity_ids),"Staged candidate appears as canonical without promotion")
    check(image_ids==entity_ids|motif_ids,"Each canonical entity and motif requires one image source record")
    check(stage_image_ids==stage_ids,"Every staged continuity must have an image need")
    check(rights_ids==image_ids|stage_image_ids,"Copyright ledger does not cover full image backlog")
    frmap={f["franchise_id"]:f for f in franchises}
    smap={s["source_id"]:s for s in sources}
    cmap={e["entity_id"]:e for e in entities}
    for f in franchises:
        w=f["existing_world_id"]
        check(w=="STAGED" or w in cmap,"Franchise linked to unknown world "+f["franchise_id"])
    for s in sources:
        url=urllib.parse.urlparse(s["page_url"])
        check(url.scheme=="https" and bool(url.hostname),"Source must be HTTPS "+s["source_id"])
        check(s["franchise_id"] in franchise_ids,"Source missing franchise "+s["source_id"])
        check(s["watch_mode"] in {"mediawiki","http_headers","manual"},
              "Unknown watch mode "+s["source_id"])
        if s["watch_mode"]=="mediawiki":
            check(bool(s["page_title"]),"MediaWiki source has no article name "+s["source_id"])
        if s["source_kind"]=="fan_wiki":
            check(s["authority"]=="secondary_unverified","Fan wiki not secondary "+s["source_id"])
            check(s["content_license"]=="fandom_text_cc_by_sa_3",
                  "Fan wiki text licence must not be promoted "+s["source_id"])
            check(s["media_rights"]=="image_file_specific",
                  "Fan wiki images cannot inherit text licence "+s["source_id"])
        if s["source_kind"]=="rights_holder":
            check(s["content_license"]=="proprietary","Owner site mislicensed "+s["source_id"])
    for c in staged:
        check(c["franchise_id"] in franchise_ids,"Staged entity missing franchise "+c["candidate_id"])
        for field in ("fan_source_id","official_source_id"):
            sid=c[field]
            if sid:
                check(sid in source_ids,"Candidate missing source "+c["candidate_id"]+"/"+sid)
                if sid in smap:
                    check(smap[sid]["franchise_id"]==c["franchise_id"],
                          "Staged source belongs to other franchise "+c["candidate_id"])
        check(c["registration_status"]=="STAGED_NOT_CANONICAL",
              "Candidate falsely promoted "+c["candidate_id"])
    for l in links:
        check(l["entity_id"] in entity_ids and l["source_id"] in source_ids
              and l["franchise_id"] in franchise_ids,
              "Broken canonical-to-wiki link "+l["entity_id"])
    for r in images+staged_images:
        status=r["image_status"]
        check(status in {"MISSING","SOURCE_CANDIDATE","SOURCE_CONFIRMED",
                          "RIGHTS_REVIEWED","APPROVED_FOR_DESIGN"},
              "Unexpected image state "+r["target_id"])
        if status!="MISSING":
            check(bool(r["image_page_url"]),"Image claimed but has no object URL "+r["target_id"])
        if status in {"SOURCE_CONFIRMED","RIGHTS_REVIEWED","APPROVED_FOR_DESIGN"}:
            check(r["identity_confirmation"]=="CONFIRMED"
                  and r["source_examination"]=="VERIFIED"
                  and bool(r["creator"]) and bool(r["source_archive_reference"]),
                  "Original provenance incomplete "+r["target_id"])
        if status=="APPROVED_FOR_DESIGN":
            check(r["rights_review"]=="APPROVED" and bool(r["license_url"]),
                  "Image published without licence review "+r["target_id"])
    for r in ledger:
        check(r["current_approval"]=="HOLD" and r["public_repo_asset_allowed"]=="NO",
              "Unverified right auto-granted "+r["target_id"])
        check(r["commercial_release_route"] in
              {"BLOCKED_UNLESS_RIGHTS_GRANTED","ORIGINAL_DESIGN_AND_IP_REVIEW_REQUIRED"},
              "Commercial gate malformed "+r["target_id"])
        check(r["private_use_route"]=="CASE_BY_CASE_SWEDISH_EXCEPTION_NOT_PUBLICATION",
              "Private use improperly granted "+r["target_id"])
    for d in decisions:
        check(bool(d.get("reviewer")) and bool(d.get("licence_or_agreement_url"))
              and bool(d.get("target_id")) and bool(d.get("decision_timestamp")),
              "Legal decision lacks human reviewer or recorded licence")
    check(source_state.get("schema")=="barnskoj.sourcewatch/v1","Unexpected watch state schema")
    for sid in source_state.get("sources",{}):
        check(sid in source_ids,"Unknown observed source in monitor")
    for x in backlog:
        check(x["source_id"] in source_ids and x["status"]=="REVIEW_REQUIRED",
              "Automatic source change was inappropriately approved")
    stats={"result":"PASS" if not errors else "FAIL",
           "canonical_entities":len(entities),"staged_candidates":len(staged),
           "image_targets":len(images)+len(staged_images),
           "wiki_source_pages":len(sources),"franchises":len(franchises),
           "legal_approvals":len(decisions),
           "image_statuses":dict(sorted(Counter(r["image_status"] for r in images+staged_images).items())),
           "errors":errors[:50]}
    print(json.dumps(stats,indent=2,ensure_ascii=False))
    return int(bool(errors))

if __name__=="__main__":
    raise SystemExit(main())
