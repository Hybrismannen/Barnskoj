#!/usr/bin/env python3
"""Derive rights decision ledger from cultural entities, image needs and staged wiki candidates.

Does NOT grant any licence. Pure local transformation; no network calls.
"""
import argparse
import csv
import io
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
COLUMNS=[
 "target_id","title","target_type","franchise_id","continuity",
 "image_status","source_image_page","source_owner_candidate","underlying_ip",
 "wiki_text_reuse","image_license_status","derivative_design_status",
 "private_use_route","commercial_release_route","public_repo_asset_allowed",
 "required_evidence","current_approval"
]

def load(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def csv_out(rows):
    out=io.StringIO(newline="")
    writer=csv.DictWriter(out,fieldnames=COLUMNS,quoting=csv.QUOTE_ALL,lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return out.getvalue()

def build():
    entities=load("catalog/entities.csv")
    images=load("images/requirements.csv")
    motifs=json.loads((ROOT/"creative/motifs.json").read_text(encoding="utf-8"))
    staged=load("sourcing/staged_entities.csv")
    franchises=load("sourcing/franchises.csv")
    links=load("sourcing/entity_source_links.csv")
    by_image={r["target_id"]:r for r in images}
    by_franchise={f["franchise_id"]:f for f in franchises}
    by_world={f["existing_world_id"]:f for f in franchises if f["existing_world_id"]!="STAGED"}
    by_entity={r["entity_id"]:r["franchise_id"] for r in links}
    rows=[]
    def base(target_id,title,target_type,franchise_id,continuity,image_info,underlying_ip):
        fr=by_franchise.get(franchise_id)
        owner=fr["possible_owner_contact"] if fr else "OWNER_UNDETERMINED"
        original=(target_type=="original_motif")
        return {
          "target_id":target_id,"title":title,"target_type":target_type,
          "franchise_id":franchise_id or "UNMAPPED",
          "continuity":continuity or "UNRESOLVED",
          "image_status":image_info.get("image_status","MISSING"),
          "source_image_page":image_info.get("image_page_url",""),
          "source_owner_candidate":owner,
          "underlying_ip":"generic_original_concept" if original else underlying_ip,
          "wiki_text_reuse":"FANDOM_CC_BY_SA_3_TEXT_ONLY_IF_APPLICABLE",
          "image_license_status":"NOT_VERIFIED",
          "derivative_design_status":"ORIGINAL_ONLY_UNTIL_PERMISSION" if original else "REQUIRES_CASE_REVIEW",
          "private_use_route":"CASE_BY_CASE_SWEDISH_EXCEPTION_NOT_PUBLICATION",
          "commercial_release_route":"ORIGINAL_DESIGN_AND_IP_REVIEW_REQUIRED" if original else "BLOCKED_UNLESS_RIGHTS_GRANTED",
          "public_repo_asset_allowed":"NO",
          "required_evidence":"per-file image licence; underlying character IP; adaptation right; portrait/branding; commercial territory; author credit",
          "current_approval":"HOLD"
        }
    for e in entities:
        id=e["entity_id"]
        im=by_image.get(id)
        if im is None:
            raise ValueError("Missing image need "+id)
        franchise=by_entity.get(id)
        if not franchise and e["entity_type"]=="universe":
            franchise=by_world.get(id,{}).get("franchise_id")
        if not franchise:
            franchise=by_world.get(e["universe_id"],{}).get("franchise_id")
        underlying=("character_or_person_rights_require_review" if e["entity_type"]!="universe"
                    else "franchise_rights_require_review")
        rows.append(base(id,e["display_name"],e["entity_type"],franchise or "",
                         e["universe_id"] if e["universe_id"]!="not_applicable" else "not_applicable",im,underlying))
    for m in motifs:
        id=m["id"]
        im=by_image.get(id)
        if im is None:
            raise ValueError("Missing motif image need "+id)
        rows.append(base(id,m["title_sv"],"original_motif","","unaffiliated",im,
                         "generic_original_concept"))
    for e in staged:
        rows.append(base(e["candidate_id"],e["display_name"],"staged_character",
                         e["franchise_id"],e["continuity"],{},
                         e["rights_subject"]))
    if len(rows)!=(len(entities)+len(motifs)+len(staged)):
        raise ValueError("Rights coverage mismatch")
    if len(set(r["target_id"] for r in rows))!=len(rows):
        raise ValueError("Duplicate rights targets")
    metrics={
     "total_targets":len(rows),"existing_entities":len(entities),
     "original_motifs":len(motifs),"staged_candidates":len(staged),
     "rights_granted":sum(r["current_approval"]=="APPROVED" for r in rows),
     "rights_on_hold":sum(r["current_approval"]=="HOLD" for r in rows),
     "commercial_ready":0,
     "private_use_automatic_permission":0
    }
    return {"rights/ledger.csv":csv_out(rows),
            "rights/metrics.json":json.dumps(metrics,ensure_ascii=False,sort_keys=True,indent=2)+"\n"},metrics

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    opts=p.parse_args()
    data,metrics=build()
    stale=[]
    for name,content in data.items():
        f=ROOT/name
        if opts.check:
            if not f.is_file() or f.read_text(encoding="utf-8")!=content:
                stale.append(name)
        else:
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text(content,encoding="utf-8")
    print(json.dumps({"status":"FAIL" if stale else "PASS","stale":stale,"metrics":metrics},
                     ensure_ascii=False,indent=2))
    return 1 if stale else 0

if __name__=="__main__":
    raise SystemExit(main())
