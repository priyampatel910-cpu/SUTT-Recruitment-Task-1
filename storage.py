import csv

with open(
    "data/cabs.csv",
    newline="",
    encoding="utf-8-sig"
) as cab_file:
    csv_reader = csv.DictReader(cab_file)

    for cab_row in csv_reader:
        print(cab_row)