#!/usr/bin/env python3
"""Query read-only generated discovery views; no runtime actions or web access."""
import argparse
import csv
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def rows(rel):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--entity", default=None, help="Example: BS-CHAR-0001")
    p.add_argument("--theme", default=None, help="Example: music")
    p.add_argument("--era", default=None, help="Example: 1980s")
    p.add_argument("--limit", type=int, default=12)
    args = p.parse_args()
    idx = rows("discovery/search.csv")
    links = rows("discovery/crosslinks.csv")
    if args.entity:
        found = next((x for x in idx if x["node_id"] == args.entity), None)
        if found is None:
            raise SystemExit("Unknown entity ID")
        filtered = [r for r in links if r["entity_id"] == args.entity]
        result = {"entity": found,
                  "original_motif_candidates": [
                      {"relation": link, "motif": next((m for m in idx if m["node_id"] == link["motif_id"]), None)}
                      for link in filtered[:max(args.limit,0)]
                  ], "disclaimer": "Editorial suggestions only; no factual or image rights inference"}
    else:
        filtered = [x for x in idx
                    if (not args.theme or args.theme in x["theme_ids"].split(";"))
                    and (not args.era or "era:" + args.era in x["era_ids"].split(";"))]
        result = {"count": len(filtered), "results": filtered[:max(args.limit,0)]}
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
