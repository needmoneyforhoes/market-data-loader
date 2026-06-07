# market-data-loader

Canonical loader and null-rate QA for the `market_history.jsonl` corpus used across the Polymarket quant stack.

Filters raw market history against a per-market quality tracker so every backtest, scan, and training job reads the same clean dataset.

## Contents

| File | What it does |
| --- | --- |
| `load_clean.py` | `load_all()` reads every market from `market_history.jsonl`. `load_clean(min_available=90)` cross-references `computable_tracker.jsonl` and drops markets whose `available` field count is below the threshold. |
| `check_null_rate.py` | Loads the clean set and reports the fraction of markets with `bn_delta_final` populated. |

`load_clean` is import-first but also runs standalone, printing clean/dropped counts. With no `computable_tracker.jsonl` present it returns all markets and prints a warning.

Stdlib only (`json`, `os`); Python 3.

## Usage

```bash
python load_clean.py        # print clean/dropped counts
python check_null_rate.py   # bn_delta_final null-rate on the clean set
```

```python
from load_clean import load_clean, load_all
markets = load_clean()                # drops markets with <90 available fields
markets = load_clean(min_available=80)
all_m   = load_all()                  # unfiltered
```

## Data

Reads `market_history.jsonl` and `computable_tracker.jsonl` from the working directory. Both are maintained in the private polymarket-data repo; run from its checkout or symlink the files in. Git-ignored here.
