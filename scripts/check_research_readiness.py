#!/usr/bin/env python3
"""Check factual parity separately from structural parity. Exit nonzero if under threshold."""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--minimum", choices=("Q0", "Q1", "Q2", "Q3"), default="Q2")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    with (root / "catalog/entities.csv").open(encoding="utf-8-sig", newline="") as fh:
        records = list(csv.DictReader(fh))
    priority = {"Q0": 0, "Q1": 1, "Q2": 2, "Q3": 3}
    threshold = priority[args.minimum]
    failures = [r["entity_id"] for r in records
                if priority.get(r["research_grade"][:2], -1) < threshold]
    grades = Counter(r["research_grade"][:2] for r in records)
    print(json.dumps({"result": "PASS" if not failures else "BLOCKED",
                      "minimum": args.minimum, "entities": len(records),
                      "research_grades": dict(grades), "below_threshold": len(failures),
                      "sample_ids": failures[:20]}, ensure_ascii=False, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
