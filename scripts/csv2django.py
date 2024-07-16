#!/bin/python
"""
Convert from a CSV format to a Django fixture JSON file.
"""

from csv import DictReader
import sys
import json
from pathlib import Path


def usage() -> None:
    print("Usage: csv2django CSVFILE MODEL_NAME")

def type_csv_row(row: dict) -> dict:
    '''
    Convert string values of a dict to integer, float or None types
    '''
    for col in row.items():

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
i = 1

with open(csv_file) as data:
    reader = DictReader(data)
    for row in reader:
        row = type_csv_row(row)
        fixtures.append({"model": model, "pk": i, "fields": row})
        i += 1

out_file = open(output, "x")
out_file.write(json.dumps(fixtures))
out_file.close()
