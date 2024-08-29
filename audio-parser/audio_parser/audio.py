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
        # print(response.content)
        f = BytesIO(response.content)
        return soundfile.SoundFile(f)


class AudioParser:

    def __init__(self, settings: dict) -> None:
        self.cents_tolerance = settings["cents_tolerance"]
        self.min = settings["freq_min"]
        self.max = settings["freq_max"]
        self.prob_tolerance = settings["prob_tolerance"]
        self.duration_tolerance = settings["duration_tolerance"]

        # Temporary variables used during streaming
        self.note_buffer: object = None
        self.total_slices = 0
        self.notes_sent = 0
        self.below_prob = 0

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
            result = librosa.pyin(y_block, sr=sr, fmin=self.min, fmax=self.max)
            await self.parse_result(result, websocket)

        # Send the final buffered note
        # TODO: This isn't DRY
        buffer = self.note_buffer
        if buffer["duration"] < self.duration_tolerance:
            buffer["frequency"] = 0
        await websocket.send(json.dumps(self.note_buffer))

        # Send a conclusion
        final = {
            "status": "ok",
            "message": "End of analysis",
            "notes_sent": self.notes_sent,
            "slices": self.total_slices,
            "below_prob": self.below_prob
        }

        await websocket.send(json.dumps(final))

        # Reset tmp variables.
        # TODO: this shouldn't be necessary - a new instance would make more sense here.
        self.note_buffer = None
        self.notes_sent = 0
        self.total_slices = 0

    async def parse_result(
        self, result: tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray], websocket
    ):
        """
        Parse a block of results from the analysis stream.

        The stream of frequencies and probabilities is held until discrete notes are found.
        Notes are then queued for sending on the websocket.
        """
        slices = 0
        group = []

        for slice in zip(*result):
            freq, voiced, prob = slice
            if prob < self.prob_tolerance:
                self.below_prob += 1

            # The frequency is only considerd if it is voiced and above the probability tolerance
            if voiced and prob >= self.prob_tolerance:

                # If this isn't the first slice of a new group
                if len(group) > 0:
                    group_avg = statistics.mean(group)
                    diff = interval(freq, group_avg)

                    if abs(diff) > self.cents_tolerance:
                        # The note in the group is finished. Send it to the queue.
                        start = self.total_slices - slices
                        note = {
                            "start": start,
                            "duration": slices,
                            "frequency": group_avg,
                        }
                        to_send = self.queue_note(note)
                        if to_send:
                            # There's a note in the queue
                            await websocket.send(json.dumps(to_send))
                            self.notes_sent += 1

                        # Reset temporary variables
                        slices = 0
                        group = []
                    else:
                        group.append(freq)
                        slices += 1
                else:
                    # First of a group
                    group.append(freq)
                    slices += 1
            self.total_slices += 1

    def queue_note(self, note: object) -> object | None:
        """
        Queue a note for sending.

        Returns a note if there is one due for sending, otherwise returns None.

        Each note is retained in a buffer and compared with the next. If they are the same (within the cents tolerance), they are merged.
        This prevents a note that is split across streamed chunks being sent as two separate notes.

        """
        buffer = self.note_buffer

        if buffer:
            diff = interval(note["frequency"], buffer["frequency"])

            if abs(diff) <= self.cents_tolerance:
                # Merge the two notes and update

                # Average based on slice count (i.e. not just the two values)
                mean = (
                    note["duration"] * note["frequency"]
                    + buffer["duration"] * buffer["frequency"]
                ) / (note["duration"] + buffer["duration"])

                note = {
                    "start": buffer["start"],
                    "duration": note["duration"] + buffer["duration"],
                    "frequency": mean,
                }
            else:
                # Update the buffer and return the old buffer for sending
                self.note_buffer = note

                # If the final note is below the duration threshold, zero out the frequency as noise
                if buffer["duration"] < self.duration_tolerance:
                    buffer["frequency"] = 0

                return buffer

        # If the buffer hasn't been returned, it should now be updated
        self.note_buffer = note
        return None
