from pitch_detectors import algorithms
import numpy as np
from scipy.io import wavfile


def read(file):
    rate, audio = wavfile.read(file)

    # Convert 16bit to float
    audioFloat = audio.astype(np.float64)
    data = algorithms.PipTrack(audioFloat, rate)
    return data.f0