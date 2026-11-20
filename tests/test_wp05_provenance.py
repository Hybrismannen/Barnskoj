"""Contract tests for the WP05 non-promoting provenance audit."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_image_provenance.py"

class ProvenanceAuditTests(unittest.TestCase):
    def run_audit(self, *args):
        p = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT,
                           capture_output=True, text=True)
        self.assertIn(p.returncode, (0, 2), p.stderr)
        return p, json.loads(p.stdout)

    def test_totals_and_no_automatic_license(self):
        p, data = self.run_audit("--summary")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(data["target_count"], sum(data["status_counts"].values()))
        self.assertEqual(data["provenance_verified"] + data["provenance_unverified"],
                         data["target_count"])
        self.assertEqual(data["duplicate_ids"], [])
        self.assertTrue(data["read_only"])

    def test_incomplete_provenance_fails_closed(self):
        p, data = self.run_audit("--summary", "--require-complete")
        expected = 2 if data["provenance_unverified"] else 0
        self.assertEqual(p.returncode, expected)

if __name__ == "__main__":
    unittest.main()
