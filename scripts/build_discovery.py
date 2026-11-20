#!/usr/bin/env python3
"""Deterministic, dependency-free Barnskoj discovery graph compiler.

Inputs: canonical entity registry + claim/source evidence + creative motif briefs
and existing decade collections. Outputs are derived, never edited by hand.
No external requests and no factual inference from tags or creative concepts.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery"
THEME_FOR_MEDIUM = {
    "medium:music": "music",
    "medium:sport": "sport",
    "medium:television": "tv",
    "medium:film-tv": "tv",
    "medium:gaming": "gaming",
    "medium:literature": "storytelling",
    "medium:comics": "storytelling",
}
DECADES = [f"era:{y}s" for y in range(1950, 2030, 10)]

def csv_in(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

def json_in(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def csv_out(rows):
    return "\n".join(",".join('"' + str(value if value is not None else "").replace('"', '""') + '"' for value in row)
                     for row in rows) + "\n"

def parts(s):
    return [x for x in (s or "").split(";") if x]

def build():
    entities = csv_in("catalog/entities.csv")
    sources = csv_in("sources/registry.csv")
    claims = csv_in("evidence/claims.csv")
    motifs = json_in("creative/motifs.json")
    themes = json_in("creative/themes.json")
    formats = json_in("creative/formats.json")
    books = csv_in("catalog/decades/collections.csv")
    activities = csv_in("production/activities.csv")
    assets = csv_in("production/assets.csv")
    entity_ids = {x["entity_id"] for x in entities}
    source_ids = {x["source_id"] for x in sources}
    theme_ids = {x["id"] for x in themes}
    format_ids = {x["id"] for x in formats}
    book_ids = {x["collection_id"] for x in books}
    motif_ids = {x["id"] for x in motifs}
    assert len(entity_ids) == len(entities)
    assert len(motif_ids) == len(motifs)
    assert len(book_ids) == len(books)
    assert all(x["rights_basis"] == "original_design_required" and x["stage"] == "concept"
               for x in motifs), "No motif may silently become a licensed asset"
    for x in motifs:
        assert set(x["theme_ids"]) <= theme_ids
        assert set(x["format_ids"]) <= format_ids
        assert x["collection_id"] in book_ids
        assert x["era_id"] in DECADES
    node_rows = [["node_id", "node_type", "name_sv", "stage", "rights_status"]]
    edge_rows = [["from_id", "relation", "to_id", "provenance", "rights_boundary"]]
    cross_rows = [["entity_id", "motif_id", "match_basis", "shared_theme", "shared_era", "stage", "rights_boundary"]]
    search_rows = [["node_id", "name_sv", "node_type", "theme_ids", "era_ids", "research_grade", "format_ids", "collection_id"]]
    edges = set()

    def node(id, typ, name, stage, right="reference_only"):
        node_rows.append([id, typ, name, stage, right])

    def edge(a, relation, b, origin, right="reference_only"):
        edges.add((a, relation, b, origin, right))

    for e in entities:
        id = e["entity_id"]
        node(id, "entity", e["display_name"], e["research_grade"], "HOLD")
        tags = set(parts(e["tag_ids"]))
        t = sorted({THEME_FOR_MEDIUM[x] for x in tags if x in THEME_FOR_MEDIUM})
        eras = sorted(tags & set(DECADES))
        if e["entity_type"] != "universe" and e["universe_id"] != "not_applicable":
            assert e["universe_id"] in entity_ids
            edge(id, "CATALOG_MEMBER_OF", e["universe_id"], "catalog_derived")
        if e["canonical_id"] != id:
            assert e["canonical_id"] in entity_ids
            edge(id, "IDENTITY_ALIAS_OF", e["canonical_id"], "identity_registry")
        for theme in t:
            edge(id, "CATALOG_TOPIC", "theme:" + theme, "tag_derived_unverified")
        for era in eras:
            edge(id, "CATALOG_ERA_ASSOCIATION", era, "tag_derived_unverified")
        search_rows.append([id, e["display_name"], "entity", ";".join(t), ";".join(eras),
                            e["research_grade"], "", ""])

    for x in sources:
        node(x["source_id"], "source", x["title"], "research_reference")
    for x in claims:
        assert x["entity_id"] in entity_ids and x["source_id"] in source_ids
        node(x["claim_id"], "claim", x["claim_sv"], x["review_status"])
        edge(x["claim_id"], "CLAIM_ABOUT", x["entity_id"], "specific_evidence")
        edge(x["claim_id"], "CLAIM_SUPPORTED_BY", x["source_id"], "specific_evidence")

    for x in themes:
        node("theme:" + x["id"], "theme", x["label_sv"], "controlled_vocabulary")
    for x in formats:
        node("format:" + x["id"], "activity_format", x["label_sv"], "format_definition")
    for era in DECADES:
        node(era, "decade", era.split(":")[1], "index_only")
    for book in books:
        b = book["collection_id"]
        node(b, "book_collection", book["title"], book["status"], "not_produced")
        dec = "era:" + book["decade_start"] + "s"
        assert dec in DECADES
        edge(b, "CURATES_DECADE", dec, "editorial_plan", "no_image_rights")
        search_rows.append([b, book["title"], "book_collection", "", dec, "",
                            book["formats"], b])

    for motif in motifs:
        m = motif["id"]
        node(m, "original_motif_concept", motif["title_sv"], "concept", "not_created")
        edge(motif["collection_id"], "CONCEPT_FOR_COLLECTION", m, "editorial_plan", "no_image_rights")
        edge(m, "DESIGNED_FOR_ERA", motif["era_id"], "creative_brief", "original_design_required")
        for t in motif["theme_ids"]:
            edge(m, "EXPLORES_THEME", "theme:" + t, "creative_brief", "original_design_required")
        for f in motif["format_ids"]:
            edge(m, "FORMAT_CANDIDATE", "format:" + f, "creative_brief", "no_print_asset")
        search_rows.append([m, motif["title_sv"], "original_motif_concept",
                            ";".join(motif["theme_ids"]), motif["era_id"], "",
                            ";".join(motif["format_ids"]), motif["collection_id"]])

    # Actual production activity and registered vector assets are separate from ideas.
    motifs_by_id = {m["id"]: m for m in motifs}
    assets_by_id = {a["asset_id"]: a for a in assets}
    for a in activities:
        activity_id = a["activity_id"]
        motif = motifs_by_id[a["motif_id"]]
        title = motif["title_sv"] + " – prick till prick"
        node(activity_id, "activity_prototype", title, a["status"], "REVIEW_PENDING")
        edge(activity_id, "USES_MOTIF", motif["id"], "production_manifest",
             "original_prototype_not_published")
        edge(activity_id, "USES_FORMAT", "format:" + a["format_id"], "production_manifest",
             "original_prototype_not_published")
        for asset_id in [a["asset_id"], a["solution_asset_id"]]:
            if asset_id:
                registered_asset = assets_by_id[asset_id]
                node(asset_id, "asset", registered_asset["asset_kind"] + " / " + activity_id,
                     "registered_not_published", registered_asset["rights_status"])
                edge(activity_id, "HAS_ASSET", asset_id, "production_manifest",
                     "not_rights_cleared")
        search_rows.append([activity_id, title, "activity_prototype",
                            ";".join(motif["theme_ids"]), motif["era_id"], "",
                            a["format_id"], motif["collection_id"]])

    motif_sorted = sorted(motifs, key=lambda m: m["id"])
    for e in entities:
        e_id = e["entity_id"]
        tags = set(parts(e["tag_ids"]))
        ts = {THEME_FOR_MEDIUM[x] for x in tags if x in THEME_FOR_MEDIUM}
        era = tags & set(DECADES)
        possible = []
        for m in motif_sorted:
            shared_t = sorted(ts & set(m["theme_ids"]))
            if not shared_t:
                continue
            same_era = m["era_id"] in era
            score = (2 if same_era else 0) + 1
            possible.append((-score, m["id"], shared_t[0],
                             m["era_id"] if same_era else "", "shared_topic_and_era" if same_era else "shared_topic_only"))
        for _score, motif_id, theme, same_era, basis in sorted(possible)[:2]:
            cross_rows.append([e_id, motif_id, basis, theme, same_era,
                               "editorial_candidate", "original_object_only_no_character_or_portrait_copy"])
            edge(e_id, "EDITORIAL_DISCOVERY_CANDIDATE", motif_id, basis,
                 "original_object_only_no_character_or_portrait_copy")

    nodes = node_rows[:1] + sorted(node_rows[1:], key=lambda row: row[0])
    edges_data = edge_rows[:1] + [list(r) for r in sorted(edges)]
    cross = cross_rows[:1] + sorted(cross_rows[1:], key=lambda r: (r[0], r[1]))
    search = search_rows[:1] + sorted(search_rows[1:], key=lambda r: r[0])
    out = {"discovery/nodes.csv": csv_out(nodes),
           "discovery/edges.csv": csv_out(edges_data),
           "discovery/crosslinks.csv": csv_out(cross),
           "discovery/search.csv": csv_out(search)}
    counts = Counter(e["research_grade"].split("_")[0] for e in entities)
    # Data-derived release metrics. Never infer produced assets from a concept brief.
    asset_ids = {x["asset_id"] for x in assets}
    published_activities = [x for x in activities if x["status"] == "published"]
    for x in published_activities:
        assert x["asset_id"] in asset_ids, "Published activity without tracked asset"
    anchor = json_in(".cdx/anchor.json")
    state = anchor["binding_state"] + ("_NOT_CENTRALLY_VERIFIED"
              if anchor["verification"]["verification_state"] == "NOT_VERIFIED" else "_EXPLICIT_VERIFICATION_RECORDED")
    metrics = {
        "entities": len(entities), "source_refs": len(sources), "atomic_claims": len(claims),
        "original_motif_concepts": len(motifs), "collections_planned": len(books),
        "themes": len(themes), "formats": len(formats), "nodes": len(nodes) - 1,
        "graph_edges": len(edges_data) - 1, "editorial_crosslinks": len(cross) - 1,
        "research_grades": dict(sorted(counts.items())),
        "print_assets_published": len(published_activities),
        "activity_prototypes": sum(x["status"] == "prototype" for x in activities),
        "assets_registered": len(assets),
        "cdx_standing": state
    }
    out["discovery/metrics.json"] = json.dumps(metrics, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    return out, metrics

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="Fail on stale or absent generated outputs")
    args = p.parse_args()
    files, metrics = build()
    stale = []
    for name, content in files.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(json.dumps({"result": "STALE" if stale else "PASS", "stale_files": stale,
                      "mode": "check" if args.check else "build", "metrics": metrics},
                     indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if stale else 0

if __name__ == "__main__":
    sys.exit(main())
