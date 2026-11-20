import csv
import json
import pathlib
import subprocess
import sys
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

class DiscoveryGraphTests(unittest.TestCase):
    def test_generated_views_fresh(self):
        r = subprocess.run([sys.executable, "scripts/build_discovery.py", "--check"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_all_graph_endpoints_exist(self):
        nodes = {n["node_id"] for n in rows("discovery/nodes.csv")}
        for e in rows("discovery/edges.csv"):
            self.assertIn(e["from_id"], nodes)
            self.assertIn(e["to_id"], nodes)

    def test_finite_crosslinks_and_license_boundary(self):
        cross = rows("discovery/crosslinks.csv")
        n = Counter(r["entity_id"] for r in cross)
        self.assertTrue(all(count <= 2 for count in n.values()))
        self.assertTrue(all(r["stage"] == "editorial_candidate" for r in cross))
        self.assertTrue(all(r["rights_boundary"] ==
                            "original_object_only_no_character_or_portrait_copy" for r in cross))
        self.assertTrue(all(r["match_basis"] in
                            {"shared_topic_and_era", "shared_topic_only"} for r in cross))

    def test_no_publication_overclaims(self):
        with (ROOT / "discovery/metrics.json").open(encoding="utf-8") as fh:
            metrics = json.load(fh)
        self.assertEqual(metrics["print_assets_published"], 0)
        self.assertEqual(metrics["cdx_standing"], "ANCHOR_DECLARED_NOT_CENTRALLY_VERIFIED")

if __name__ == "__main__":
    unittest.main()
