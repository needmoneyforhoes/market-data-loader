"""Load market_history.jsonl filtered against computable_tracker.jsonl.

Usage from a Python session:
    from load_clean import load_clean, load_all
    markets = load_clean()     # drops degraded markets
    all_m   = load_all()       # everything
"""
import json
import os

HIST_FILE    = "market_history.jsonl"
TRACKER_FILE = "computable_tracker.jsonl"


def load_all(path=HIST_FILE):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def load_clean(min_available=90, hist_path=HIST_FILE, tracker_path=TRACKER_FILE):
    markets = load_all(hist_path)
    if not os.path.exists(tracker_path):
        print(f"[load_clean] {tracker_path} not found — returning all {len(markets)}")
        return markets
    with open(tracker_path) as f:
        tracker = [json.loads(l) for l in f if l.strip()]
    bad = {e["slug"] for e in tracker if e["available"] < min_available}
    clean = [m for m in markets if m.get("slug") not in bad]
    print(f"[load_clean] {len(clean)}/{len(markets)} clean (dropped {len(bad)} with <{min_available} available fields)")
    return clean


if __name__ == "__main__":
    load_clean()
