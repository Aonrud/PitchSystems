import math


def interval(f1: float, f2: float) -> float:
    """
    Get the interval in cents between two frequencies.
    """
    return 1200 * math.log2(f2 / f1)


def add(freq: float, cents: float) -> float:
    """
    Get the frequency in Hertz that is the given
    number of cents above the given frequency.
    """
    return freq * (2 ** (cents / 1200))
