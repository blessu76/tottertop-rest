import json
import unittest
from pathlib import Path

from helpers import REPO

import indexnow as ix  # noqa: E402


class IndexNow(unittest.TestCase):
    def test_key_found_in_repo(self):
        self.assertRegex(ix.find_key(REPO), r"^[0-9a-f]{32}$")

    def test_payload(self):
        p = ix.build_payload("a" * 32, ["https://tottertop.ipe.rest/", "https://tottertop.ipe.rest/ko/"])
        self.assertEqual(p["host"], "tottertop.ipe.rest")
        self.assertEqual(p["keyLocation"], "https://tottertop.ipe.rest/%s.txt" % ("a" * 32))
        json.dumps(p)

    def test_mixed_hosts_and_empty_refused(self):
        with self.assertRaises(SystemExit):
            ix.build_payload("a" * 32, ["https://tottertop.ipe.rest/", "https://ipe.rest/"])
        with self.assertRaises(SystemExit):
            ix.build_payload("a" * 32, [])


if __name__ == "__main__":
    unittest.main()
