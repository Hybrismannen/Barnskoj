import csv
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def table(p):
    with (ROOT / p).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

class CanonicalBuildTests(unittest.TestCase):
    def test_derived_views_match_source(self):
        r = subprocess.run([sys.executable,"scripts/build_catalog.py","--check"],
                           cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)

    def test_write_model_owns_every_entity(self):
        base=table("catalog/source/entities_base.csv")
        extras=table("catalog/source/legacy_details.csv")
        visible=table("catalog/entities.csv")
        self.assertEqual(len(base),485)
        self.assertEqual({e["entity_id"] for e in base},{e["entity_id"] for e in visible})
        self.assertEqual({e["entity_id"] for e in base},{e["entity_id"] for e in extras})

    def test_no_claim_without_sparse_provenance(self):
        proofs=table("evidence/field_proofs.csv")
        attributes=table("evidence/attribute_evidence.csv")
        ids={(x["entity_id"],x["attribute"]) for x in proofs}
        reported={(x["entity_id"],x["attribute"]) for x in attributes if x["evidence_status"]=="claim_verified"}
        self.assertEqual(ids,reported)
