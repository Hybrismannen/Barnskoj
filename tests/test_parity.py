import csv
import pathlib
import subprocess
import sys
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

class EntityParityTests(unittest.TestCase):
    def test_uniform_schema_and_references(self):
        run = subprocess.run([sys.executable, str(ROOT / "scripts/validate_parity.py")],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_all_485_present(self):
        entities = read("catalog/entities.csv")
        attributes = read("evidence/attribute_evidence.csv")
        counts = Counter(a["entity_id"] for a in attributes)
        self.assertEqual(len(entities), 485)
        self.assertEqual(len(counts), 485)
        self.assertEqual(set(counts.values()), {17})

    def test_no_fabricated_fact_completeness(self):
        entities = read("catalog/entities.csv")
        self.assertTrue(all(e["rights_status"] == "HOLD" for e in entities))
        self.assertFalse(any(e["research_grade"] == "Q3_deep_verified" for e in entities))

if __name__ == "__main__":
    unittest.main()
