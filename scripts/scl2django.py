#!/bin/python
import sys
import math
from pathlib import Path
import json
from decimal import Decimal
from pprint import pprint

"""
Read a directory of scl files and parse them all as Django fixtures for the pitches.scale model.
"""

def usage() -> None:
    print("Usage: scl2django SCL_DIRECTORY")

class SclParser:
    """Class for parsing .scl files into Django fixtures
        see: https://www.huygens-fokker.org/scala/scl_format.html
    """

    # Allowed deviation between cents value given and an interval to be considered equal
    CENTS_TOLERANCE = 0.0005

    intervals: list
    sys_map: dict
    missing: list

    def __init__(self, intervals: list, sys_map: dict):
        self.intervals = intervals
        self.sys_map = sys_map
        self.missing = []

    def parse(self, filename: str) -> object:
        """Parse an scl file and return an object

        Args:
            filename (str):

        Returns:
            object:
        """

        scl = open(filename, "r")

        # After title and interval count are read, all subsequent lines are intervals
        scale = {
            "name": "",
            "count": 0,
            "intervals": [],
        }

        try:
            # TODO: For robustness, check that the count matches the number of intervals received.
            for line in scl:
                # Ignore comment lines
                if line[0] == "!":
                    continue

                #Truncate end of line comments
                if "!" in line:
                    line = line.partition("!")[0]

                # .scl files don't include a description. However, the Scala set often contains descriptive information in the title. Take post-comma content as description.
                if scale["name"] == "":
                    scale["name"] = line.strip()
                elif scale["count"] == 0:
                    scale["count"] = int(line)
                else:
                    scale["intervals"].append(self.get_interval_id(line))

            # Count isn't part of Scale model
            del scale["count"]

            # Scl doesn't provide description beyond a title
            scale["description"] = ""

            # If file is mapped to a system, add the system
            key = filename.name
            if key in sys_map:
                scale["system"] = int(sys_map[key])

            return scale
        except UnicodeDecodeError:
            print(f"Non-unicode file {filename}")
        except ValueError:
            print(f"Bad value: {line}")


    def get_interval_id(self, text: str) -> int:
        """
        Get the interval ID matching an scl interval line
        """

        # Drop newlines
        text = text.rstrip()

        # Drop "cents" -- seems to be appended in some files
        if "cents" in text:
            text = text.partition("cents")[0].strip()

        # An integer without decimal point is assumed to be X/1 ratio
        if text.find(".") == -1 and text.find("/") == -1:
            text += "/1"

        int_id = -1
        cents_val = text

        # Handle ratios
        if text.find("/") != -1:
            parts = text.split("/")
            int_id = next(
                (
                    interval["pk"]
                    for interval in intervals
                    if interval["fields"]["ratio_numerator"] == int(parts[0])
                    and interval["fields"]["ratio_denominator"] == int(parts[1])
                ),
                -1,
            )
            try:
                cents_val = float(1200 * math.log2(int(parts[1]) / int(parts[0])))
            except ValueError:
                print(f"Invalid interval: {text}")

        #No ratio match found -- try the cents value
        if int_id < 0:
            # Otherwise match cents value
            int_id = next(
                (
                    interval["pk"]
                    for interval in intervals
                    # Match on isclose() to allow for rounding/float imprecision.
                    # Difference is entirely inaudible, so essentially meaningless.
                    if math.isclose(
                        interval["fields"]["cents"],
                        float(cents_val),
                        abs_tol=self.CENTS_TOLERANCE,
                    )
                ),
                -1,
            )

        #Finally, add it to the missing intervals list
        if int_id < 0:
            self.missing.append(text)

        return (None, int_id) [int_id > 0]



args = sys.argv
if len(args) < 2:
    usage()

scl_dir = Path(args[1])
if not scl_dir.is_dir():
    sys.exit(f"Invalid directory: {scl_dir}.")

files = [f for f in scl_dir.iterdir() if Path.is_file(f)]

interval_file = open(
    (Path(__file__).parent / "../pitch-systems-api/fixtures/interval.json").resolve(),
    "r",
)
intervals = json.load(interval_file)

# Manual mapping of systems to scl files.
sys_map: dict = {}

with open("system_map.csv") as sys_file:
    for line in sys_file:
        try:
            parts = line.split(",")
            sys_map[parts[0]] = parts[1].rstrip()
        except IndexError:
            print(f"Bad sys_map line: {line}")

print(sys_map)


parser = SclParser(intervals, sys_map)

fixtures = []
i = 1

incomplete_file = open("incomplete", "w")


for f in files:

    # Drop scales with unmatched intervals
    results = parser.parse(f)
    if results and None in results["intervals"]:
        incomplete_file.write(f"{f}\n")
    else:
         # TMP: Drop if system unmatched
        if results and "system" in results:
            fixtures.append(
                {
                    "pk": i,
                    "model": "pitches.scale",
                    "fields": results
                }
            )
            i += 1
        else:
            print(f"No system: {results}")


pprint(parser.missing)
incomplete_file.close()

# Write the JSON fixtures file
out_file = open("scale.json", "x")
out_file.write(json.dumps(fixtures))
out_file.close()
