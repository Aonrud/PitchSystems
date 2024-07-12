#!/bin/python
'''
Convert from a CSV format to a Django fixture JSON file.
'''

from csv import DictReader
import sys
import json
from pathlib import Path


def usage():
    print("Usage: csv2django CSVFILE MODEL_NAME")

args = sys.argv
if (len(args) < 3):
    usage()

csv_file = args[1]
output = Path(csv_file).stem + ".json"
model = args[2]
fixtures = []
i = 1

with open(csv_file) as data:
    reader = DictReader(data)
    for row in reader:  
        fixtures.append({ "model": model, "pk": i, "fields": row })
        i+=1

out_file = open(output, 'x')
out_file.write(json.dumps(fixtures))
out_file.close()