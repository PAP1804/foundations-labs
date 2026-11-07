# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 1, Day 3: the Day 2 answers as functions (stdlib csv only).

One function, one job, named for what it returns. Same three questions:
  1. How many penguins of each species are there?
  2. How many rows have a missing value, per column?
  3. Which species has the most rows with a missing value?
"""

import csv
import sys
from pathlib import Path

# Default to the CSV next to this script, so it runs from any folder.
DEFAULT_CSV = Path(__file__).resolve().parent / "penguins.csv"

# Values treated as "missing". This file uses "NA"; other copies leave the cell blank.
MISSING = {"", "NA", "NaN", "nan", "null", "None"}


def is_missing(value):
    """Return True if a single cell value counts as missing."""
    return value is None or value.strip() in MISSING


def has_missing(row):
    """Return True if any cell in the row is missing."""
    return any(is_missing(value) for value in row.values())


def read_rows(path):
    """Return (column names, list of row dicts) from a CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def count_species(rows):
    """Return {species: number of rows}."""
    counts = {}
    for row in rows:
        species = row["species"]
        if species in counts:
            counts[species] += 1
        else:
            counts[species] = 1
    return counts


def missing_per_column(rows, columns):
    """Return {column: number of rows where that column is missing}."""
    counts = {}
    for column in columns:
        count = 0
        for row in rows:
            if is_missing(row[column]):
                count += 1
        counts[column] = count
    return counts


def missing_rows_per_species(rows):
    """Return {species: number of rows with any missing value}, including zeros."""
    counts = {species: 0 for species in count_species(rows)}
    for row in rows:
        if has_missing(row):
            counts[row["species"]] += 1
    return counts


def species_most_missing(missing_counts):
    """Return (sorted list of species tied for the most missing rows, that count)."""
    top = max(missing_counts.values(), default=0)
    leaders = sorted(s for s, n in missing_counts.items() if n == top)
    return leaders, top


def format_counts(counts, keys, width):
    """Return the counts as aligned report lines, in the order of keys."""
    return [f"   {key:<{width}} {counts[key]:>4}" for key in keys]


def format_leaders(leaders, top):
    """Return the one-line verdict for question 3."""
    if top == 0:
        return "   No species has missing values."
    if len(leaders) == 1:
        return f"   Most missing: {leaders[0]} ({top} rows)"
    return f"   Tied for most missing: {', '.join(leaders)} ({top} rows each)"


def main(path=DEFAULT_CSV):
    columns, rows = read_rows(path)
    species_counts = count_species(rows)
    column_counts = missing_per_column(rows, columns)
    species_missing = missing_rows_per_species(rows)
    leaders, top = species_most_missing(species_missing)

    lines = [
        "Columns: " + ", ".join(columns),
        f"Total rows: {len(rows)}",
        "",
        "1. Penguins per species:",
        *format_counts(species_counts, sorted(species_counts), 10),
        "",
        "2. Rows with a missing value, per column:",
        *format_counts(column_counts, columns, 18),
        "",
        "3. Rows with any missing value, per species:",
        *format_counts(species_missing, sorted(species_missing), 10),
        format_leaders(leaders, top),
    ]
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
