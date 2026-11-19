#!/usr/bin/env python3
"""Barnskoj v2 parity: consistent entity metadata, tags and provenance for all 485 objects."""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "display_name", "entity_type", "canonical_id", "universe_id", "primary_medium",
    "genre_bucket", "era_association", "cultural_context",
    "first_appearance_year", "documented_swedish_broadcast_year",
    "credited_creator", "origin_country", "intended_audience",
    "activity_format", "rights_status", "publication_status", "research_grade"
)
FACETS = (
    "entity_type", "medium", "cultural_context", "cultural_era",
    "universe", "curation_bucket", "audience", "activity_format",
    "source_quality", "rights", "publication", "geographic_origin",
    "identity", "language_variant"
)
ALLOWED = {"catalog_derived", "unknown", "claim_verified", "not_applicable",
           "not_assigned", "policy_state", "computed_from_registry"}
errors = []
warnings = []

def check(condition, message):
    if not condition:
        errors.append(message)

def csvrows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        check(bool(reader.fieldnames) and all(reader.fieldnames), "Missing CSV header: " + path)
        out = list(reader)
    for n, r in enumerate(out, 2):
        check(None not in r and all(v is not None for v in r.values()),
              f"Malformed CSV {path}:{n}")
    return out

def parts(s):
    return [v for v in (s or "").split(";") if v]

def unique(rows, key, description):
    result = {}
    for r in rows:
        identifier = r[key]
        check(identifier not in result, f"Repeated {description}: {identifier}")
        result[identifier] = r
    return result

