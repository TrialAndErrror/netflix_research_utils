import json
from pathlib import Path
import shutil


def read_file(filename: Path):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


def write_file(data: dict or list, filename: Path):
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
