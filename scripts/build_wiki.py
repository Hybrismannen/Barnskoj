#!/usr/bin/env python3
"""Build versioned GitHub Wiki pages from sourced registries. Never fetch remote assets."""
import argparse
import csv
import json
import pathlib
from collections import Counter, defaultdict

ROOT=pathlib.Path(__file__).resolve().parents[1]
WIKI=ROOT/"wiki-src"
BASE="https://github.com/Hybrismannen/Barnskoj/blob/main/"
def table(name):
    with (ROOT/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
def esc(s):
    return (s or "").replace("|",r"\|").replace("\n"," ")
def link(name,url):
    return "["+esc(name)+"]("+url+")" if url else "—"
def build():
    entities=table("catalog/entities.csv")
    images=table("images/requirements.csv")
    stage_images=table("images/staged_requirements.csv")
    franchises=table("sourcing/franchises.csv")
    sources=table("sourcing/wiki_sources.csv")
    staged=table("sourcing/staged_entities.csv")
    rights=table("rights/ledger.csv")
    licenses=table("rights/license_matrix.csv")
    status=Counter(x["image_status"] for x in images+stage_images)
    header=[
      "# Bildindex – originalbilder och källstatus",
      "",
      "**Alla historiska originalbilder ska kunna härledas till exakt källa, upphov och licens.** "
      "En saknad bild är aldrig en fri publiceringsrätt.",
      "",
      f"**Mål: {len(images)+len(stage_images)}** "
      f"({len(entities)} katalogentiteter + {len(images)-len(entities)} motiv "
      f"+ {len(staged)} nya granskningskandidater).",
      "",
      "Status: "+", ".join(f"{k}: {n}" for k,n in sorted(status.items()))+".",
      "",
      "- [Figurer och barn-tv](Bildindex-Figurer)",
      "- [Personer och grupper](Bildindex-Personer)",
      "- [Berättelsevärldar](Bildindex-Universum)",
      "- [Originalmotiv](Bildindex-Motiv)",
      "- [Nya universumkandidater](Bildindex-Staging)",
      "",
      "[Fullständig rådata](https://github.com/Hybrismannen/Barnskoj/tree/main/images) · "
      "[Rättighetsöversikt](Rattighetsmatris) · "
      "[Källbevakning](Universumkallor)",
      ""
    ]
    out={"wiki-src/Bildindex.md":"\n".join(header)}
    groups=[
      ("Bildindex-Figurer","BS-CHAR",images),
      ("Bildindex-Personer","BS-PER",images),
      ("Bildindex-Universum","BS-WORLD",images),
      ("Bildindex-Motiv","BS-MOT",images),
      ("Bildindex-Staging","BC-",stage_images)
    ]
    for page,prefix,data in groups:
        rows=[r for r in data if r["target_id"].startswith(prefix)]
        title={
          "Bildindex-Figurer":"Figurer och barn-tv",
          "Bildindex-Personer":"Personer och grupper",
          "Bildindex-Universum":"Berättelsevärldar",
          "Bildindex-Motiv":"Originalmotiv",
          "Bildindex-Staging":"Nya staged universumkandidater"
        }[page]
        lines=["# "+title,"",f"**{len(rows)} individuella bildkrav.** "
               "Ett sökspår är inte ett licensbeslut.","",
               "| ID | Entitet | Bildstatus | Originalbild / källa | Rättighet |",
               "| --- | --- | --- | --- | --- |"]
        for r in rows:
            id=r["target_id"]
            ref=(BASE+"records/"+id+".md" if prefix in ("BS-CHAR","BS-PER","BS-WORLD")
                 else BASE+"creative/motifs.json" if prefix=="BS-MOT"
                 else BASE+"sourcing/staged_entities.csv")
            lines.append("| "+link(id,ref)+" | "+esc(r["title"])+" | "+
                         esc(r["image_status"])+" | "+
                         link("Källobjekt",r["image_page_url"])+" | "+
                         esc(r["rights_review"])+" |")
        lines.extend(["","[Alla bildbehov](Bildindex) · [Rättighetsmatris](Rattighetsmatris)",""])
        out["wiki-src/"+page+".md"]="\n".join(lines)
    src_by_fr=defaultdict(list)
    cand_by_fr=defaultdict(list)
    for s in sources: src_by_fr[s["franchise_id"]].append(s)
    for x in staged: cand_by_fr[x["franchise_id"]].append(x)
    lines=["# Levande universumkällor","",
           "Fan-wikis och officiella register bevakas som **källspår**. "
           "En ändrad artikel skapar ett granskningsärende, inte automatiskt ett nytt faktum.",
           "",
           f"**{len(franchises)} källfamiljer, {len(sources)} registrerade webbsidor "
           f"och {len(staged)} iscensatta kandidater.**",""]
    for f in franchises:
        fid=f["franchise_id"]
        lines.extend(["## "+f["name"],"",
                      "**Äldre universum-ID:** "+f["existing_world_id"]+"  ",
                      "**Möjliga rättighetskontakter:** "+f["possible_owner_contact"]+"  ",
                      "**Särskilda versioner:** "+f["continuity_variants"],"",
                      "| Källa | Typ | Kontinuitet | Bevakning |",
                      "| --- | --- | --- | --- |"])
        for s in src_by_fr[fid]:
            lines.append("| "+link(s["source_name"],s["page_url"])+" | "+
                         esc(s["source_kind"])+" | "+esc(s["media_scope"])+
                         " | "+esc(s["watch_mode"])+" |")
        if cand_by_fr[fid]:
            lines.extend(["","**Objekt som väntar på identitetsgranskning:** "+
                          ", ".join(esc(c["display_name"])+" ("+c["continuity"]+")"
                                    for c in cand_by_fr[fid])+"."])
        lines.append("")
    lines.extend(["[Rådata och uppdateringsstatus]("+BASE+"sourcing/README.md) · "
                  "[Rättighetspolicy](Rattigheter)",""])
    out["wiki-src/Universumkallor.md"]="\n".join(lines)
    metrics=json.loads((ROOT/"rights/metrics.json").read_text(encoding="utf-8"))
    lines=["# Rättighetsmatris för Barnskoj","",
           f"**{metrics['total_targets']} objekt – "
           f"{metrics['rights_granted']} dokumenterat godkända.** "
           "Allt är HOLD tills ett faktiskt beslut finns.",
           "",
           "**Wiki-text och bildlicens är två olika tillstånd.** "
           "Fandom-text kan normalt vara CC BY-SA 3.0 utan att "
           "karaktärsdesignen eller uppladdad bildfil får omritas och säljas.",
           "",
           "| Licens | Kommersiell bok | Bearbetad målarbild |",
           "| --- | --- | --- |"]
    for x in licenses:
        lines.append("| "+link(x["license_class"],x["license_reference"])+
                     " | "+esc(x["commercial_sale"])+" | "+
                     esc(x["publication_of_adaptation"])+" |")
    lines.extend(["",
      "[Juridiskt beslutsregister för alla 526 objekt]("+BASE+"rights/ledger.csv) · "
      "[Originala bildobjekt](Bildindex) · "
      "[Fullständig bedömning]("+BASE+"rights/README.md)",""])
    out["wiki-src/Rattighetsmatris.md"]="\n".join(lines)
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    files=build()
    stale=[]
    for name,content in files.items():
        path=ROOT/name
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8")!=content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding="utf-8")
    print(json.dumps({"status":"FAIL" if stale else "PASS","pages":len(files),
                      "stale":stale},ensure_ascii=False))
    return int(bool(stale))
if __name__=="__main__":
    raise SystemExit(main())
