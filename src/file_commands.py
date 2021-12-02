import json
import os
from pathlib import Path
import numpy as np

from src import RESULTS_FILENAME


def load_from_json_data(filename):
    """
    Load file from JSON data.

    Option 1) Load from filename provided in parameters, which should be data from the
    UNOGS API

    Option 2) Load form nf_dict, which is a dictionary in the format of:
    {
        Movie Name: Netflix ID
    }

    If Option 1 is used, the script will create nf_dict and save it.

    :param filename:
    :return: dict
    """
    nf_path = Path(os.getcwd(), 'nf_dict.json')

    """
    If nf_dict doesn't exist, create it
    """
    if not nf_path.exists():
        """
        Load from filename provided
        """
        path = Path(os.getcwd(), filename)
        with open(path, 'r') as file:
            json_data = json.load(file)

        """
        Split into lists of movies, then create dictionary.
        """
        all_movies = list(np.concatenate([item['results'] for item in json_data]).flat)
        nf_lookup = {item['title']: item['nfid'] for item in all_movies}

        """
        Save nf_dict
        """
        with open(nf_path, 'w+') as file:
            json.dump(nf_lookup, file)

    """
    Load from nf_dict
    """
    with open(nf_path, 'r') as file:
        data = json.load(file)

    return data


def save_results(movie_data):
    """
    Save results to json file.

    Filename is provided by global RESULTS_FILENAME constant.

    :param movie_data: dict
    :return: None
    """
    with open(RESULTS_FILENAME, 'w+') as file:
        json.dump(movie_data, file)
