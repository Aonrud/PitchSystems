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
from datetime import timedelta
import yaml

class AudioUrlHandler:
    """
    Fetch, validate and open audio file data from a remote URL.
    """

    def __init__(self, *, url: str) -> None:
        self.validate_url(url)
        self.url = url
        self.session = CachedSession(
            "http_cache",
            backend=FileCache(decode_content=False),
            stream=True,
            expire_after=timedelta(days=1),
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
            raise ValueError(f"URL can't be retrieved: {url}")

        mime = file_check.headers["Content-Type"].partition(";")[0]

        if not mime.partition("/")[0] == "audio":
            raise ValueError("URL is not an audio file")

    def get(self) -> soundfile.SoundFile:
        # Could become invalid between instantiation and fetch
        self.validate_url(self.url)
        response = self.session.get(self.url)
        f = BytesIO(response.content)
        return soundfile.SoundFile(f)


class Note:
    """
    Represents a note object as they are sent by the parser.
    """

    start: int
    slices: int
    frequency: float


class AudioParser:

    def __init__(self, conf_path: str) -> None:
        """
        param: conf_path Path to the configuration file, relative to the project root.
        """

        # Assign all valid settings with empty values
        self.settings: dict = {
            "cents_tolerance": None,
            "min": None,
            "max": None,
            "prob_tolerance": None,
            "duration_tolerance": None,
        }

        config: dict

        # Load config file
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            conf_file = open(BASE_DIR / conf_path, "r")
            config = yaml.safe_load(conf_file)
        except OSError:
            raise Exception("Can't read configuration file. Please check it exists and is readable.")

        self.applySettings(config)

        if None in self.settings.values():
            # Can't have empty settings in the default config
            raise Exception("Configuration issue. Please check config.yaml for errors.")

        # Temporary variables used during streaming
        self.note_buffer: Note = None
        self.short_buffer: Note = None
        self.total_slices = 0
        self.notes_sent = 0
        self.below_prob = 0

    def applySettings(self, settings: dict):
        """
        Apply a settings dict.
        """
        for key in settings:
            if key in self.settings:
                print(f"Setting {key} to {settings.get(key)}")
                self.settings[key] = settings.get(key)

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
                y_block, sr=sr, fmin=self.settings["min"], fmax=self.settings["max"]
            )
            await self.parse_result(result, websocket)

        # Send the final buffered note
        # TODO: This isn't DRY
        buffer = self.note_buffer
        if buffer["slices"] >= self.settings["duration_tolerance"]:
            await websocket.send(json.dumps(self.note_buffer))

        # Send a conclusion
        final = {
            "status": "ok",
            "message": "End of analysis",
            "notes_sent": self.notes_sent,
            "slices": self.total_slices,
            "below_prob": self.below_prob,
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

        Slices of the stream are merged into a Note() when they meet the matching criteria.

        Notes are then queued for sending on the websocket.
        """
        slices = 0
        group = []

        for slice in zip(*result):
            freq, voiced, prob = slice
            if prob < self.settings["prob_tolerance"]:
                self.below_prob += 1

            # The frequency is only considerd if it is voiced and above the probability tolerance
            if voiced and prob >= self.settings["prob_tolerance"]:

                # If this isn't the first slice of a new group
                if len(group) > 0:
                    # group_avg = statistics.mean(group)
                    # diff = interval(freq, group_avg)

                    diff = interval(freq, group[-1])

                    if abs(diff) > self.settings["cents_tolerance"]:
                        # The note in the group is finished. Send it to the queue.
                        start = self.total_slices - slices
                        note = {
                            "start": start,
                            "slices": slices,
                            "frequency": statistics.mean(group),
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

    def queue_note(self, note: Note) -> Note | None:
        """
        Queue a note for sending.

        Returns a note if there is one due for sending, otherwise returns None.

        Each note is retained in a buffer and compared with the next. If the notes are equal they are merged.

        A note is returned for sending only once a subsequent note has been queued that matches the sending criteria.
        """
        buffer = self.note_buffer

        if not buffer:
            self.note_buffer = note
            return None

        match = self.notes_match(buffer, note)

        if match:
            # Note matches the buffer so merge it in
            self.note_buffer = self.notes_merge(buffer, note)
        else:
            # Update the buffer and return the old buffer for sending
            self.note_buffer = note

            # If the final note is above the duration threshold, send it. Otherwise, drop it.
            if buffer["slices"] >= self.settings["duration_tolerance"]:
                return buffer
            else:
                print("Dropped note:")
                print(buffer)

    def notes_merge(self, note1: Note, note2: Note) -> Note:
        """
        Merge two note objects.
        """
        new_length = note1["slices"] + note2["slices"]
        # The new frequency should average the two.
        # Since we no longer have the individual slice values, the relative size is accounted for below instead of taking a crude average of the two.
        freq = (
            (note1["slices"] * note1["frequency"])
            + (note2["slices"] * note2["frequency"])
        ) / new_length
        return {"slices": new_length, "start": note1["start"], "frequency": freq}

    def notes_match(self, note1: Note, note2: Note) -> bool:
        """
        Check if two notes match, within the cents tolerance range.
        """
        diff = interval(note1["frequency"], note2["frequency"])
        if abs(diff) <= self.settings["cents_tolerance"]:
            return True

        return False
