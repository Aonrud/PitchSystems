import math
from decimal import Decimal


def cents_between(f1: float, f2: float) -> float:
    """
    Return the interval in cents between two frequencies
    """
    return 1200 * math.log2(f2 / f1)


def cents_above(freq: float, cents: float) -> float:
    """
    Return the frequency in Hertz that is the given
    number of cents above the given frequency.
    """
    return freq * (2 ** (cents / 1200))
