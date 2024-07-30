import librosa_pyin as freq_reader
# import ess as freq_reader
# import pd as freq_reader
import csv
import numpy as np
import audio_parser.cents as cents
import statistics
from pprint import pprint


def collate(freqs: list, cents_tolerance: int = 10) -> list:
    """
    Collate frequencies into note groups based on frequency proximity.

    This is quite a crude approach, but is useful where a good onset algorithm is absent.
    Proper onset should account for attack, confidence and pitch change together.

    :param int cents_tolerance:
    :param list freqs:
    :return: list
    """
    groups = [[]]
    durations = []
    group_index = 0

    # Group freqs. into lists where they are +- 5 cents apart
    for i in range(len(freqs)):
        if i > 0:
            diff = cents.interval(freqs[i - 1], freqs[i])
            # print("Difference of {} cents".format(diff))
            if abs(diff) > cents_tolerance:
                group_index += 1
                groups.append([])
            groups[group_index].append(freqs[i])

    notes = []
    for group in groups:
        if len(group) > 0:
            durations.append(len(group))
            notes.append(statistics.median(group))
    return [notes, durations]


# For human-readable numpy output
np.set_printoptions(precision=3)

audio_dir = "audio_files/recorded/"
# audio_dir = "audio_files/generated/"
csv_file = 'compare.csv'
# csv_file = 'short.csv'

with open(audio_dir + csv_file) as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        row: dict
        print("Checking " + row["filename"])
        data = freq_reader.read(audio_dir + row["filename"])

        print("Raw data:")
        pprint(data)
        freqs, durations = collate(data)
        print("Freqs. collated:")
        print(freqs)
        # print("Durations (frames):")
        # print(durations)

        print("Freqs. target:")
        print(row["target_frequencies"])

        intervals = []
        for i in range(len(freqs)):
            if i > 0:
                intervals.append(cents.interval(freqs[0], freqs[i]))
        print("Intervals:")
        print(intervals)

        print("Target intervals:")
        print(row["intervals"])
