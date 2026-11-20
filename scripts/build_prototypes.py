#!/usr/bin/env python3
"""Produce printable A4 vector prototypes with exact numbered dot routes.

Outputs are internal prototypes, NOT human-tested, rights-cleared or published.
No third-party imagery, font downloads, network access or binary dependencies.
"""
import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPECS=ROOT/"production/prototype_specs.json"

def route(spec):
    key=spec["contour"]
    if len(key)<3: raise ValueError("Insufficient contour")
    out=[]
    for i,a in enumerate(key):
        b=key[(i+1)%len(key)]
        length=math.hypot(b[0]-a[0],b[1]-a[1])
        n=max(1,math.ceil(length/spec["step_mm"]))
        for j in range(n):
            t=j/n
            out.append((round(a[0]+(b[0]-a[0])*t,2),
                        round(a[1]+(b[1]-a[1])*t,2)))
    if not 15<=len(out)<=100:
        raise ValueError("Unreasonable dot count")
    for i,p in enumerate(out):
        x,y=p
        if not (20<=x<=190 and 42<=y<=250): raise ValueError("Point out of safe A4 area")
        q=out[(i+1)%len(out)]
        if math.hypot(q[0]-x,q[1]-y)<6:
            raise ValueError("Dots too close to label/print reliably")
    return out

def fmt(n):
    return f"{n:.2f}"

def decorations(kind):
    if kind=="jukebox":
        return [
         '<path d="M61 143 V112 Q62 79 105 72 Q148 79 149 112 V143" fill="none" stroke="#555" stroke-width="1.6"/>',
         '<path d="M64 160 H146 M64 178 H146 M64 195 H146" stroke="#777" stroke-width="1.2"/>',
         '<rect x="75" y="202" width="60" height="19" rx="3" fill="none" stroke="#555" stroke-width="1.5"/>'
        ]
    if kind=="disco":
        return [
         '<path d="M48 145 H162 M59 111 H151 M59 179 H151 M105 83 V207 M76 92 Q105 145 76 198 M134 92 Q105 145 134 198" fill="none" stroke="#777" stroke-width="1.2"/>',
         '<path d="M105 81 V67" stroke="#777" stroke-width="1.5"/>'
        ]
    if kind=="arcade":
        return [
         '<rect x="82" y="109" width="46" height="37" rx="3" fill="none" stroke="#555" stroke-width="1.6"/>',
         '<path d="M76 160 H134 M77 178 H133" stroke="#777" stroke-width="1.3"/>',
         '<path d="M97 168 v-10" stroke="#555" stroke-width="1.6"/>',
         '<circle cx="97" cy="157" r="3" fill="none" stroke="#555" stroke-width="1.4"/>',
         '<circle cx="117" cy="166" r="3" fill="none" stroke="#555" stroke-width="1.3"/>',
         '<circle cx="127" cy="166" r="3" fill="none" stroke="#555" stroke-width="1.3"/>'
        ]
    raise ValueError("Unknown original decor")

def svg(spec,answer=False):
    points=route(spec)
    id=spec["activity_id"]
    title=spec["title"]
    lines=[
     '<?xml version="1.0" encoding="utf-8"?>',
     '<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297" role="img">',
     '<title>'+("Facit – " if answer else "Prick till prick – ")+title+'</title>',
     '<desc>Eget originalmotiv i A4, en intern prototyp. '+("Facit visar sammanbunden kontur." if answer else "Förbind punkterna i nummerordning.")+'</desc>',
     '<rect width="210" height="297" fill="white"/>',
     '<text x="20" y="24" font-family="sans-serif" font-size="8" font-weight="bold" fill="#222">'+("FACIT · " if answer else "PRICK TILL PRICK · ")+title+'</text>',
     '<text x="20" y="34" font-family="sans-serif" font-size="3.8" fill="#555">'+("Originalkonturen med lösning" if answer else "Förbind 1 till "+str(len(points))+" i nummerordning")+'</text>',
    ]
    if answer:
        coords=" ".join(fmt(x)+","+fmt(y) for x,y in points+[points[0]])
        lines.append('<polyline data-role="solution-route" fill="none" stroke="#222" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" points="'+coords+'"/>')
        lines.extend(decorations(spec["detail_type"]))
    else:
        for i,(x,y) in enumerate(points,1):
            lines.append('<circle data-dot-number="'+str(i)+'" cx="'+fmt(x)+'" cy="'+fmt(y)+'" r="0.85" fill="#222"/>')
            lines.append('<text data-label-number="'+str(i)+'" x="'+fmt(x+2.4)+'" y="'+fmt(y-2.1)+'" font-family="sans-serif" font-size="3.3" fill="#222">'+str(i)+'</text>')
    lines.extend([
     '<path d="M20 258 H190" stroke="#aaa" stroke-width="0.35"/>',
     '<text x="20" y="265" font-family="sans-serif" font-size="3.5" fill="#555">BARNSKOJ · ORIGINALPROTOTYP · EJ PUBLICERAD</text>',
     '<text x="20" y="272" font-family="sans-serif" font-size="3" fill="#777">'+id+' · '+str(len(points))+' punkter · A4 1:1</text>',
     '</svg>', ''
    ])
    return "\n".join(lines)

def outputs():
    specs=json.loads(SPECS.read_text(encoding="utf-8"))
    result={}
    for s in specs:
        result["production/prototypes/"+s["activity_id"]+".svg"]=svg(s,False)
        result["production/solutions/"+s["activity_id"]+".svg"]=svg(s,True)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    stale=[]
    for name,content in outputs().items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8")!=content: stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding="utf-8")
    print(json.dumps({"generated_files":6,"stale":stale},ensure_ascii=False))
    return 1 if stale else 0
if __name__=="__main__":
    raise SystemExit(main())
