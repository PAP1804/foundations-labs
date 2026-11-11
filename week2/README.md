# Week 2 — files and paths

Phase 0, Week 2 of the Applied Analytics, ML & AI track (Nov 2026).

## Progress

- **Day 1 — done.** `day1.py` (stdlib `csv` and `os` only): reuses the four Week 1 functions and adds `write_report`, which writes the three answers and the cleaning log to `week2/report.txt`. Details below.

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
