# Week 1 — Python foundations

Phase 0, Week 1 of the Applied Analytics, ML & AI track (Nov 2026).

## What this week covers

1. Variables and types — assignment, rebinding vs mutation, `==` vs `is`
2. Control flow — conditionals, loops, comprehensions
3. Functions — definitions, scope, return values (`None` and why it matters)
4. Data structures — lists, dicts, tuples, aliasing, counting patterns + Week 1 synthesis

## Progress

- **Day 1 — done.** `day1.py` (stdlib `csv` only): prints column names and the first 5 rows of the Palmer Penguins CSV, counts total rows and rows with any missing value. Result: 344 rows, 11 with a missing value. Details below.
- Day 2 — control flow: extend the CSV program (count per species, missing per column, species with most missing rows). Outstanding.
- Day 3 — functions: refactor into `read_rows` / `count_species` / `missing_per_column` / `species_most_missing` / `main`. Outstanding.
- Day 4 — data structures: same three CSV questions with the right structures (counter pattern, tuple return). Outstanding.

## Day 1 — first look at the data

Run from the repo root (the script finds `penguins.csv` next to itself):

```bash
python3 week1/day1.py
```

Output:

```
Columns: species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, year

First 5 rows:
['Adelie', 'Torgersen', '39.1', '18.7', '181', '3750', 'male', '2007']
['Adelie', 'Torgersen', '39.5', '17.4', '186', '3800', 'female', '2007']
['Adelie', 'Torgersen', '40.3', '18', '195', '3250', 'female', '2007']
['Adelie', 'Torgersen', 'NA', 'NA', 'NA', 'NA', 'NA', '2007']
['Adelie', 'Torgersen', '36.7', '19.3', '193', '3450', 'female', '2007']

Total rows: 344
Rows with any missing value: 11
```

### Takeaways

- **`csv` returns everything as strings.** `'39.1'` and `'181'` are text until converted, so any arithmetic needs `float()` / `int()` first.
- **Missing values are the text `NA`, not empty cells.** A check like `if value == ""` finds zero missing rows here. The script treats blanks, `NA`, `NaN`, `null` and `None` as missing, so it also works on other copies of the dataset.
- **Missing data comes in two patterns.** 9 rows are missing only `sex`; 2 rows are missing every measurement and `sex`. Dropping all 11 rows loses real measurements from the 9, which matters for later analysis.
- **Read the header separately.** `next(reader)` takes the column names off first, so the row count (344) excludes the header line (the file has 345 lines).
