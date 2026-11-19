#!/usr/bin/env python3
"""Barnskoj catalogue structural QA. Stdlib only; no external network calls.

Provenance/rights QA remain human duties. This script validates machine-checkable
cross-references and rejects broken registry integrity, not historically false claims.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
WARNINGS = []

def load(rel):
    path = ROOT / rel
    if not path.is_file():
        ERRORS.append(f"Missing catalogue {rel}")
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(not name for name in reader.fieldnames):
            ERRORS.append(f"CSV header broken: {rel}")
            return []
        rows = list(reader)
    for i, row in enumerate(rows, 2):
        if None in row or any(v is None for v in row.values()):
            ERRORS.append(f"Column mismatch: {rel}:{i}")
    return rows

def ids(rows, field, label):
    vals = [r.get(field, "") for r in rows]
    if any(not v for v in vals):
        ERRORS.append(f"Blank {field} in {label}")
    for value, amount in Counter(vals).items():
        if amount > 1:
            ERRORS.append(f"Duplicate {label} identifier: {value} ({amount})")
    return set(vals)

def subset(value):
    return set(filter(None, (value or "").split(";")))

def main():
    char = load("catalog/characters.csv")
    people = load("catalog/celebrities.csv")
    worlds = load("catalog/universes.csv")
    src = load("sources/registry.csv")
    tags = load("tags/taxonomy.csv")
    assigned = load("tags/assignments.csv")
    identities = load("catalog/identity_registry.csv")
    aliases = load("catalog/aliases.csv")
    qa = load("quality/entity_quality.csv")
    claims = load("evidence/claims.csv")
    checks = load("evidence/source_checks.csv")
    all_rows = char + people
    eid = ids(all_rows, "id", "entity")
    wid = ids(worlds, "world_id", "world")
    sid = ids(src, "source_id", "source")
    tid = ids(tags, "tag_id", "tag")
    ids(claims, "claim_id", "claim")
    ids(identities, "entity_id", "identity")
    ids(qa, "entity_id", "QA")
    ids(aliases, "alias_id", "alias")
    if {r["entity_id"] for r in qa} != eid:
        ERRORS.append("QA does not cover exactly all entities")
    if {r["entity_id"] for r in identities} != eid:
        ERRORS.append("Identity registry does not cover exactly all entities")
    worlds_by_id = {r["world_id"]: r for r in worlds}
    src_by_id = {r["source_id"]: r for r in src}
    qa_by_id = {r["entity_id"]: r for r in qa}
    assigned_by_entity = defaultdict(set)
    pairs = set()
    for r in assigned:
        item = (r["entity_id"], r["tag_id"])
        if item in pairs:
            ERRORS.append(f"Duplicate tag assignment: {item}")
        pairs.add(item)
        assigned_by_entity[r["entity_id"]].add(r["tag_id"])
        if r["entity_id"] not in eid:
            ERRORS.append(f"Assignment references missing entity: {r['entity_id']}")
        if r["tag_id"] not in tid:
            ERRORS.append(f"Assignment references missing tag: {r['tag_id']}")
    claim_by_entity = defaultdict(list)
    for r in claims:
        e, s = r["entity_id"], r["source_id"]
        if e not in eid | wid:
            ERRORS.append(f"Unknown claim entity: {e}")
        if s not in sid:
            ERRORS.append(f"Unknown claim source: {s}")
        elif r["source_url"] != src_by_id[s]["url"]:
            ERRORS.append(f"Claim source_url does not match registry: {r['claim_id']}")
        if not r["claim_sv"].strip() or not r["source_locator"].strip():
            ERRORS.append(f"Incomplete evidence item: {r['claim_id']}")
        claim_by_entity[e].append(r)
    for r in all_rows:
        e = r["id"]
        for key in ("profile_path", "source_dossier_path"):
            rel = r.get(key, "")
            if not rel or not (ROOT / rel).is_file():
                ERRORS.append(f"Missing {key} for {e}: {rel}")
        sources = subset(r.get("source_ids"))
        for s in sources:
            if s not in sid:
                ERRORS.append(f"{e}: unknown source ID {s}")
        assigned_tags = assigned_by_entity.get(e, set())
        exported_tags = subset(r.get("tag_ids"))
        if assigned_tags != exported_tags:
            ERRORS.append(f"{e}: tag index differs from assignment table")
        if not assigned_tags:
            ERRORS.append(f"{e}: no tags")
        if r.get("canonical_entity_id") not in eid:
            ERRORS.append(f"{e}: missing canonical entity")
        q = qa_by_id.get(e)
        if q:
            if int(q["source_count"]) != len(sources):
                ERRORS.append(f"{e}: QA source_count mismatch")
            if int(q["checked_claim_count"]) != len(claim_by_entity[e]):
                ERRORS.append(f"{e}: QA checked_claim_count mismatch")
            grade = ("Q2_partial_claim_verified" if claim_by_entity[e]
                     else "Q1_source_leads" if sources else "Q0_no_source")
            if q["research_grade"] != grade:
                ERRORS.append(f"{e}: QA research grade mismatched")
        if e.startswith("BS-CHAR") and r.get("universe_id") not in wid:
            ERRORS.append(f"{e}: unknown world")
    for w in worlds:
        if not (ROOT / w["profile_path"]).is_file():
            ERRORS.append(f"Universe profile missing {w['world_id']}")
        members = [x for x in char if x["universe_id"] == w["world_id"]]
        if w["entity_count"] != str(len(members)):
            ERRORS.append(f"Universe member count mismatch: {w['world_id']}")
        if not members:
            WARNINGS.append(f"Empty universe: {w['world_id']}")
    for r in checks:
        if r["source_id"] not in sid:
            ERRORS.append(f"Unknown source check ID: {r['source_id']}")
        elif r["url"] != src_by_id[r["source_id"]]["url"]:
            ERRORS.append(f"Source-check URL mismatch: {r['source_id']}")
    for r in aliases:
        if r["entity_id"] not in eid or r["canonical_entity_id"] not in eid:
            ERRORS.append(f"Broken alias: {r['alias_id']}")
    for r in identities:
        entity = next((x for x in all_rows if x["id"] == r["entity_id"]), None)
        if entity and entity["canonical_entity_id"] != r["canonical_entity_id"]:
            ERRORS.append(f"Identity catalogue mismatch {r['entity_id']}")
    if len({r["url"] for r in src}) != len(src):
        WARNINGS.append("Identical source URLs appear under multiple IDs")
    flagged_no_source = sum(not subset(r.get("source_ids")) for r in all_rows)
    if flagged_no_source:
        WARNINGS.append(f"{flagged_no_source} entities remain without sources (research debt)")
    reported = {
        "entities": len(all_rows), "characters": len(char),
        "people": len(people), "universes": len(worlds),
        "sources": len(src), "tags": len(tags),
        "tag_assignments": len(assigned), "claims": len(claims),
        "source_checks": len(checks), "errors": ERRORS,
        "warnings": WARNINGS, "result": "FAIL" if ERRORS else "PASS"
    }
    print(json.dumps(reported, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0

if __name__ == "__main__":
    sys.exit(main())
