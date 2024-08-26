from urllib.parse import unquote_plus
from audio import AudioParser
from websocket import *
from dotenv import load_dotenv
import yaml
from pathlib import Path
import asyncio


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Load configuration
conf_file = open(BASE_DIR / "config.yaml", "r")
config = yaml.safe_load(conf_file)


async def run():
    parser = AudioParser(config)
    socket = SocketHandler("localhost", 5678, parser)
    await socket.connect()


if __name__ == "__main__":
    asyncio.run(run())
