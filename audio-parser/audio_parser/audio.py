import validators
import requests
from requests_cache import CachedSession, FileCache
from io import BytesIO
import librosa
from cents import *
import statistics
import numpy
import asyncio
import websockets
from pathlib import Path
import json
from urllib.request import urlopen
import soundfile

BASE_DIR = Path(__file__).resolve().parent.parent


class AudioUrlHandler:
    """
    Fetch, validate and open audio file data from a remote URL.
    """

    def __init__(self, *, url: str) -> None:
        self.validate_url(url)
        self.url = url
        self.session = CachedSession(
            "http_cache", backend=FileCache(decode_content=False), stream=True
        )

    def validate_url(self, url: str) -> None:
        """
        Check that a URL is valid, available and represents an audio file.
        """
        # Check the string is a url
        if not validators.url(url):
            raise ValueError("Invalid URL")

        # Check the URL returns an audio file
        file_check = requests.head(url)

        if not file_check.status_code == 200:
            raise ValueError("URL can't be retrieved")

        mime = file_check.headers["Content-Type"].partition(";")[0]

        if not mime.partition("/")[0] == "audio":
            raise ValueError("URL is not an audio file")

    def get(self) -> soundfile.SoundFile:
        # Could become invalid between instantiation and fetch
        self.validate_url(self.url)
        response = self.session.get(self.url)
        print(response.content)
        f = BytesIO(response.content)
        return soundfile.SoundFile(f)


class AudioParser:

    def __init__(self, settings: dict) -> None:
        """ """
        self.cents_tolerance = settings["cents_tolerance"]
        self.sample_significance = settings["sample_significance"]
        self.min = settings["freq_min"]

    async def stream(self, file, websocket):
        n_fft = 2048
        hop_length = 512
        sr = librosa.get_samplerate(file)

        stream = librosa.stream(
            file,
            block_length=16,
            frame_length=n_fft,
            hop_length=hop_length,
            mono=True,
            fill_value=0,
        )
        for y_block in stream:
            result = librosa.pyin(
                y_block, sr=sr, fmin=self.min, fmax=self.max
            )
            message = json.dumps(result[0])
            await websocket.send(message)


    def parse(self) -> dict:
        y, sr = librosa.load(self.data)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, sr=sr, fmin=self.min, fmax=self.max
        )

        f0 = f0[~numpy.isnan(f0)]
        freqs, durations = self.collate(f0.tolist())

        # Try accepting only freqs detected for x or more samples
        freqs_filtered = [
            freq
            for (freq, duration) in zip(freqs, durations)
            if duration > self.sample_significance
        ]

        intervals = [0.0]  # First note is unison with itself
        for i in range(len(freqs_filtered)):
            if i > 0:
                intervals.append(interval(freqs_filtered[0], freqs_filtered[i]))

        return {"freqs": freqs_filtered, "intervals": intervals}

    def collate(self, freqs: list) -> list:
        """
        Collate frequencies into note groups based on frequency proximity.

        This is quite a crude approach, but is useful where a good onset algorithm is absent.
        Proper onset should account for attack, confidence and pitch change together.
        """
        groups: list[list] = [[]]
        durations: list[int] = []
        group_index: int = 0

        # Group freqs. into lists where they are +- cents_tolerance cents apart
        for i in range(len(freqs)):
            if i > 0:
                diff = interval(freqs[i - 1], freqs[i])
                if abs(diff) > self.cents_tolerance:
                    group_index += 1
                    groups.append([])
                groups[group_index].append(freqs[i])

        notes = []
        for group in groups:
            if len(group) > 0:
                durations.append(len(group))
                # notes.append(statistics.median(group))
                notes.append(statistics.mean(group))
        return [notes, durations]
