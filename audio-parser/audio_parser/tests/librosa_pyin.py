import statistics
import librosa
import numpy as np


def read(file):
    fmin = 75
    fmax = 1400
    prob_threshold = 0.5

    y, sr = librosa.load(file)

    # Split harmonic and percussive.
    # Percussive is useful for instruments with a reasonable attack, but nonsense results for e.g. clean sine wave
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    freqs, voiced_flag, voiced_probs = librosa.pyin(y_harmonic, sr=sr, fmin=fmin, fmax=fmax)
    # print(onset_frames)
    freq_groups = []
    group_index = -1
    for index, freq in enumerate(freqs):
        #Drop before first onset
        if (index >= onset_frames[0]):
            if index in onset_frames:
                freq_groups.append([])
                group_index+=1
            #print("Index: {} voiced: {} Prob: {} Freq: {}".format(index, voiced_flag[index], voiced_probs[index], freq))
            if (voiced_flag[index] == True and voiced_probs[index] >= prob_threshold):
                freq_groups[group_index].append(freq)

    notes = []
    frame_counts = []
    for group in freq_groups:
        if len(group)> 0:
            notes.append(statistics.median(group))
            frame_counts.append(len(group))
    print(frame_counts)
    return notes

