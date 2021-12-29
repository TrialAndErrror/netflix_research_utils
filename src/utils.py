import json
from pathlib import Path


def read_file(filename: Path):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


def write_file(data: dict, filename: Path):
    with open(filename, 'w+') as file:
        json.dump(data, file)