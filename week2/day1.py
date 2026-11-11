# Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.
# Missing: written as the text "NA", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).
# Question: is missing data spread evenly across species, or concentrated in one?
"""Week 2, Day 1: the Week 1 answers written to a report file (stdlib csv and os only).

Run from the repo root so the relative paths resolve:
    python week2/day1.py
"""

import csv
import os

DATA_PATH = os.path.join("week1", "penguins.csv")
REPORT_PATH = os.path.join("week2", "report.txt")

# Values treated as "missing". This file uses "NA"; other copies leave the cell blank.
MISSING = {"", "NA", "NaN", "nan", "null", "None"}

# The 3-line cleaning log, written into the report as well as kept above as comments.
CLEANING_LOG = [
    "Contents: 344 Palmer Penguins (3 species, 3 islands, 2007-2009), 8 columns: species, island, 4 body measurements, sex, year.",
    "Missing: written as the text \"NA\", never a blank cell; 11 rows affected (9 lack only sex, 2 lack all 4 measurements and sex).",
    "Question: is missing data spread evenly across species, or concentrated in one?",
]


def is_missing(value):
    """Return True if a single cell value counts as missing."""
    return value is None or value.strip() in MISSING


# --- Week 1 functions (from week1/day4.py) ---------------------------------

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
    (None, 0) if no row has a missing value."""
    counts = {}
    for row in rows:
        if any(is_missing(value) for value in row.values()):
            counts[row["species"]] = counts.get(row["species"], 0) + 1
    if not counts:
        return (None, 0)
    # Sort by count descending, then name ascending, so ties are deterministic.
    return min(counts.items(), key=lambda item: (-item[1], item[0]))


# --- New in Week 2 -----------------------------------------------------------

def write_report(rows, path):
    """Write the three answers and the cleaning log to path as plain text, one fact per line."""
    species_counts = count_species(rows)
    column_counts = missing_per_column(rows)
    species, count = species_most_missing(rows)

    with open(path, "w", encoding="utf-8") as f:
        f.write("Penguins report\n")
        f.write(f"Source: {DATA_PATH}\n")
        f.write(f"Total rows: {len(rows)}\n")
        f.write("\n")

        f.write("Penguin species counts\n")
        for name, n in sorted(species_counts.items()):
            f.write(f"{name}: {n}\n")
        f.write("\n")

        f.write("Missing values per column\n")
        for column, n in column_counts.items():
            f.write(f"{column}: {n}\n")
        f.write("\n")

        if species is None:
            f.write("Species with most missing rows: none (no missing values)\n")
        else:
            f.write(f"Species with most missing rows: {species} ({count})\n")
        f.write("\n")

        f.write("Cleaning log\n")
        for line in CLEANING_LOG:
            f.write(f"{line}\n")


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Can't find {DATA_PATH} from {os.getcwd()}. Run this from the repo root: python week2/day1.py")
        return
    rows = read_rows(DATA_PATH)
    write_report(rows, REPORT_PATH)
    print(f"Wrote {REPORT_PATH} ({len(rows)} rows read from {DATA_PATH})")


if __name__ == "__main__":
    main()
