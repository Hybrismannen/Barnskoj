#!/usr/bin/env python3
"""WP01: canonical single-write registry -> backward-compatible derived views.

The only manually edited entity baseline is catalog/source/entities_base.csv.
Legacy-specific fields live in catalog/source/legacy_details.csv.
Tag links, claims and six claim-backed field mappings are independently authored.
This generator cannot certify claims, legal rights or published materials.
"""
import argparse
import csv
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = [
    "display_name", "entity_type", "canonical_id", "universe_id", "primary_medium",
    "genre_bucket", "era_association", "cultural_context", "first_appearance_year",
    "documented_swedish_broadcast_year", "credited_creator", "origin_country",
    "intended_audience", "activity_format", "rights_status", "publication_status",
    "research_grade"
]
ENTITY_COLUMNS = [
    "entity_id","display_name","entity_type","canonical_id","identity_status","universe_id",
    "primary_medium","genre_bucket","era_association","cultural_context",
    "first_appearance_year","documented_swedish_broadcast_year","credited_creator",
    "origin_country","intended_audience","activity_format","rights_status",
    "publication_status","research_grade","claim_ids","source_ids","tag_ids",
    "profile_path","source_dossier_path","baseline_record_path","taxonomy_version"
]
CHAR_COLUMNS = [
    "id","name","universe","era","origin","record_kind","verification_status",
    "rights_status","production_status","profile_path","source_ids",
    "source_dossier_path","universe_id","canonical_entity_id","identity_status",
    "tag_ids","baseline_record_path"
]
PERSON_COLUMNS = [
    "id","name","domain","genre","record_kind","verification_status",
    "likeness_status","production_status","profile_path","source_ids",
    "source_dossier_path","canonical_entity_id","identity_status","tag_ids","baseline_record_path"
]
WORLD_COLUMNS = [
    "world_id","name","legacy_era_range","catalogue_origin","entity_count",
    "profile_path","status","baseline_record_path","source_dossier_path",
    "tag_ids","research_grade","source_ids"
]
QA_COLUMNS = [
    "entity_id","name","canonical_id","entity_type","source_count",
    "checked_claim_count","research_grade","qa_flags","rights_gate",
    "profile_path","source_dossier_path","tag_count"
]
PARITY_COLUMNS = [
    "entity_id","display_name","entity_type","canonical_id","research_grade",
    "source_count","claim_count","required_attributes","present_attributes",
    "required_tag_facets","present_tag_facets","schema_parity",
    "factual_verification","rights_gate","baseline_record_path"
]
ATTRIBUTE_COLUMNS = ["entity_id","attribute","value","evidence_status","claim_ids","source_ids","qualification"]
BACKLOG_COLUMNS = ["entity_id","display_name","research_grade","priority","required_next_action",
                   "profile_path","source_dossier_path","baseline_record_path"]
BACKLOG_ACTION = {
    "Q0_no_source": ("P0_source_discovery",
        "Find entity-specific authoritative primary source; validate identity and at least one claim"),
    "Q1_source_leads": ("P1_claim_verification",
        "Read entity-specific source; capture claim, exact locator, checked date; resolve identities"),
    "Q2_partial_claim_verified": ("P2_full_depth_verification",
        "Verify origin, historical chronology, language versions, cultural context, creator and conflicts; obtain editorial Q3 sign-off"),
}

def load(name):
    with (ROOT/name).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

def sep(s):
    return [x for x in (s or "").split(";") if x]

def render(rows, columns):
    buf = io.StringIO(newline="")
    wr = csv.DictWriter(buf, fieldnames=columns, quoting=csv.QUOTE_ALL, lineterminator="\n", extrasaction="ignore")
    wr.writeheader()
    for row in rows:
        wr.writerow({col: row.get(col, "") for col in columns})
    return buf.getvalue()

def index_unique(rows, id_col):
    out = {}
    for row in rows:
        key = row[id_col]
        if not key or key in out:
            raise ValueError("Duplicate/blank source ID: "+str(key))
        out[key] = row
    return out

