import csv

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

def species_most_missing(rows):
    missing = {}
    for row in rows:
        if any(v in ("", "NA") for v in row.values()):  # this file writes missing as "NA"
            s = row["species"]
            missing[s] = missing.get(s, 0) + 1
    if not missing:  # no row has a missing value: no species to name
        return None
    return max(missing, key=missing.get)

def main():
    rows = read_rows("week1/penguins.csv")
    print(count_species(rows))
    print(species_most_missing(rows))

main()
