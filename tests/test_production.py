import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class ProductionSafetyTests(unittest.TestCase):
    def test_no_unapproved_publications(self):
        proc = subprocess.run([sys.executable, "scripts/validate_production.py"],
                              cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('"published": 0', proc.stdout)