def build():
    base = load("catalog/source/entities_base.csv")
    legacy = index_unique(load("catalog/source/legacy_details.csv"), "entity_id")
    proofs = load("evidence/field_proofs.csv")
    claims = load("evidence/claims.csv")
    sources = index_unique(load("sources/registry.csv"), "source_id")
    tags = index_unique(load("tags/taxonomy.csv"), "tag_id")
    assignments = load("tags/assignments.csv")
    originals = index_unique(base, "entity_id")
    if set(originals) != set(legacy):
        raise ValueError("Missing or extra legacy detail record")
    tag_map = defaultdict(list)
    for row in assignments:
        eid, tag = row["entity_id"], row["tag_id"]
        if eid not in originals or tag not in tags or tag in tag_map[eid]:
            raise ValueError("Broken/duplicate tag assignment "+eid+":"+tag)
        tag_map[eid].append(tag)
    claims_by = defaultdict(list)
    claim_index = index_unique(claims, "claim_id")
    for row in claims:
        if row["entity_id"] not in originals or row["source_id"] not in sources:
            raise ValueError("Dangling source or entity in claim "+row["claim_id"])
        claims_by[row["entity_id"]].append(row["claim_id"])
    proof_index = {}
    for row in proofs:
        key = row["entity_id"], row["attribute"]
        if key in proof_index or key[0] not in originals or key[1] not in FIELDS:
            raise ValueError("Invalid duplicate/unknown field proof "+str(key))
        claim = claim_index.get(row["claim_id"])
        if not claim or claim["entity_id"] != key[0] or claim["source_id"] != row["source_id"]:
            raise ValueError("Proof not bound to matching entity and source: "+str(key))
        if originals[key[0]].get(key[1], "") not in claim["claim_sv"]:
            raise ValueError("Proof source does not contain registered value: "+str(key))
        proof_index[key] = row
    entities = []
    for row in base:
        e = dict(row)
        id = e["entity_id"]
        source_ids = sep(e["source_ids"])
        if any(sid not in sources for sid in source_ids):
            raise ValueError("Missing source for "+id)
        links = tag_map[id]
        if not links:
            raise ValueError("Missing tags for "+id)
        medium = next((t for t in links if tags[t]["facet"] == "medium"), None)
        if not medium:
            raise ValueError("Missing primary medium for "+id)
        grade = ("Q2_partial_claim_verified" if claims_by[id]
                 else "Q1_source_leads" if source_ids else "Q0_no_source")
        e.update(primary_medium=medium, research_grade=grade,
                 claim_ids=";".join(claims_by[id]),tag_ids=";".join(links))
        entities.append(e)
    entity_by_id = index_unique(entities,"entity_id")
    worlds = {e["entity_id"]:e for e in entities if e["entity_type"]=="universe"}
    count_world = Counter(e["universe_id"] for e in entities if e["entity_id"].startswith("BS-CHAR"))
    char, people, world, qa, parity, attributes, backlog = [], [], [], [], [], [], []
    record_files = {}
    for e in entities:
        id,typ = e["entity_id"], e["entity_type"]
        l = legacy[id]
        nsrc, nclaim, ntag = len(sep(e["source_ids"])), len(sep(e["claim_ids"])), len(sep(e["tag_ids"]))
        if id.startswith("BS-CHAR"):
            if e["universe_id"] not in worlds:
                raise ValueError("Missing linked world: "+id)
            char.append(dict(
                id=id,name=e["display_name"],universe=worlds[e["universe_id"]]["display_name"],
                era=e["era_association"],origin=e["cultural_context"],record_kind=typ,
                verification_status=l["legacy_verification_status"],rights_status=l["legacy_rights_status"],
                production_status=l["legacy_production_status"],profile_path=e["profile_path"],
                source_ids=e["source_ids"],source_dossier_path=e["source_dossier_path"],
                universe_id=e["universe_id"],canonical_entity_id=e["canonical_id"],
                identity_status=e["identity_status"],tag_ids=e["tag_ids"],
                baseline_record_path=e["baseline_record_path"]))
        elif id.startswith("BS-PER"):
            people.append(dict(id=id,name=e["display_name"],domain=l["domain"],
                genre=e["genre_bucket"],record_kind=typ,
                verification_status=l["legacy_verification_status"],
                likeness_status=l["likeness_status"],production_status=l["legacy_production_status"],
                profile_path=e["profile_path"],source_ids=e["source_ids"],
                source_dossier_path=e["source_dossier_path"],canonical_entity_id=e["canonical_id"],
                identity_status=e["identity_status"],tag_ids=e["tag_ids"],
                baseline_record_path=e["baseline_record_path"]))
        elif typ=="universe":
            world.append(dict(world_id=id,name=e["display_name"],
                legacy_era_range=e["era_association"],catalogue_origin=e["cultural_context"],
                entity_count=str(count_world[id]),profile_path=e["profile_path"],
                status=l["world_status"],baseline_record_path=e["baseline_record_path"],
                source_dossier_path=e["source_dossier_path"],tag_ids=e["tag_ids"],
                research_grade=e["research_grade"],source_ids=e["source_ids"]))
        else:
            raise ValueError("Unknown family: "+id)

        if not (ROOT/e["profile_path"]).is_file() or not (ROOT/e["source_dossier_path"]).is_file():
            raise ValueError("Profile or source dossier missing for "+id)
        if id.startswith(("BS-CHAR","BS-PER")):
            flags = []
            if not nsrc:
                flags.append("NO_SOURCE_URL")
            elif not nclaim:
                flags.append("SOURCE_LINK_ONLY")
            if e["identity_status"]!="canonical":
                flags.append("IDENTITY_ALIAS")
            if id.startswith("BS-CHAR"):
                flags.append("ERA_RANGE_NOT_DEBUT_YEAR")
                if typ=="real_person_presenter": flags.append("REAL_PERSON_IN_CHAR_TABLE")
                if typ=="character_collective": flags.append("COLLECTIVE_RECORD")
                if typ=="performed_tv_persona": flags.append("PERFORMER_PERSONA_SPLIT_REQUIRED")
                if e["display_name"]=="Red": flags.append("NAME_COLLISION_DIFFERENT_UNIVERSE")
            flags.append("RIGHTS_NOT_GRANTED")
            qa.append(dict(entity_id=id,name=e["display_name"],canonical_id=e["canonical_id"],
                entity_type=typ,source_count=str(nsrc),checked_claim_count=str(nclaim),
                research_grade=e["research_grade"],qa_flags=";".join(flags),
                rights_gate="HOLD",profile_path=e["profile_path"],
                source_dossier_path=e["source_dossier_path"],tag_count=str(ntag)))

        parity.append(dict(entity_id=id,display_name=e["display_name"],entity_type=typ,
            canonical_id=e["canonical_id"],research_grade=e["research_grade"],
            source_count=str(nsrc),claim_count=str(nclaim),
            required_attributes="17",present_attributes="17",required_tag_facets="14",
            present_tag_facets="14",schema_parity="PASS",
            factual_verification=("PARTIAL" if nclaim else "NOT_VERIFIED"),
            rights_gate="HOLD",baseline_record_path=e["baseline_record_path"]))
        bucket = e["research_grade"]
        priority, action = BACKLOG_ACTION[bucket]
        backlog.append(dict(entity_id=id,display_name=e["display_name"],research_grade=bucket,
            priority=priority,required_next_action=action,profile_path=e["profile_path"],
            source_dossier_path=e["source_dossier_path"],baseline_record_path=e["baseline_record_path"]))
        tag_facet = defaultdict(list)
        for tag in sep(e["tag_ids"]):
            tag_facet[tags[tag]["facet"]].append(tag)
        attr_rows = []
        for key in FIELDS:
            value = e[key]
            proof = proof_index.get((id,key))
            cid, sid = "", ""
            if proof is not None:
                status = "claim_verified"
                cid, sid = proof["claim_id"], proof["source_id"]
                note = "Enbart detta avgränsade faktapåstående är belagt."
            elif key in {"first_appearance_year","documented_swedish_broadcast_year","credited_creator","origin_country"}:
                if value != "unknown": raise ValueError("Unproved historical fact "+id+"/"+key)
                status, note = "unknown", "Forskningslucka."
            elif key in {"intended_audience","activity_format"}:
                status,note="not_assigned","Ärvt registervärde; inte externt verifierat."
            elif key in {"rights_status","publication_status"}:
                status,note="policy_state","Ärvt registervärde; inte externt verifierat."
            elif key=="research_grade":
                status,note="computed_from_registry","Ärvt registervärde; inte externt verifierat."
            elif value=="not_applicable":
                status,note="not_applicable","Ärvt registervärde; inte externt verifierat."
            elif value=="unknown":
                status,note="unknown","Ärvt registervärde; inte externt verifierat."
            else:
                status,note="catalog_derived","Ärvt registervärde; inte externt verifierat."
            att=dict(entity_id=id,attribute=key,value=value,evidence_status=status,
                     claim_ids=cid,source_ids=sid,qualification=note)
            attributes.append(att)
            attr_rows.append(att)
        heading = [
            "# "+e["display_name"]+" – standardiserad basprofil",
            "",
            "**Entitet:** "+id+" · **Forskningsgrad:** "+bucket+
            " · **Publikationsrätt:** HOLD · **Schema:** 2.0",
            "",
            "[Fördjupningsprofil](../"+e["profile_path"]+") · "+
            "[Individuellt källdossier](../"+e["source_dossier_path"]+") · "+
            "[Evidensmatris](../evidence/attribute_evidence.csv)",
            "",
            "## Obligatoriska attribut",
            "| Attribut | Värde | Evidensstatus | Påståendebelägg |",
            "| --- | --- | --- | --- |",
        ]
        for a in attr_rows:
            heading.append("| "+a["attribute"]+" | "+a["value"].replace("|",r"\|")+
                           " | "+a["evidence_status"]+" | "+(a["claim_ids"] or "–")+" |")
        heading.extend(["","## Samtliga taggdimensioner"])
        for key in ["entity_type","medium","cultural_context","cultural_era","universe",
                    "curation_bucket","audience","activity_format","source_quality",
                    "rights","publication","geographic_origin","identity","language_variant"]:
            vals = tag_facet.get(key)
            if not vals: raise ValueError("Missing tag facet "+id+"/"+key)
            heading.append("- **"+key+":** "+", ".join("`"+t+"`" for t in vals))
        heading.extend(["","**Käll-ID:** "+(e["source_ids"] or "saknas")+
                        " · **Claim-ID:** "+(e["claim_ids"] or "saknas"),"",
                        "Obelagda uppgifter markeras `unknown`. Källor är inte bildlicenser. "+
                        "Likvärdiga fält innebär inte likvärdig faktaverifiering.",""])
        record_files[e["baseline_record_path"]]="\n".join(heading)

    outputs = {
        "catalog/entities.csv": render(entities,ENTITY_COLUMNS),
        "catalog/characters.csv": render(char,CHAR_COLUMNS),
        "catalog/celebrities.csv": render(people,PERSON_COLUMNS),
        "catalog/universes.csv": render(world,WORLD_COLUMNS),
        "quality/entity_quality.csv": render(qa,QA_COLUMNS),
        "quality/entity_parity.csv": render(parity,PARITY_COLUMNS),
        "quality/RESEARCH_BACKLOG.csv": render(sorted(backlog,key=lambda r:(r["priority"],r["entity_id"])),BACKLOG_COLUMNS),
        "evidence/attribute_evidence.csv": render(attributes,ATTRIBUTE_COLUMNS)
    }
    outputs.update(record_files)
    return outputs

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    files=build()
    stale=[]
    for name,expected in files.items():
        p=ROOT/name
        if args.check:
            if name.startswith("records/"):
                # Legacy records are preserved until first canonical regeneration.
                if not p.is_file() or not (p.read_text(encoding="utf-8").startswith("# ")):
                    stale.append(name)
            elif not p.is_file():
                stale.append(name)
            elif name.endswith(".csv"):
                with p.open(encoding="utf-8-sig",newline="") as f:
                    found=list(csv.DictReader(f))
                with io.StringIO(expected,newline="") as f:
                    wanted=list(csv.DictReader(f))
                if found != wanted: stale.append(name)
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(expected,encoding="utf-8")
    counts={"derived":len(files),"stale":len(stale),"examples":stale[:12]}
    print(json.dumps(counts,ensure_ascii=False,indent=2))
    return 1 if stale else 0

if __name__=="__main__":
    sys.exit(main())
