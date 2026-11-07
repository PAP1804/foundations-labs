# Week 1 — Python foundations

Phase 0, Week 1 of the Applied Analytics, ML & AI track (Nov 2026).

## What this week covers

1. Variables and types — assignment, rebinding vs mutation, `==` vs `is`
2. Control flow — conditionals, loops, comprehensions
3. Functions — definitions, scope, return values (`None` and why it matters)
4. Data structures — lists, dicts, tuples, aliasing, counting patterns + Week 1 synthesis

## Progress

- **Day 1 — done.** `day1.py` (stdlib `csv` only): prints column names and the first 5 rows of the Palmer Penguins CSV, counts total rows and rows with any missing value. Result: 344 rows, 11 with a missing value. Details below.
- **Day 2 — done.** `day2.py`: count per species, missing per column, species with most missing rows. Result: Adelie 152, Chinstrap 68, Gentoo 124; `sex` missing in 11 rows; Adelie has the most missing rows (6). Details below.
- **Day 3 — done.** `day3.py`: the Day 2 program refactored into one-job functions (`read_rows`, `count_species`, `missing_per_column`, `missing_rows_per_species`, `species_most_missing`, `main`, plus small helpers). Output identical to Day 2. Details below.
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

## Day 2 — control flow: species and missing counts

```bash
python3 week1/day2.py
```

Output:

```
Columns: species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, year
Total rows: 344

1. Penguins per species:
   Adelie      152
   Chinstrap    68
   Gentoo      124

2. Rows with a missing value, per column:
   species               0
   island                0
   bill_length_mm        2
   bill_depth_mm         2
   flipper_length_mm     2
   body_mass_g           2
   sex                  11
   year                  0

3. Rows with any missing value, per species:
   Adelie        6
   Chinstrap     0
   Gentoo        5
   Most missing: Adelie (6 rows)
```

### Takeaways

- **A dict keyed by species beats `if`/`elif` on names.** The `if species in counts: ... else: ...` pattern finds the species from the data, so nothing is hard-coded and a fourth species would just appear.
- **Per-column and per-row counts answer different questions.** Column counts add to 19, but only 11 rows are affected, because the 2 empty rows are missing 5 values each. `sex` alone accounts for all 11 rows.
- **"Most" depends on counts vs rates.** Adelie has the most missing rows (6 of 152 = 3.9%), but Gentoo's rate is slightly higher (5 of 124 = 4.0%). Chinstrap has none. With so few, the difference means little, but the question needs to say which one it means.
- **Handle ties and the zero case explicitly.** `max()` alone silently picks one winner; the script lists every species tied at the top and says so when nothing is missing.
- **Sanity-check totals.** 152 + 68 + 124 = 344 and 6 + 0 + 5 = 11 both match the Day 1 counts, which confirms no rows were dropped or double-counted.

## Day 3 — functions: one function, one job

```bash
python3 week1/day3.py
```

Output: identical to Day 2 (checked with `diff`), shown above.

| Function | Returns |
|----------|---------|
| `is_missing(value)` | whether one cell counts as missing |
| `has_missing(row)` | whether any cell in a row is missing |
| `read_rows(path)` | `(columns, rows)` from the CSV |
| `count_species(rows)` | `{species: count}` |
| `missing_per_column(rows, columns)` | `{column: missing count}` |
| `missing_rows_per_species(rows)` | `{species: rows with any missing value}` |
| `species_most_missing(counts)` | `(species tied at the top, their count)` |
| `format_counts(counts, keys, width)` | aligned report lines |
| `format_leaders(leaders, top)` | the question-3 verdict line |
| `main(path)` | nothing: wires the functions together and prints |

### Takeaways

- **The planned `species_most_missing` did two jobs.** Counting missing rows per species and picking the top are separate, so they became `missing_rows_per_species` and `species_most_missing`. Now the ranking can be reused on any `{name: count}` dict, e.g. rates instead of counts.
- **Calculating and printing are split.** The counting functions return data and never print; `format_*` functions turn data into text; only `main` prints. That makes each answer testable on its own, e.g. `species_most_missing({"A": 2, "B": 2})` returns `(["A", "B"], 2)`.
- **Return a tuple when the answer has two parts.** `species_most_missing` returns both the leaders and the count, so the caller doesn't recompute `max()`.
- **A refactor should not change results.** Diffing Day 3's output against Day 2's confirmed the behaviour is unchanged.
- **Edge cases are easier to check in small functions.** `max(..., default=0)` keeps `species_most_missing({})` from crashing on an empty file.
