import os
import pickle
from pathlib import Path

import pandas as pd

from src.utils import read_json


def get_file_path(key, timeframe):
    return Path(Path(os.getcwd(), 'pickles'), f'{key}: {timeframe}.pickle')


def read_pytrends_data(file_path):
    with open(file_path, 'rb') as infile:
        data = pickle.load(infile)

    return data


def load_netflix_nametags():
    netflix_nametags_file = Path(os.getcwd(), 'netflix_nametags.json')
    if not netflix_nametags_file.exists():
        raise FileNotFoundError('Missing Netflix Nametags file')
    netflix_titles_df = pd.DataFrame(read_json(netflix_nametags_file))
    return netflix_titles_df


def setup_directories():
    output_dir = Path(os.getcwd(), 'results')
    pickle_dir = Path(os.getcwd(), 'pickles')
    output_dir.mkdir(exist_ok=True)
    pickle_dir.mkdir(exist_ok=True)
    return pickle_dir, output_dir