def run():
    entities = csvrows("catalog/entities.csv")
    characters = csvrows("catalog/characters.csv")
    people = csvrows("catalog/celebrities.csv")
    worlds = csvrows("catalog/universes.csv")
    taxonomy = csvrows("tags/taxonomy.csv")
    assignments = csvrows("tags/assignments.csv")
    attributes = csvrows("evidence/attribute_evidence.csv")
    source_rows = csvrows("sources/registry.csv")
    claim_rows = csvrows("evidence/claims.csv")
    parity = csvrows("quality/entity_parity.csv")
    quality_old = csvrows("quality/entity_quality.csv")

    en = unique(entities, "entity_id", "entity")
    worlds_by_id = unique(worlds, "world_id", "world")
    sources = unique(source_rows, "source_id", "source")
    claims = unique(claim_rows, "claim_id", "claim")
    tags = unique(taxonomy, "tag_id", "tag")
    parity_by_id = unique(parity, "entity_id", "parity")
    legacy_quality = unique(quality_old, "entity_id", "legacy quality")

    expected = {r["id"] for r in characters + people} | set(worlds_by_id)
    check(len(entities) == 485, f"Expected 485 entity records, got {len(entities)}")
    check(set(en) == expected, "Canonical registry not equal to character/person/world union")
    check(set(parity_by_id) == set(en), "Paritetsmatris incomplete")
    check(set(legacy_quality) == {r["id"] for r in characters + people},
          "Old QA must cover character/person registers")

    assignments_for = defaultdict(set)
    for r in assignments:
        eid, tid = r["entity_id"], r["tag_id"]
        check(eid in en and tid in tags, f"Unknown assignment {eid}/{tid}")
        check(tid not in assignments_for[eid], f"Duplicate assignment {eid}/{tid}")
        assignments_for[eid].add(tid)

    attr_map = defaultdict(dict)
    for a in attributes:
        eid, key = a["entity_id"], a["attribute"]
        check(eid in en, f"Unknown attribute owner {eid}")
        check(key in FIELDS, f"Unexpected field {eid}/{key}")
        check(key not in attr_map[eid], f"Duplicate field {eid}/{key}")
        attr_map[eid][key] = a
        status = a["evidence_status"]
        check(status in ALLOWED, f"Invalid evidence status {eid}/{key}: {status}")
        if status == "claim_verified":
            links = parts(a["claim_ids"])
            ref_ids = parts(a["source_ids"])
            check(bool(links) and bool(ref_ids), f"Verified without linked evidence {eid}/{key}")
            for claim_id in links:
                cl = claims.get(claim_id)
                check(cl is not None, f"Unknown claim {claim_id}")
                if cl:
                    check(cl["entity_id"] == eid, f"Misattributed claim {eid}/{claim_id}")
                    check(cl["source_id"] in ref_ids, f"Wrong source {eid}/{claim_id}")
                    check(a["value"] in cl["claim_sv"], f"Unsubstantiated field value {eid}/{key}")
            for sid in ref_ids:
                check(sid in sources, f"Unknown attribute source {eid}/{sid}")
        else:
            check(not parts(a["claim_ids"]) and not parts(a["source_ids"]),
                  f"Unverified field has faux evidence {eid}/{key}")
        if status == "unknown":
            check(a["value"] == "unknown", f"Unknown value improperly populated {eid}/{key}")
        if status == "not_assigned":
            check(a["value"] == "unassigned", f"Unassigned value not explicit {eid}/{key}")

    grades = Counter()
    for eid, r in en.items():
        check(set(attr_map[eid]) == set(FIELDS), f"Attribute parity failure {eid}")
        for field in FIELDS:
            if field in attr_map[eid]:
                check(attr_map[eid][field]["value"] == r[field], f"Attribute diverges from master {eid}/{field}")
        ids = set(parts(r["tag_ids"]))
        check(ids == assignments_for[eid], f"Tag export/assignment mismatch {eid}")
        check(all(t in tags for t in ids), f"Undefined tags {eid}")
        fs = {tags[t]["facet"] for t in ids if t in tags}
        check(all(f in fs for f in FACETS), f"Missing required facet {eid}: {set(FACETS) - fs}")
        check(r["canonical_id"] in en, f"Broken canonical identity {eid}")
        if r["entity_type"] == "universe":
            check(r["universe_id"] == eid, f"World self-reference inconsistent {eid}")
        elif eid.startswith("BS-CHAR"):
            check(r["universe_id"] in worlds_by_id, f"Broken universe {eid}")
        elif eid.startswith("BS-PER"):
            check(r["universe_id"] == "not_applicable", f"Person universe must be not_applicable {eid}")
        else:
            check(False, f"Unknown entity family {eid}")

        for field in ("profile_path", "source_dossier_path", "baseline_record_path"):
            path = r[field]
            check(bool(path) and (ROOT / path).is_file(), f"Missing linked file {eid}/{field}: {path}")
        check(r["rights_status"] == "HOLD" and r["publication_status"] == "reference_only",
              f"Unapproved rights/publication gate {eid}")
        sr = parts(r["source_ids"])
        cl = parts(r["claim_ids"])
        for sid in sr:
            check(sid in sources, f"Unknown source reference {eid}/{sid}")
        for cid in cl:
            check(cid in claims and claims[cid]["entity_id"] == eid, f"Invalid claim reference {eid}/{cid}")
        expected_grade = "Q2_partial_claim_verified" if cl else "Q1_source_leads" if sr else "Q0_no_source"
        check(r["research_grade"] == expected_grade, f"Research grade mismatch {eid}")
        grades[expected_grade] += 1
        grade_tag = "evidence:" + expected_grade[:2].lower()
        check(grade_tag in ids, f"Missing research-grade tag {eid}")
        pr = parity_by_id.get(eid)
        if pr:
            check(pr["schema_parity"] == "PASS", f"Parity status false {eid}")
            check(int(pr["required_attributes"]) == len(FIELDS)
                  and int(pr["present_attributes"]) == len(FIELDS), f"Attribute count differs {eid}")
            check(int(pr["required_tag_facets"]) == len(FACETS)
                  and int(pr["present_tag_facets"]) == len(FACETS), f"Facet count differs {eid}")
            check(int(pr["source_count"]) == len(sr) and int(pr["claim_count"]) == len(cl),
                  f"Source count differs {eid}")
        if eid in legacy_quality:
            check(int(legacy_quality[eid]["tag_count"]) == len(ids),
                  f"Legacy QA tag count out of sync {eid}")
        if expected_grade == "Q0_no_source":
            warnings.append(eid + ": missing source research")

    for row in characters + people:
        e = en.get(row["id"])
        if e:
            check(row["baseline_record_path"] == e["baseline_record_path"],
                  f"Broken baseline link {row['id']}")
            check(set(parts(row["tag_ids"])) == set(parts(e["tag_ids"])),
                  f"Local register vs canonical tags differ {row['id']}")
    for w in worlds:
        e = en.get(w["world_id"])
        if e:
            check(w["baseline_record_path"] == e["baseline_record_path"],
                  f"World baseline link broken {w['world_id']}")
            check(set(parts(w["tag_ids"])) == set(parts(e["tag_ids"])),
                  f"World vs canonical tags differ {w['world_id']}")

    output = {"result": "FAIL" if errors else "PASS",
              "entities": len(en), "universes": len(worlds), "fields": len(FIELDS),
              "required_facets": len(FACETS), "attribute_rows": len(attributes),
              "sources": len(sources), "claims": len(claims), "research_grades": dict(grades),
              "research_gaps": len(warnings), "errors": errors[:100]}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(run())
