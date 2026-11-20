#!/usr/bin/env python3
"""Barnskoj one-command DevOps health gate, read-only; no deployment/publication."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CMDS=[
 ("WP01 canonical source and derived views",["scripts/build_catalog.py","--check"]),
 ("WP02 catalog integrity",["scripts/validate_catalog.py"]),
 ("WP02 entity parity",["scripts/validate_parity.py"]),
 ("WP02 creative graph freshness",["scripts/build_discovery.py","--check"]),
 ("WP03 generated SVG freshness",["scripts/build_prototypes.py","--check"]),
 ("WP03 vector layout and solutions",["scripts/validate_svg_prototypes.py"]),
 ("WP03 publication and rights",["scripts/validate_production.py"]),
 ("CDX pinned anchor",[".cdx/check_anchor.py"]),
 ("CDX declared-not-verified state",[".cdx/check_local_state.py"]),
 ("Regression and adversarial tests",["-m","unittest","discover","-s","tests","-v"]),
]
def main():
    results=[]
    for name,command in CMDS:
        p=subprocess.run([sys.executable,*command],cwd=ROOT,
                         text=True,capture_output=True)
        results.append({"gate":name,"status":"PASS" if p.returncode==0 else "FAIL",
                        "code":p.returncode,
                        "details":(p.stdout+p.stderr)[-1200:] if p.returncode else ""})
    state={"result":"PASS" if all(r["code"]==0 for r in results) else "FAIL",
           "gates":results,"scope":"local static CI; not human release or central CDX admission"}
    print(json.dumps(state,indent=2,ensure_ascii=False))
    return 0 if state["result"]=="PASS" else 1
if __name__=="__main__":
    sys.exit(main())
