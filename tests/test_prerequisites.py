import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

class PreconditionsTest(unittest.TestCase):
    def test_preconditions_are_computed_and_synchronized(self):
        p=subprocess.run([sys.executable,"scripts/check_wp_prerequisites.py","--check"],
                         cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_private_or_commercial_rights_never_auto_granted(self):
        state=json.loads((ROOT/"devops/PRE_WP_STATUS.json").read_text(encoding="utf-8"))
        self.assertFalse(state["right_to_sell_granted_automatically"])
        self.assertFalse(state["automatic_private_use_permission"])
