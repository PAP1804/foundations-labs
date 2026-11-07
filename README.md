# foundations-labs

Portfolio of hands-on data foundations labs, built step by step with plain Python.

## Requirements

- Python 3 (check with `python3 --version`; install from https://www.python.org/downloads/)
- No third-party packages: the labs use the standard library only.

## Labs

| Week | Day | File | What it does |
|------|-----|------|--------------|
| 1 | 1 | [`week1/day1.py`](week1/day1.py) | Loads the Palmer Penguins CSV with the stdlib `csv` module, prints the column names and first 5 rows, and counts total rows and rows with any missing value. |

## Running

```bash
cd week1
python3 day1.py
```

Expected result on the included `penguins.csv`:

```
Total rows: 344
Rows with any missing value: 11
```

## Data

`week1/penguins.csv` is the Palmer Penguins dataset (Gorman, Williams & Fraser, 2014;
distributed in the [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) project, CC0).
Missing values are recorded as `NA`.
