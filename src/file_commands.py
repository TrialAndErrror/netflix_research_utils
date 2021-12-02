import json
from pathlib import Path
import numpy as np

from src import make_results_filename, INPUT_FOLDER, OUTPUT_FOLDER, PROCESSED_FOLDER


def setup_directories():
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    PROCESSED_FOLDER.mkdir(exist_ok=True)


def load_from_json_data(filename: str):
    """
    Load file from JSON data.

    Option 1) Load from filename provided in parameters, which should be data from the
    UNOGS API

    Option 2) Load form nf_dict, which is a dictionary in the format of:
    {
        Movie Name: Netflix ID
    }

    If Option 1 is used, the script will create nf_dict and save it.

    :param filename: str
    :return: dict
    """
    nf_path = Path(INPUT_FOLDER, 'nf_dict.json')

    """
    If nf_dict doesn't exist, create it
    """
    if not nf_path.exists():
        """
        Load from filename provided
        """
        path = Path(INPUT_FOLDER, filename)
        json_data = read_file(path)

        """
        Split into lists of movies, then create dictionary.
        """
        all_movies = list(np.concatenate([item['results'] for item in json_data]).flat)
        nf_lookup = {item['title']: item['nfid'] for item in all_movies}

        """
        Save nf_dict
        """
        write_file(nf_lookup, nf_path)

    """
    Load from nf_dict
    """
    data = read_file(nf_path)

    return data


def save_results(movie_data: dict):
    """
    Save results to json file.

    Filename is provided by global RESULTS_FILENAME constant.

    :param movie_data: dict
    :return: None
    """
    write_file(movie_data, make_results_filename())


def read_file(filename: Path):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def write_file(data: dict, filename: Path):
    with open(filename, 'w+') as file:
        json.dump(data, file)
