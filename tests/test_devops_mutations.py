"""WP02: regression tests for partial updates and fail-closed publication.

Operate in-memory. Do not mutate repository source files in CI.
"""
import copy
import csv
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from scripts import build_catalog, validate_production

def table(s):
    return list(csv.DictReader(io.StringIO(s)))

class MutationAndReleaseGuards(unittest.TestCase):
    def test_one_name_edit_reflows_master_legacy_and_card(self):
        original_load=build_catalog.load
        def changed(path):
            data=original_load(path)
            if path=="catalog/source/entities_base.csv":
                data=copy.deepcopy(data)
                data[0]["display_name"]="TEST_ONLY_RENAMED_ENTITY"
            return data
        with patch.object(build_catalog,"load",side_effect=changed):
            generated=build_catalog.build()
        self.assertEqual(table(generated["catalog/entities.csv"])[0]["display_name"],
                         "TEST_ONLY_RENAMED_ENTITY")
        self.assertEqual(table(generated["catalog/characters.csv"])[0]["name"],
                         "TEST_ONLY_RENAMED_ENTITY")
        self.assertIn("TEST_ONLY_RENAMED_ENTITY",
                      generated["records/BS-CHAR-0001.md"])

    def test_unproved_historical_field_is_rejected(self):
        original_load=build_catalog.load
        def poisoned(path):
            data=original_load(path)
            if path=="catalog/source/entities_base.csv":
                data=copy.deepcopy(data)
                data[0]["origin_country"]="Sweden"
            return data
        with patch.object(build_catalog,"load",side_effect=poisoned):
            with self.assertRaisesRegex(ValueError,"Unproved historical fact"):
                build_catalog.build()

    def test_false_claim_reference_is_rejected(self):
        original_load=build_catalog.load
        def poisoned(path):
            data=original_load(path)
            if path=="evidence/field_proofs.csv":
                data=copy.deepcopy(data)
                data[0]["claim_id"]="CLM-DOES-NOT-EXIST"
            return data
        with patch.object(build_catalog,"load",side_effect=poisoned):
            with self.assertRaisesRegex(ValueError,"Proof not bound"):
                build_catalog.build()

    def test_publishing_without_reviews_fails_closed(self):
        real_load=validate_production.load
        def poisoned(path):
            data=real_load(path)
            if path=="production/activities.csv":
                data=copy.deepcopy(data)
                data[0]["status"]="published"
                data[0]["published_at"]="2026-11-20"
            return data
        validate_production.ERRORS.clear()
        try:
            with patch.object(validate_production,"load",side_effect=poisoned):
                with redirect_stdout(io.StringIO()):
                    result=validate_production.run()
            self.assertEqual(result,1)
            self.assertTrue(any("Publication missing rights_review" in x
                                for x in validate_production.ERRORS))
            self.assertTrue(any("Published asset not cleared" in x
                                for x in validate_production.ERRORS))
        finally:
            validate_production.ERRORS.clear()

if __name__=="__main__":
    unittest.main()
