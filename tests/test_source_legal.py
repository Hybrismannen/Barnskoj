import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

class SourceLegalIntegrityTests(unittest.TestCase):
    def test_crosslinks_and_rights_have_full_coverage(self):
        p=subprocess.run([sys.executable,"scripts/validate_source_model.py"],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_generated_rights_ledger_not_stale(self):
        p=subprocess.run([sys.executable,"scripts/build_rights.py","--check"],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
