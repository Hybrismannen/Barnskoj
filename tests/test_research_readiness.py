import csv
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
class ReadinessTests(unittest.TestCase):
    def test_current_catalogue_is_not_falsely_certified(self):
        proc = subprocess.run([sys.executable, "scripts/check_research_readiness.py",
                               "--minimum", "Q2"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn('"below_threshold": 448', proc.stdout)

    def test_complete_q0_coverage_as_baseline(self):
        proc = subprocess.run([sys.executable, "scripts/check_research_readiness.py",
                               "--minimum", "Q0"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
