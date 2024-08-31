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
    Set up and handle the websocket
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        sockdir = "/run/sockets/"
        sockfile = "audio-parser.sock"
        # Give socket a unique name if running under Supervisor
        if "SUPERVISOR_PROCESS_NAME" in os.environ:
            sockfile = f"{os.environ['SUPERVISOR_PROCESS_NAME']}.sock"
        
        socket = sockdir + sockfile
        print(f"Socket will be created at {socket}")

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
                if data["settings"]:
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
