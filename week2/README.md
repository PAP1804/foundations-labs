# Week 2 — files and paths

Phase 0, Week 2 of the Applied Analytics, ML & AI track (Nov 2026).

## Progress

- **Day 1 — done.** `day1.py` (stdlib `csv` and `os` only): reuses the four Week 1 functions and adds `write_report`, which writes the three answers and the cleaning log to `week2/report.txt`. Details below.
- **Day 2 — done.** `day2.py`: a deliberately broken copy of the Week 1 program, debugged one fix at a time. Four bugs fixed (three planted, one hidden behind them). Details below.
- **Day 3 — done.** `day3.py`: publishes species counts and missing-per-column as CSV files with `DictWriter`, then reads them back with `DictReader` and checks them against the Week 1 figures. Details below.
- **Day 4 — done.** `day4.py`: the Day 3 functions hardened against bad input: a missing file exits with code 1, rows with no species are logged and skipped, and `check_counts` refuses to print counts that don't add up. Tested on `penguins_corrupt.csv`. Details below.

## Day 1 — answers written to a report file

Run from the repo root, so the relative paths `week1/penguins.csv` and `week2/report.txt` resolve:

```bash
python week2/day1.py
```

Terminal output:

```
Wrote week2/report.txt (344 rows read from week1/penguins.csv)
```

[`report.txt`](report.txt):

```
Penguins report
Source: week1/penguins.csv
Total rows: 344

Penguin species counts
Adelie: 152
Chinstrap: 68
Gentoo: 124

Missing values per column
species: 0
island: 0
bill_length_mm: 2
bill_depth_mm: 2
flipper_length_mm: 2
body_mass_g: 2
sex: 11
year: 0

Species with most missing rows: Adelie (6)

Cleaning log
Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
Question: is missing data spread evenly across species, or concentrated in one?
```

### Takeaways

- **Relative paths resolve against the current folder, not the script's.** From the repo root, `os.path.join("week1", "penguins.csv")` works; from inside `week2/` the same line looks for `week2/week1/penguins.csv`. `main()` checks with `os.path.exists` and prints `os.getcwd()` so the mistake is obvious instead of a traceback.
- **`f.write` adds no newline.** Unlike `print`, every line needs its own `"\n"`; the report's 25 lines all end with one, including the last.
- **`"w"` replaces the file.** Each run rewrites `report.txt` from scratch, so the committed report always matches the code that produced it.
- **`os.path.join` builds paths portably.** It uses `/` on Linux and macOS and `\` on Windows, so the same script runs everywhere.
- **Reused code gives the same answers.** The four functions copied from `week1/day4.py` produce 152 / 68 / 124, 11 missing `sex`, and Adelie with 6, matching Week 1.

## Day 2 — debugging: one fix at a time

```bash
python week2/day2.py
```

Output after the last fix:

```
{'Adelie': 152, 'Gentoo': 124, 'Chinstrap': 68}
Adelie
```

Each fix was followed by a run:

| Run | Error (last line of the traceback) | Where | Fix |
|-----|-------------------------------------|-------|-----|
| 1 | `KeyError: 'specie'` | `count_species`, line 11 | `row["species"]`: the column is `species` |
| 2 | `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | `count_species`, line 12 | `counts.get(species, 0)`: `get` returns `None` for a new key without a default |
| 3 | `ValueError: max() iterable argument is empty` | `species_most_missing`, line 21 | return `None` when no row has a missing value |
| 4 | no error, but prints `None` instead of `Adelie` | `species_most_missing`, line 18 | treat `""` and `"NA"` as missing |

### Takeaways

- **Read the last line, then the bottom frame.** The last line names the error type and value; the bottom frame names the file, line and function. Together they point straight at the fix for runs 1–3.
- **One fix per run shows what each fix did.** Fixing bug 1 revealed bug 2 on the very next line; fixing bug 3 revealed that the program ran but gave the wrong answer, which an all-at-once fix would have hidden.
- **Bug 3 was supposed to fire only on data with no missing rows, yet it fired on penguins.** The check `v == ""` never matches this file's `NA`, so to this program penguins *had* no missing rows. That made a fourth, silent bug: the same `""`-vs-`NA` gotcha as Week 1 Day 1.
- **"Runs clean" is not "correct".** Run 4 had no traceback but printed `None`; only checking against known answers (152 / 68 / 124 and Adelie) caught it.
- **`None` for "no answer", not `("none", 0)`.** The function returns a species name, so `None` keeps the return type consistent; a tuple only for the empty case would change the type, and `"none"` could be mistaken for a species. Tested with `[{"species": "Adelie"}, {"species": "Gentoo"}]`, which returns `None`.

