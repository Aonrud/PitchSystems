#!/bin/python
"""
Convert from a CSV format to a Django fixture JSON file.
"""

from csv import DictReader
import sys
import json
from pathlib import Path
import math


def usage() -> None:
    print("Usage: csv2django CSVFILE MODEL_NAME")

# Allowed deviation between cents value given and an interval to be considered equal
CENTS_TOLERANCE = 0.0005
# Can start with higher id when merging with an existing list
PK_start = 86

interval_file = open(
    (Path(__file__).parent / "../pitch-systems-api/fixtures/interval.json").resolve(),
    "r",
)
intervals = json.load(interval_file)

def find_intervals(value: str) -> list:
    """
    Find interval IDs by cents value.
    """
    cents_list = value.split(",")
    ids = []

    for cents in cents_list:
        int_id = next(
                    (
                        interval["pk"]
                        for interval in intervals
                        # Match on isclose() to allow for rounding/float imprecision.
                        if math.isclose(
                            interval["fields"]["cents"],
                            float(cents),
                            abs_tol=CENTS_TOLERANCE,
                        )
                    ),
                    None
                )
        ids.append(int_id)
    return ids


def type_csv_row(row: dict) -> dict:
    '''
    Convert string values of a dict to integer, float or None types
    '''
    for col in row.items():

        # Special case of intervals - search the interval fixtures for matches and get the IDs
        if col[0] in ["intervals", "interval"]:
            print(f"{col[1]} matches {find_intervals(col[1])}")
            match = find_intervals(col[1])
            if col[0] == "interval":
                match = match[0]
            row[col[0]] = match
        else:
            # Null values
            if len(col[1]) == 0 or col[1].lower() in ( "null", "none"):
                row[col[0]] = None

            # Numeric values - Try int, then float
            try:
                row[col[0]] = int(col[1])
            except:
                try:
                    row[col[0]] = float(col[1])
                except:
                    continue
    return row

args = sys.argv
if len(args) < 3:
    usage()

csv_file = args[1]
output = Path(csv_file).stem + ".json"
model = args[2]
fixtures = []
i = PK_start

with open(csv_file) as data:
    reader = DictReader(data)
    for row in reader:
        row = type_csv_row(row)
        fixtures.append({"model": model, "pk": i, "fields": row})
        i += 1

out_file = open(output, "x")
out_file.write(json.dumps(fixtures))
out_file.close()
