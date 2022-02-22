import json
import pickle
from pathlib import Path
import shutil

from src.unogs import PICKLE_FOLDER


def read_json(filename: Path):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


def write_json(data: dict or list, filename: Path):
    with open(filename, 'w+') as file:
        json.dump(data, file, indent=4)


def copy_file(file_path, dest_path):
    try:
        shutil.copy(file_path, dest_path)
        print("File copied successfully.")

    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

    # If there is any permission issue
    except PermissionError:
        print("Permission denied.")


def save_pickle(data, filename: str):
    path = Path(PICKLE_FOLDER, filename)

    with open(path, 'w+b') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    path = Path(PICKLE_FOLDER, filename)
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data