import os
import pickle
from pathlib import Path

from src.flix import PICKLE_DIR


def get_pickle_path(filename, extra_folder: str = None):
    filename = filename if filename.endswith('.pickle') else f'{filename}.pickle'
    if extra_folder:
        path = Path(PICKLE_DIR, extra_folder, f'{filename}')
    else:
        path = Path(PICKLE_DIR, f'{filename}')
    os.makedirs(path.parent, exist_ok=True)
    return path


def save_pickle(data, filename: str, extra_folder: str = None):
    path = get_pickle_path(filename, extra_folder)

    with open(path, 'w+b') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data
