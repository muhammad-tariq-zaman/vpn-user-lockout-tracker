import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import track

def row(user, attempts, locked, days):
    return {"user": user, "failed_attempts": str(attempts), "locked": locked,
            "last_attempt_days": str(days)}

class TestLockoutTracker(unittest.TestCase):
    def test_locked(self):
        r, _ = track([row("bilal", 5, "yes", 0)])
        self.assertEqual(r[0][2], "LOCKED")

    def test_at_risk(self):
        r, _ = track([row("ayesha", 4, "no", 1)])
        self.assertEqual(r[0][2], "AT RISK")

    def test_exactly_threshold_is_at_risk(self):
        r, _ = track([row("ayesha", 3, "no", 1)])
        self.assertEqual(r[0][2], "AT RISK")

    def test_below_threshold_is_ok(self):
        r, _ = track([row("sara", 2, "no", 0)])
        self.assertEqual(r[0][2], "OK")

    def test_custom_threshold(self):
        r, _ = track([row("ayesha", 4, "no", 1)], at_risk=5)
        self.assertEqual(r[0][2], "OK")

    def test_locked_comes_first(self):
        r, _ = track([row("ayesha", 4, "no", 1), row("bilal", 5, "yes", 0)])
        self.assertEqual(r[0][0], "bilal")

    def test_most_attempts_first_within_verdict(self):
        r, _ = track([row("ayesha", 3, "no", 1), row("omar", 4, "no", 2)])
        self.assertEqual(r[0][0], "omar")

    def test_invalid_row_is_skipped(self):
        r, skipped = track([row("x", "many", "no", 1),
                            row("sara", 1, "no", 0)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(track([]), ([], 0))
