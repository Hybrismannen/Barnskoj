"""Contract tests for WP06 read-only pre-production decision gating."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "production_preflight.py"

class PreflightTests(unittest.TestCase):
    def run_preflight(self, *args):
        p = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT,
                           capture_output=True, text=True)
        self.assertIn(p.returncode, (0, 2), p.stderr)
        return p, json.loads(p.stdout)

    def test_preflight_never_auto_approves_publication(self):
        p, data = self.run_preflight()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(data["mode"], "READ_ONLY")
        self.assertFalse(data["activity_publication_approved"])
        self.assertFalse(data["central_CDX_admission_verified_by_this_script"])
        self.assertGreaterEqual(data["image_provenance_required"], data["image_provenance_verified"])

    def test_requires_all_prerequisites(self):
        p, data = self.run_preflight("--require-ready")
        expected = 0 if data["new_WP_eligible_for_human_review"] else 2
        self.assertEqual(p.returncode, expected)

if __name__ == "__main__":
    unittest.main()
