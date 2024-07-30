import validators
import requests
from requests_cache import CachedSession, FileCache
from io import BytesIO
import librosa
import cents
import statistics
import numpy


class AudioUrlHandler:
    """
    Fetch, validate and open audio file data from a remote URL.
    """

    def __init__(self, *, url: str) -> None:
        self.validate_url(url)
        self.url = url
        self.session = CachedSession(
            "http_cache", backend=FileCache(decode_content=False)
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

    def __init__(self, data: BytesIO) -> None:
        self.data = data

    def parse(self) -> dict:
        y, sr = librosa.load(self.data)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, sr=sr, fmin=50, fmax=2000)

        f0 = f0[~numpy.isnan(f0)]
        freqs, durations = self.collate(f0.tolist())

        # Try accepting only freqs detected for 10 or more samples
        freqs_filtered = [freq for (freq, duration) in zip(freqs, durations) if duration > 10]

        intervals = [ 0.0 ] # First note is unison with itself
        for i in range(len(freqs_filtered)):
            if i > 0:
                intervals.append(cents.interval(freqs_filtered[0], freqs_filtered[i]))

        return {"freqs": freqs_filtered, "intervals": intervals}

    def collate(self, freqs: list, cents_tolerance: int = 20) -> list:
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
                diff = cents.interval(freqs[i - 1], freqs[i])
                if abs(diff) > cents_tolerance:
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
