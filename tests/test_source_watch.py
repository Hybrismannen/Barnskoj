import unittest
from scripts import watch_wiki_sources as watch

class WatchTests(unittest.TestCase):
    def test_no_false_inference_or_duplicate(self):
        source={"source_id":"T","franchise_id":"GOT","page_url":"https://test.example/p"}
        state,events,changes=watch.merge_observation(
            [source],{"sources":{}},[],{"T":("12","OBSERVED")},"2026-11-20T00:00:00Z")
        self.assertEqual(events,[])
        state,events,changes=watch.merge_observation(
            [source],state,events,{"T":("13","OBSERVED")},"2026-11-21T00:00:00Z")
        self.assertEqual(len(changes),1)
        self.assertEqual(changes[0]["status"],"REVIEW_REQUIRED")
        state,events,changes=watch.merge_observation(
            [source],state,events,{"T":(None,"ACCESS_BLOCKED")},"2026-11-22T00:00:00Z")
        self.assertEqual(len(changes),0)
        self.assertEqual(state["sources"]["T"]["version"],"13")
        state,events,changes=watch.merge_observation(
            [source],state,events,{"T":("13","OBSERVED")},"2026-11-23T00:00:00Z")
        self.assertEqual(len(events),1)
