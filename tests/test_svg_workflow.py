import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

class SvgWorkflowTests(unittest.TestCase):
    def test_svg_prototypes_reproducible(self):
        r=subprocess.run([sys.executable,"scripts/build_prototypes.py","--check"],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)

    def test_prototype_print_geometry_and_solution_match(self):
        r=subprocess.run([sys.executable,"scripts/validate_svg_prototypes.py"],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)

    def test_no_publication_bypass(self):
        r=subprocess.run([sys.executable,"scripts/validate_production.py"],
                         cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('"published": 0',r.stdout)
        self.assertIn('"activities": 3',r.stdout)
