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
| 2 | Control flow: counts per species, missing per column | Outstanding |
| 3 | Functions: refactor the CSV program into functions | Outstanding |
| 4 | Data structures: counter pattern, tuple returns, week synthesis | Outstanding |

## Running

Requires Python 3 (`python3 --version`; install from https://www.python.org/downloads/). Week 1 uses the standard library only.

Run any lab from the repo root:

```bash
python3 week1/day1.py
```

## Data

| Dataset | File | Source | License | Used in |
|---------|------|--------|---------|---------|
| Palmer Penguins | [`week1/penguins.csv`](week1/penguins.csv) | Gorman, Williams & Fraser (2014), via [palmerpenguins](https://github.com/allisonhorst/palmerpenguins) | CC0 | Week 1 |

## License

Code is released under the [MIT License](LICENSE). Datasets keep their own licenses, listed above.
