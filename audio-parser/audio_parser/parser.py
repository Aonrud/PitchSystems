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

    def get(self) -> BytesIO:
        # Could become invalid between instantiation and fetch
        self.validate_url(self.url)
        response = self.session.get(self.url)
        return BytesIO(response.content)


class AudioParser:

    def __init__(self, data: BytesIO, settings: dict) -> None:
        """ """
        self.data = data
        self.cents_tolerance = settings["cents_tolerance"]
        self.sample_significance = settings["sample_significance"]
        self.min = settings["freq_min"]
        self.max = settings["freq_max"]

        """Value to store results of current analysis. Should be reset on completion"""
        self.results = []

    async def connect(self):
        async with websockets.serve(self.stream, "localhost", 5678):
            await asyncio.Future()  # run forever

    async def stream(self, websocket):
        n_fft = 2048
        hop_length = 512
        sr = librosa.get_samplerate(self.data)

        file = str(BASE_DIR / 'test.wav')
        stream = librosa.stream(
            file,
            block_length=16,
            frame_length=n_fft,
            hop_length=hop_length,
            mono=True,
            fill_value=0,           
        )
        for y_block in stream:
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y_block, sr=sr, fmin=self.min, fmax=self.max
            )
            self.parse_results((f0, voiced_flag, voiced_probs))
            await websocket.send(json.dumps(f0.tolist()))
            # await asyncio.sleep(random.random() * 2 + 1)

    def parse_results(results: tuple):
        for result in results:
            print(result)




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
