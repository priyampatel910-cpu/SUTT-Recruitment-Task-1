import csv
from pathlib import Path
from models import Cab
from pool import CabPool
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

            for line_number, cab_row in enumerate(csv_reader, start = 2):
                try:
                    driver_name = parse_name(cab_row["driver_name"])
                    seat_count = parse_seats(cab_row["seats"])
                    destination = parse_destination(cab_row["destination"])
                    time_slot = parse_timeslot(cab_row["time_slot"])

                    new_cab = Cab(
                        driver_name,
                        seat_count,
                        destination,
                        time_slot
                    )

                    loaded_cabs.append(new_cab)

                except ValueError as error:
                    print(
                        f"Cab file line {line_number} skipped: {error}"
                    )

    except FileNotFoundError:
        print(f"Could not find the file at {csv_path}")

    if not loaded_cabs:
        print("No cabs were loaded")

    return loaded_cabs