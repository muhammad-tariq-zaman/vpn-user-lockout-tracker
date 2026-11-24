"""Track VPN users heading for, or already in, lockout.

Usage: python3 main.py lockouts.csv [--at-risk 3]
CSV columns: user,failed_attempts,locked,last_attempt_days.
locked is yes or no; last_attempt_days is how many days ago
the last failed attempt was. Verdicts:
- LOCKED: the account is locked.
- AT RISK: not locked, but failed attempts are at or above
  --at-risk (default 3).
- OK: fewer failed attempts than the threshold.
LOCKED first, then AT RISK (most attempts first), then OK.
Rows with a non-numeric failed_attempts or a locked value
other than yes/no are reported as skipped, not silently
dropped.
"""
import argparse, csv, sys

VERDICT_ORDER = {"LOCKED": 0, "AT RISK": 1, "OK": 2}

def track(rows, at_risk=3):
    out = []
    skipped = 0
    for row in rows:
        try:
            user = row["user"].strip()
            attempts = int(row["failed_attempts"])
            locked = row["locked"].strip().lower()
            days = int(row["last_attempt_days"])
            if not user or locked not in ("yes", "no"):
                raise ValueError("bad value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        if locked == "yes":
            verdict = "LOCKED"
            detail = f"account locked, {attempts} failed attempt(s)"
        elif attempts >= at_risk:
            verdict = "AT RISK"
            detail = (f"{attempts} failed attempt(s), last {days} day(s) ago")
        else:
            verdict = "OK"
            detail = f"{attempts} failed attempt(s)"
        out.append((user, attempts, verdict, detail))
    out.sort(key=lambda r: (VERDICT_ORDER[r[2]], -r[1], r[0]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--at-risk", type=int, default=3)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = track(list(csv.DictReader(f)), args.at_risk)
    for user, _, verdict, detail in results:
        print(f"{user}: {verdict} - {detail}")
    counts = {v: sum(1 for *_, verdict, _ in results if verdict == v)
              for v in VERDICT_ORDER}
    print(f"{counts['LOCKED']} locked, {counts['AT RISK']} at risk, "
          f"{counts['OK']} ok out of {len(results)} user(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
