import pickle
import re
from pathlib import Path
from src.flix import PICKLE_DIR


def check_for_404(soup_data):
    return re.search('Page Not Found', soup_data)

def get_pickle_path(filename):
    filename = filename if filename.endswith('.pickle') else f'{filename}.pickle'
    path = Path(PICKLE_DIR, f'{filename}')
    return path


def save_pickle(data, filename: str):
    path = get_pickle_path(filename)

    with open(path, 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data
