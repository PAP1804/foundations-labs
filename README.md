# foundations-labs

Hands-on labs for applied data science, AI engineering, financial engineering, and quantitative finance.

Each lab is a small, runnable program built from first principles: standard library first, libraries once the fundamentals are clear. Every completed lab records its output and the takeaways learned along the way.

## Layout

```
foundations-labs/
├── README.md          this file: overview and index
└── weekN/
    ├── README.md      the week's plan, progress, outputs and takeaways
    ├── dayN.py        one script per lab
    └── *.csv          data used that week
```

## Labs

### [Week 1 — Python foundations](week1/README.md)

| Day | Lab | Status |
|-----|-----|--------|
| 1 | [`day1.py`](week1/day1.py): first look at the Palmer Penguins CSV, row and missing-value counts | Done |
| 2 | [`day2.py`](week1/day2.py): counts per species, missing per column, species with most missing rows | Done |
| 3 | [`day3.py`](week1/day3.py): the same answers as one-job functions | Done |
| 4 | [`day4.py`](week1/day4.py): the answers with dicts (counter pattern) and a tuple; [Week 1 cleaning log](week1/README.md#week-1-cleaning-log) | Done |

## Running

Requires Python 3 (`python3 --version`; install from https://www.python.org/downloads/). Week 1 uses the standard library only.

Run any lab from the repo root:

```bash
python3 week1/day1.py
```

## Data

| Dataset | File | Source | License | SHA-256 | Used in |
|---------|------|--------|---------|---------|---------|
| Palmer Penguins | [`week1/penguins.csv`](week1/penguins.csv) | Gorman, Williams & Fraser (2014), via [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) | CC0 | `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93` | Week 1 |

Verify a dataset before running: `sha256sum week1/penguins.csv` (macOS: `shasum -a 256 week1/penguins.csv`).

## License

Code is released under the [MIT License](LICENSE). Datasets keep their own licenses, listed above.
