import csv
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

class CatalogueQualityTests(unittest.TestCase):
    def test_validator(self):
        p = subprocess.run([sys.executable, str(ROOT / "scripts/validate_catalog.py")],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_same_name_different_universes(self):
        matches = [r for r in rows("catalog/characters.csv") if r["name"] == "Red"]
        self.assertGreaterEqual(len(matches), 2)
        self.assertGreaterEqual(len({r["universe_id"] for r in matches}), 2)
        self.assertEqual(len({r["canonical_entity_id"] for r in matches}), len(matches))

    def test_mondo_alias(self):
        x = {r["id"]: r for r in rows("catalog/celebrities.csv")}
        self.assertEqual(x["BS-PER-0091"]["canonical_entity_id"],
                         x["BS-PER-0088"]["canonical_entity_id"])

    def test_evidence_no_auto_rights(self):
        grades = rows("quality/entity_quality.csv")
        self.assertTrue(all(r["rights_gate"] == "HOLD" for r in grades))
        self.assertTrue(all(r["research_grade"] != "Q3_deep_verified" for r in grades))

if __name__ == "__main__":
    unittest.main()
