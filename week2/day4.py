# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 2, Day 4: harden the CSV program against bad input (stdlib csv, os and sys only).

Run from the repo root; the input path is optional:
    python week2/day4.py                            # week1/penguins.csv
    python week2/day4.py week2/penguins_corrupt.csv

Extends the Day 3 functions (copied from week2/day3.py):
  read_rows          - a missing file prints an error to stderr and exits with code 1.
  count_species      - rows whose species is absent, "" or "NA" are logged to stderr and
                       skipped; returns (counts, skipped) instead of counts.
  missing_per_column - unchanged.
New: check_counts - the counts must sum to rows read minus rows skipped, or nothing is printed.
"""

import csv
import os
import sys

DEFAULT_PATH = os.path.join("week1", "penguins.csv")

# Missing values in this file: blank cells and the text "NA".
MISSING = ("", "NA")


def read_rows(path):
    """Return the CSV's rows as a list of dicts; exit with code 1 if the file is missing."""
    try:
        f = open(path, newline="")
    except FileNotFoundError:
        print(f"error: no such file: {path}", file=sys.stderr)
        raise SystemExit(1)
    with f:
        return list(csv.DictReader(f))


def count_species(rows):
    """Return (counts, skipped): species -> count, and how many rows had no usable species.

    A row with no species column (KeyError) or a missing species value ("" or "NA")
    is logged to stderr, counted as skipped, and left out of the counts.
    """
    counts = {}
    skipped = 0
    for row in rows:
        try:
            species = row["species"]
        except KeyError:
            print(f"skipped a row with no species column: {row}", file=sys.stderr)
            skipped += 1
            continue
        if species is None or species.strip() in MISSING:
            print(f"skipped a row with missing species: {row}", file=sys.stderr)
            skipped += 1
            continue
        counts[species] = counts.get(species, 0) + 1
    return counts, skipped


def missing_per_column(rows):
    """Return a dict: column -> number of rows where that column is missing ("" or "NA")."""
    counts = {}
    for row in rows:
        for column, value in row.items():
            if value in MISSING:
                counts[column] = counts.get(column, 0) + 1
    return counts


def check_counts(counts, rows_read, skipped):
    if sum(counts.values()) != rows_read - skipped:
        raise ValueError(
            f"counts sum to {sum(counts.values())} but {rows_read - skipped} rows were kept"
        )


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    rows = read_rows(path)
    counts, skipped = count_species(rows)
    check_counts(counts, len(rows), skipped)  # raises before anything is published

    print(dict(sorted(counts.items())))
    print(f"rows read: {len(rows)} | skipped: {skipped}")
    print(f"missing per column: {dict(sorted(missing_per_column(rows).items()))}")


if __name__ == "__main__":
    main()
