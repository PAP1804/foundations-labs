# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 1, Day 4: the three CSV answers built with the structures each one wants (stdlib csv only).

  rows                 -> list of dicts       (one dict per penguin)
  count_species        -> dict  species -> count   (counter pattern)
  missing_per_column   -> dict  column  -> count
  species_most_missing -> tuple (species, count)
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


def read_rows(path):
    """Return the CSV's rows as a list of dicts (column name -> value)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_species(rows):
    """Return a dict: species -> number of rows."""
    counts = {}
    for row in rows:
        counts[row["species"]] = counts.get(row["species"], 0) + 1
    return counts


def missing_per_column(rows):
    """Return a dict: column -> number of rows where that column is missing."""
    counts = {column: 0 for column in (rows[0] if rows else {})}
    for row in rows:
        for column, value in row.items():
            if is_missing(value):
                counts[column] = counts.get(column, 0) + 1
    return counts


def species_most_missing(rows):
    """Return a tuple (species, count): the species with the most rows containing
    a missing value, and how many. Ties go to the alphabetically first species;
    (None, 0) if there are no rows."""
    counts = {}
    for row in rows:
        if any(is_missing(value) for value in row.values()):
            counts[row["species"]] = counts.get(row["species"], 0) + 1
    if not counts:
        return (None, 0)
    # Sort by count descending, then name ascending, so ties are deterministic.
    return min(counts.items(), key=lambda item: (-item[1], item[0]))


def main(path=DEFAULT_CSV):
    rows = read_rows(path)
    print("Total rows:", len(rows))

    print()
    print("1. Penguins per species:")
    species_counts = count_species(rows)
    for species, count in sorted(species_counts.items()):
        print(f"   {species:<10} {count:>4}")

    print()
    print("2. Rows with a missing value, per column:")
    for column, count in missing_per_column(rows).items():
        print(f"   {column:<18} {count:>4}")

    print()
    print("3. Species with the most rows containing a missing value:")
    species, count = species_most_missing(rows)
    if species is None:
        print("   No rows have missing values.")
    else:
        share = count / species_counts[species]
        print(f"   {species}: {count} rows ({share:.1%} of {species_counts[species]})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
