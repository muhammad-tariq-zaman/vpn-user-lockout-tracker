# vpn-user-lockout-tracker

Track VPN users heading for, or already in, lockout: the input CSV lists user, failed_attempts, locked (yes/no) and last_attempt_days — LOCKED when the account is locked, AT RISK when not locked but failed attempts are at or above --at-risk (default 3), OK otherwise — LOCKED first, then AT RISK (most attempts first), then OK. Rows with a non-numeric failed_attempts or a locked value other than yes/no are reported as skipped, not silently dropped.

Sample input is included (sample.csv with six users, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
bilal: LOCKED - account locked, 5 failed attempt(s)
ayesha: AT RISK - 4 failed attempt(s), last 1 day(s) ago
omar: AT RISK - 3 failed attempt(s), last 2 day(s) ago
sara: OK - 1 failed attempt(s)
hina: OK - 0 failed attempt(s)
1 locked, 2 at risk, 2 ok out of 5 user(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