## Day 3 — publishing the answers as CSV

```bash
python week2/day3.py
```

Output:

```
Wrote week2/species_counts.csv and week2/missing_per_column.csv from 344 rows
species_counts.csv matches Week 1: True
missing_per_column.csv matches Week 1: True
species total equals row count: True
```

[`species_counts.csv`](species_counts.csv):

```
species,count
Adelie,152
Chinstrap,68
Gentoo,124
```

[`missing_per_column.csv`](missing_per_column.csv):

```
column,missing_count
bill_depth_mm,2
bill_length_mm,2
body_mass_g,2
flipper_length_mm,2
sex,11
```

### Takeaways

- **The round trip is the check.** Writing a file proves nothing; reading it back with `DictReader` and comparing with the known answers (152 / 68 / 124, and the five missing counts) does. A wrong count like Adelie 151 opens cleanly and has a header, so only the known answer catches it.
- **Counter pattern vs pre-filled zeros changes the output.** Week 1's `missing_per_column` started every column at 0; here only columns with a missing value get a key, so `species`, `island` and `year` are left out, as the published file expects.
- **`DictReader` gives back strings.** `"152"` has to become `int("152")` before comparing with `152`, or every check fails.
- **`newline=""` and `\r\n`.** `csv` writes `\r\n` line endings by default; opening with `newline=""` stops Python adding a second `\r` on Windows. The files match the expected contents byte for byte.
- **Copied, not imported.** `week2/day2.py` runs `main()` at import (no `__main__` guard), so importing its functions would run that program too. The guard is what makes a script safe to import.

## Day 4 — hardening: exceptions and skipped rows

`penguins_corrupt.csv` is `week1/penguins.csv` with two cells changed: row 1 (file line 2, an Adelie from Torgersen) has its species blanked, and row 277 (file line 278, a Chinstrap from Dream) has its species set to `NA`.

Corrupt run (stderr and stdout together):

```bash
python week2/day4.py week2/penguins_corrupt.csv
```

```
skipped a row with missing species: {'species': '', 'island': 'Torgersen', 'bill_length_mm': '39.1', 'bill_depth_mm': '18.7', 'flipper_length_mm': '181', 'body_mass_g': '3750', 'sex': 'male', 'year': '2007'}
skipped a row with missing species: {'species': 'NA', 'island': 'Dream', 'bill_length_mm': '46.5', 'bill_depth_mm': '17.9', 'flipper_length_mm': '192', 'body_mass_g': '3500', 'sex': 'female', 'year': '2007'}
{'Adelie': 151, 'Chinstrap': 67, 'Gentoo': 124}
rows read: 344 | skipped: 2
missing per column: {'bill_depth_mm': 2, 'bill_length_mm': 2, 'body_mass_g': 2, 'flipper_length_mm': 2, 'sex': 11, 'species': 2}
```

Clean run:

```bash
python week2/day4.py week1/penguins.csv
```

```
{'Adelie': 152, 'Chinstrap': 68, 'Gentoo': 124}
rows read: 344 | skipped: 0
missing per column: {'bill_depth_mm': 2, 'bill_length_mm': 2, 'body_mass_g': 2, 'flipper_length_mm': 2, 'sex': 11}
```

Missing file:

```
$ python week2/day4.py week2/nope.csv
error: no such file: week2/nope.csv        (exit code 1)
```

### Takeaways

- **A broken assumption fails loudly; bad data is counted.** A missing input file means the program can't do its job, so it stops with exit code 1 and names the file. A row with no species is data, so it is skipped, logged and counted, and the run goes on.
- **Errors go to stderr, results to stdout.** With `2>/dev/null` only the counts are left, so the results can be piped or saved without the skip messages mixed in.
- **The check turns "nothing crashed" into "the numbers add up".** 151 + 67 + 124 = 342 = 344 − 2, so the corrupt run passes honestly. `check_counts({"Adelie": 151}, 344, 2)` raises `ValueError: counts sum to 151 but 342 rows were kept`, and the program prints no counts.
- **`KeyError` and a missing value are different failures.** `DictReader` always gives every row a `species` key when the header has one, so the `KeyError` branch only fires for a file without that column; blank and `NA` values are the case that actually happened here. Both are tested.
- **`missing_per_column` now reports `species: 2`.** The corruption shows up in the existing per-column count too, which confirms the two skipped rows from a second direction.
