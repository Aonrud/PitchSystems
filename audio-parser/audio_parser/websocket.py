import validators
import requests
from requests_cache import CachedSession, FileCache
from io import BytesIO
import librosa
import websockets
import json
from audio import *
import os

class SocketHandler:
    """
    Set up and handle the websocket.
    Websocket can be set either to listen on a port or bind to a Unix socket by passing 'mode' param of "port" or "socket".

    param mode:
    param host:
    param port:
    """

    def __init__(self, mode: str = "socket", host: str = "localhost", port: int = 5678):
        self.mode = mode
        self.host = host
        self.port = port

    async def connect(self):
        """
        Setup the websocket ready for connections.
        """
        if self.mode == "port":
            await self.connect_port()
        else:
            await self.connect_socket()

    async def connect_port(self):
        """
        Create the websocket in 'port' mode.
        """
        print(f"Listening at {self.host}:{self.port}")
        async with websockets.serve(self.handler, host=self.host, port=self.port):
            await asyncio.Future()

    async def connect_socket(self):
        """
        Create the websocket in unix socket mode.
        """
        sockdir = "/run/sockets/"
        sockfile = "audio-parser.sock"
        # Give socket a unique name if running under Supervisor
        if "SUPERVISOR_PROCESS_NAME" in os.environ:
            sockfile = f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock"

        socket = sockdir + sockfile
        print(f"Listening on unix socket at {socket}")

        async with websockets.unix_serve(
            self.handler,
            path=socket,
        ):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        async for message in websocket:
            if isinstance(message, str):
                await self.str_message(message, websocket)
            else:
                await self.bin_message(message, websocket)

    async def str_message(self, message: str, websocket):
        try:
            data = json.loads(message)
            if data["url"]:

                audio = AudioUrlHandler(url=data["url"])
                parser = AudioParser("config.yaml")

                # Check if any settings adjustments have been passed
                if "settings" in data:
                    parser.applySettings(data["settings"])

                # Parse the audio
                await parser.stream(audio.get(), websocket)
        except json.JSONDecodeError:
            await websocket.send(
                json.dumps(
                    {"status": "error", "message": "Received an invalid message."}
                )
            )

    async def validate(message):

        await websocket.send(
            json.dumps({"status": "error", "message": "Received an invalid message."})
        )
        return False

    async def bin_message(self, message, websocket):
        pass
