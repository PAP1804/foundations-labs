# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 2, Day 3: publish the CSV answers as CSV files (stdlib csv and os only).

Run from the repo root so the relative paths resolve:
    python week2/day3.py

Reused functions are copied, not imported: week2/day2.py calls main() at import
time (no __main__ guard), so importing it would run that program first.
"""

import csv
import os

DATA_PATH = os.path.join("week1", "penguins.csv")
SPECIES_PATH = os.path.join("week2", "species_counts.csv")
MISSING_PATH = os.path.join("week2", "missing_per_column.csv")

# Missing values in this file: blank cells and the text "NA" (the Wednesday / Day 2 fix).
MISSING = ("", "NA")

# Week 1 verified figures: the known answers every output is checked against.
EXPECTED_SPECIES = {"Adelie": 152, "Chinstrap": 68, "Gentoo": 124}
EXPECTED_MISSING = {
    "bill_depth_mm": 2,
    "bill_length_mm": 2,
    "body_mass_g": 2,
    "flipper_length_mm": 2,
    "sex": 11,
}


# --- Reused (copied from week2/day2.py, bugs fixed) ---------------------------

def read_rows(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def count_species(rows):
    counts = {}
    for row in rows:
        species = row["species"]
        counts[species] = counts.get(species, 0) + 1
    return counts


# --- Reused (copied from week1/day4.py; counter pattern only, so columns with no
# missing values are left out, matching the published file) --------------------

def missing_per_column(rows):
    """Return a dict: column -> number of rows where that column is missing ("" or "NA")."""
    counts = {}
    for row in rows:
        for column, value in row.items():
            if value in MISSING:
                counts[column] = counts.get(column, 0) + 1
    return counts


# --- New: writers ---------------------------------------------------------------

def write_species_counts(counts, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species", "count"])
        writer.writeheader()
        for species, count in sorted(counts.items()):
            writer.writerow({"species": species, "count": count})


def write_missing_per_column(missing, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["column", "missing_count"])
        writer.writeheader()
        for column, count in sorted(missing.items()):
            writer.writerow({"column": column, "missing_count": count})


# --- New: round-trip check --------------------------------------------------------

def read_back(path, key_field, count_field):
    """Return {key: int(count)} read from a published CSV with DictReader."""
    with open(path, newline="") as f:
        return {row[key_field]: int(row[count_field]) for row in csv.DictReader(f)}


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Can't find {DATA_PATH} from {os.getcwd()}. Run this from the repo root: python week2/day3.py")
        return

    rows = read_rows(DATA_PATH)
    species_counts = count_species(rows)
    missing = missing_per_column(rows)

    write_species_counts(species_counts, SPECIES_PATH)
    write_missing_per_column(missing, MISSING_PATH)
    print(f"Wrote {SPECIES_PATH} and {MISSING_PATH} from {len(rows)} rows")

    # Round trip: read both files back and compare with the known answers.
    species_back = read_back(SPECIES_PATH, "species", "count")
    missing_back = read_back(MISSING_PATH, "column", "missing_count")
    print("species_counts.csv matches Week 1:", species_back == EXPECTED_SPECIES)
    print("missing_per_column.csv matches Week 1:", missing_back == EXPECTED_MISSING)
    print("species total equals row count:", sum(species_back.values()) == len(rows))


if __name__ == "__main__":
    main()
