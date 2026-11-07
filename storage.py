import csv
from pathlib import Path
from models import Cab
from validator import parse_name, parse_seats,parse_destination, parse_timeslot

def load_cabs_csv(csv_path):
    loaded_cabs = []

    try:
        with open(
            csv_path,
            newline="",
            encoding="utf-8-sig"
        ) as cab_file:
            csv_reader = csv.DictReader(cab_file)

            if csv_reader.fieldnames is None:
                print("The cab CSV file is empty.")

            missing_colums = [
                column for column in [
                    "driver_name",
                    "seats",
                    "destination",
                    "time_slot"
                ] if column not in csv_reader.fieldnames
            ]

            if missing_columns:
                print("This file is missing columns : " + ", ".join(missing_columns))

                return loaded_cabs

    except FileNotFoundError:
        print(f"Could not find the file at {csv_path}")

    if not loaded_cabs:
        print("No cabs were loaded")

    return loaded_cabs