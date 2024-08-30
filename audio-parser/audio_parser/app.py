from urllib.parse import unquote_plus
from audio import AudioParser
from websocket import *
from dotenv import load_dotenv
from pathlib import Path
import asyncio


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


async def run():
    socket = SocketHandler("localhost", 5678)
    await socket.connect()


if __name__ == "__main__":
    asyncio.run(run())
