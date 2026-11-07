"""Week 1, Day 1: first look at the Palmer Penguins CSV using only the stdlib csv module."""

import csv
import sys

# Values treated as "missing". This file uses "NA"; other copies leave the cell blank.
MISSING = {"", "NA", "NaN", "nan", "null", "None"}


def is_missing(value):
    return value is None or value.strip() in MISSING


def main(path="penguins.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        print("Columns:", ", ".join(header))
        print()
        print("First 5 rows:")

        total_rows = 0
        rows_with_missing = 0

        for row in reader:
            if not row:  # skip blank lines
                continue
            total_rows += 1

            if total_rows <= 5:
                print(row)

            # A short row also counts as missing data.
            if len(row) < len(header) or any(is_missing(v) for v in row):
                rows_with_missing += 1

    print()
    print("Total rows:", total_rows)
    print("Rows with any missing value:", rows_with_missing)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "penguins.csv")
