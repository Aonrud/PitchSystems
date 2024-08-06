from flask import Flask, jsonify, request
from urllib.parse import quote_plus, unquote_plus
from parser import *
import os
from dotenv import load_dotenv
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Load configuration
conf_file = open(BASE_DIR / 'config.yaml', 'r')
config = yaml.safe_load(conf_file)
print(config)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    response = {
        "key": "value"
    }
    return jsonify(response)

@app.route('/api/v1/', methods=['GET'])
def api():
    url_encoded = request.args.get("url")
    if not url_encoded:
        return "No URL provided. Requests must include a valid 'url' parameter", 400

    url = unquote_plus(url_encoded)
    try:
        audio = AudioUrlHandler(url=url)
    except ValueError:
        return "Invalid audio URL", 400

    parser = AudioParser(audio.get(), config)
    return jsonify(parser.parse())

if __name__ == '__main__':
    app.run(host="127.0.0.1", threaded=True, debug=True ) # Dev use only