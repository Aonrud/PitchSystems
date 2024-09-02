from audio import AudioParser
from websocket import *
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from sys import argv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


async def main(mode:str):
    socket = SocketHandler(mode = mode)

    # Start the connection
    await socket.connect()


if __name__ == "__main__":
    mode = "socket"
    if len(argv) > 1 and argv[1] == "dev":
        mode = "port"
    asyncio.run(main(mode))
