import datetime
import json
import os
from pathlib import Path

import numpy as np

"""
Filename Setup:

Filename determines the name of the results file.
Currently set to "results" with a timestamp at the end.
"""
RESULTS_FILENAME = f'results_{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.json'


def load_from_json_data(filename):
    nf_path = Path(os.getcwd(), 'nf_dict.json')

    if not nf_path.exists():
        path = Path(os.getcwd(), filename)
        with open(path, 'r') as file:
            json_data = json.load(file)

        all_movies = list(np.concatenate([item['results'] for item in json_data]).flat)
        nf_lookup = {item['title']: item['nfid'] for item in all_movies}
        with open(nf_path, 'w+') as file:
            json.dump(nf_lookup, file)

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
