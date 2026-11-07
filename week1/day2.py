# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 1, Day 2: control flow over the Palmer Penguins CSV (stdlib csv only).

Answers three questions:
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
    return value is None or value.strip() in MISSING


def main(path=DEFAULT_CSV):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)

    print("Columns:", ", ".join(columns))
    print("Total rows:", len(rows))

    # 1. Penguins per species: a dict keyed by species, so new species need no code change.
    species_counts = {}
    for row in rows:
        species = row["species"]
        if species in species_counts:
            species_counts[species] += 1
        else:
            species_counts[species] = 1

    print()
    print("1. Penguins per species:")
    for species in sorted(species_counts):
        print(f"   {species:<10} {species_counts[species]:>4}")

    # 2. Missing values per column: loop over the columns, count missing cells in each.
    missing_per_column = {}
    for column in columns:
        count = 0
        for row in rows:
            if is_missing(row[column]):
                count += 1
        missing_per_column[column] = count

    print()
    print("2. Rows with a missing value, per column:")
    for column in columns:
        print(f"   {column:<18} {missing_per_column[column]:>4}")

    # 3. Rows with any missing value, per species; then pick the largest.
    missing_rows_by_species = {species: 0 for species in species_counts}
    for row in rows:
        if any(is_missing(value) for value in row.values()):
            missing_rows_by_species[row["species"]] += 1

    print()
    print("3. Rows with any missing value, per species:")
    for species in sorted(missing_rows_by_species):
        print(f"   {species:<10} {missing_rows_by_species[species]:>4}")

    top_count = max(missing_rows_by_species.values())
    leaders = sorted(s for s, n in missing_rows_by_species.items() if n == top_count)
    if top_count == 0:
        print("   No species has missing values.")
    elif len(leaders) == 1:
        print(f"   Most missing: {leaders[0]} ({top_count} rows)")
    else:
        print(f"   Tied for most missing: {', '.join(leaders)} ({top_count} rows each)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
