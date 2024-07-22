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

    intervals: dict

    def __init__(self, intervals: list):
        self.intervals = intervals

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

        # TODO: For robustness, check that the count matches the number of intervals received.
        for line in scl:
            # Ignore comment lines
            if line[0] == "!":
                continue

            if scale["name"] == "":
                scale["name"] = line.strip()
            elif scale["count"] == 0:
                scale["count"] = int(line)
            else:
                scale["intervals"].append(self.get_interval_id(line))

        # Count isn't part of Scale model
        del scale["count"]

        # Scl doesn't provide description beyond a title
        scale["description"] = scale["name"]

        return scale

    def get_interval_id(self, text: str) -> int:
        """
        Get the interval ID matching an scl interval line
        """

        # An integer without decimal point is assumed to be X/1 ratio
        if text.find(".") == -1 and text.find("/") == -1:
            text += "/1"

        # Handle ratios
        if text.find("/") != -1:
            parts = text.split("/")
            return next(
                (
                    interval["pk"]
                    for interval in intervals
                    if interval["fields"]["ratio_numerator"] == int(parts[0])
                    and interval["fields"]["ratio_denominator"] == int(parts[1])
                ),
                None,
            )

        # Otherwise match cents value
        return next(
            (
                interval["pk"]
                for interval in intervals
                # Match on isclose() to allow for rounding/float imprecision.
                # Difference is entirely inaudible, so essentially meaningless.
                if math.isclose(
                    interval["fields"]["cents"],
                    float(text),
                    abs_tol=self.CENTS_TOLERANCE,
                )
            ),
            None,
        )


args = sys.argv
if len(args) < 2:
    usage()

scl_dir = Path(args[1])
if not scl_dir.is_dir():
    sys.exit(f"Invalid directory: {scl_dir}.")

files = [f for f in scl_dir.iterdir() if Path.is_file(f)]

interval_file = open(
    (Path(__file__).parent / "../pitch-system-api/fixtures/interval.json").resolve(),
    "r",
)
intervals = json.load(interval_file)

parser = SclParser(intervals)

fixtures = []
i = 1

for file in files:
    fixtures.append(
        {
            "pk": i,
            "model": "pitches.scale",
            "fields": parser.parse(file)
        }
    )
    i += 1

pprint(fixtures)
out_file = open("scales.json", "x")
out_file.write(json.dumps(fixtures))
out_file.close()