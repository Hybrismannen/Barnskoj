#!/usr/bin/env python3
"""WP03 prototype SVG QC: geometry, IDs, number sequence, A4 and answer integrity."""
import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NS="{http://www.w3.org/2000/svg}"

def readcsv(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def validate():
    specs=json.loads((ROOT/"production/prototype_specs.json").read_text(encoding="utf-8"))
    rows=readcsv("production/activities.csv")
    assets=readcsv("production/assets.csv")
    rr={r["activity_id"]:r for r in rows}
    assetmap={r["asset_id"]:r for r in assets}
    errors=[]
    result={}
    for spec in specs:
        ident=spec["activity_id"]
        activity=rr.get(ident)
        if not activity or activity["status"]!="prototype" or activity["motif_id"]!=spec["motif_id"]:
            errors.append(ident+" unregistered/wrong status")
            continue
        if activity["format_id"]!="dot-to-dot" or activity["requires_solution"]!="yes":
            errors.append(ident+" invalid format/solution requirement")
        if any(activity[x]=="PASS" for x in ("human_review","rights_review","print_review","accessibility_review")):
            errors.append(ident+" falsely accepted reviewer gate")
        asset=assetmap.get(activity["asset_id"])
        solution=assetmap.get(activity["solution_asset_id"])
        if not asset or not solution:
            errors.append(ident+" missing asset manifest")
            continue
        if asset["source_path"] != "production/prototypes/"+ident+".svg" or solution["source_path"] != "production/solutions/"+ident+".svg":
            errors.append(ident+" unexpected asset paths")
        if any(a["rights_status"]=="CLEARED" for a in (asset,solution)):
            errors.append(ident+" rights cleared without human review")
        try:
            doc=ET.parse(ROOT/asset["source_path"]).getroot()
            answer=ET.parse(ROOT/solution["source_path"]).getroot()
            for root in (doc,answer):
                if root.tag!=NS+"svg" or root.get("viewBox")!="0 0 210 297" or root.get("width")!="210mm" or root.get("height")!="297mm":
                    errors.append(ident+" invalid A4 geometry")
            dots=[x for x in doc.iter(NS+"circle") if x.get("data-dot-number")]
            labels=[x for x in doc.iter(NS+"text") if x.get("data-label-number")]
            dnums=[int(x.get("data-dot-number")) for x in dots]
            lnums=[int(x.get("data-label-number")) for x in labels]
            if dnums!=list(range(1,len(dnums)+1)) or lnums!=dnums:
                errors.append(ident+" noncontinuous or unmatched labels")
            if len(dnums)<15 or len(dnums)>100:
                errors.append(ident+" invalid point count")
            coords=[(float(d.get("cx")),float(d.get("cy"))) for d in dots]
            for i,p in enumerate(coords):
                q=coords[(i+1)%len(coords)]
                if not (20<=p[0]<=190 and 42<=p[1]<=250):
                    errors.append(ident+" printable safety envelope violation")
                if math.hypot(q[0]-p[0],q[1]-p[1])<6:
                    errors.append(ident+" adjacent dots too close")
            routes=[x for x in answer.iter(NS+"polyline") if x.get("data-role")=="solution-route"]
            if len(routes)!=1:
                errors.append(ident+" no unique answer route")
            else:
                ps=[tuple(map(float,p.split(","))) for p in routes[0].get("points","").split()]
                if len(ps)!=len(coords)+1 or ps!=coords+[coords[0]]:
                    errors.append(ident+" answer route differs from puzzle dots")
            if len(dnums)>0: result[ident]=len(dnums)
        except (ET.ParseError,ValueError,OSError,IndexError) as exc:
            errors.append(ident+" malformed SVG: "+str(exc))
    status={"status":"PASS" if not errors else "FAIL","validated":result,"error_count":len(errors),"errors":errors}
    print(json.dumps(status,indent=2,ensure_ascii=False))
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(validate())
