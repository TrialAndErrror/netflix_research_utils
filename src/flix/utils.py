import os
import pickle
import re
from pathlib import Path
from src.flix import PICKLE_DIR
from slugify import slugify


def get_slug(title):
    if title == 'Security (Netflix Original)':
        slug = 'security-2021'
    elif title == 'Outlaws (Netflix Original)':
        slug = 'outlaws-2021'
    else:
        slug = slugify(title).replace('/', '')
    return slug


def check_for_404(soup_data):
    return re.search('Page Not Found', soup_data)


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
