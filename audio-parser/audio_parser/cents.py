import numpy as np


def interval(f1: float, f2: float):
    return 1200 * np.log2(f2/f1)


def add(freq: float, cents: float):
    return (freq * cents * 2)/1200
