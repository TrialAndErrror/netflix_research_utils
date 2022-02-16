import os
import pickle
import re
from pathlib import Path

import pandas as pd

from src.flix import PICKLE_DIR
from slugify import slugify

from src.utils import write_file


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


def save_premiere_dates_df(premiere_dict):
    premiere_df = pd.DataFrame.from_records(premiere_dict).infer_objects()
    premiere_df['Premiere Date'] = pd.to_datetime(premiere_df['Premiere Date'], format='%m/%d/%Y')
    valid_df = premiere_df[premiere_df['Premiere Date'] > '01/01/2004']
    valid_df.to_csv('./pickle_jar/summary/premiere_dates_df.csv')

    # save_pickle(premiere_dict, '!!!premiere_dates!!!', extra_folder='summary')


def save_top10_dict(data, filename):
    export_dict = {}
    for title, data_tuple in data:
        export_dict[title] = {}

        df_list: pd.DataFrame
        for chart_type, df_list in data_tuple:
            export_dict[title][chart_type] = df_list[0].to_json()

    write_file(export_dict, Path(os.getcwd(), PICKLE_DIR, 'summary', filename))