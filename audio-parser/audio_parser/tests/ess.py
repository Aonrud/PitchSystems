import essentia
import essentia.standard as es
from pprint import pprint
import numpy
import matplotlib.pyplot as plt
from pylab import plot, show, figure, imshow

plt.rcParams["figure.figsize"] = (15, 6)


def read(file):
    audio = es.EqloudLoader(filename=file, sampleRate=44100)()
    hopSize = 128
    frameSize = 2048
    sampleRate = 44100

    pitch_extractor = es.PitchMelodia(frameSize=frameSize, hopSize=hopSize)
    pitch_values, pitch_confidence = pitch_extractor(audio)
    pitch_times = numpy.linspace(0.0, len(audio) / sampleRate, len(pitch_values))

    #print("Pitch times:")
    #print(numpy.round(pitch_times, 2))

    # Parse out onsets to then apply to raw frequency data?
    onsets, durations, notes = es.PitchContourSegmentation(hopSize=128)(
        pitch_values, audio
    )
    for i, f in enumerate(pitch_values):
        print("{}: freq: {} confidence: {}".format(i, pitch_values[i], pitch_confidence[i]))

    return pitch_values
