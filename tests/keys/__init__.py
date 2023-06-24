import json
from pathlib import Path
from joserfc.jwk import import_key

BASE_PATH = Path(__file__).parent


def load_key(filename: str, options=None):
    with open((BASE_PATH / filename).resolve(), "rb") as f:
        content: bytes = f.read()

    if filename.endswith(".json"):
        data = json.loads(content)
        return import_key(data['kty'], data, options)

    kty = filename.split('-', 1)[0]
    return import_key(kty.upper(), content, options)


def read_key(filename: str):
    with open((BASE_PATH / filename).resolve(), "rb") as f:
        content: bytes = f.read()

    if filename.endswith(".json"):
        return json.loads(content)
    return content