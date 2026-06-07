# market-data-loader

Source-of-truth market-history loader and data-quality QA used across the Polymarket quant research stack.

## Why it exists

Every backtest, strategy scan, and model-training job in the suite reads the same
`market_history.jsonl` corpus. Some markets are degraded (missing book/indicator
fields from feed gaps), and silently including them poisons backtests. This repo is
the single canonical loader: it filters the raw history against a per-market quality
tracker so downstream consumers all see the same clean dataset, plus a small QA check
to spot-test field population.

## What's inside

| Module | Purpose |
| --- | --- |
| `load_clean.py` | The loader. `load_all()` reads every market from `market_history.jsonl`; `load_clean(min_available=90)` cross-references `computable_tracker.jsonl` and drops any market whose `available` field count falls below the threshold. Import as `from load_clean import load_clean, load_all`. |
| `check_null_rate.py` | Data-quality QA: loads the clean set and reports what fraction of markets have `bn_delta_final` populated — a quick null-rate sanity check after a corpus refresh. |

`load_clean` is import-first (designed to be called from other research scripts) but
also runs standalone via its `__main__`, printing the clean/dropped counts.

## Requirements

- Python 3 (standard library only — `json`, `os`; no third-party deps)
- The data corpus (see below). With no `computable_tracker.jsonl` present, `load_clean`
  fails open and returns all markets with a warning.

## Usage

```bash
# Print clean/dropped counts (expects the two .jsonl files in cwd)
python load_clean.py

# Field-population QA on the clean set
python check_null_rate.py
```

From a Python session:

```python
from load_clean import load_clean, load_all
markets = load_clean()           # drops degraded markets (<90 available fields)
markets = load_clean(min_available=80)
all_m   = load_all()             # unfiltered
```

## Data

This repo ships **no data**. Both scripts read `market_history.jsonl` and
`computable_tracker.jsonl` from the working directory; these are maintained in the
private **polymarket-data** repo. Point the process at that checkout (run from its
root, or symlink the files in) — they are git-ignored here and must never be committed.

> Private research software. No warranty; use at your own risk.
