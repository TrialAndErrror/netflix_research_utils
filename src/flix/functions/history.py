import glob
from pathlib import Path
from typing import List, Tuple, Text

import pandas as pd
from bs4 import BeautifulSoup

from src.flix import PICKLE_DIR
from src.flix.utils.debug_messages import print_red, print_green
from src.flix.functions.utils import check_for_missing_data
from src.flix.utils.network import get_data
from src.flix.utils.pickle import save_pickle, load_pickle


def flix_history(nf_id_dict):
    missing_titles = []

    for slug in nf_id_dict:
        missing = get_data(slug, url='top10/', extra_folder='history')

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')


def get_history_tables(soup: BeautifulSoup) -> List[Tuple[str, pd.DataFrame]]:
    """
    Read soup and search for Netflix Top 10 History tables;
    return a list if any tables are found

    :param soup: BeautifulSoup
    :return:
    """
    results_list = []

    netflix_movies = soup.select('#toc-netflix-2')

    if netflix_movies:
        html_snippet = str(netflix_movies)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Movies', data[0]))

    if len(results_list) > 0:
        return results_list


def read_history_soup(filename) -> (Text, List[Tuple[str, pd.DataFrame]]):
    """
    Load pickle file, convert data to soup object, and get Top 10 History tables.

    :param filename:
    :return:
    """

    """
    Load pickle and initialize soup object.
    """
    pickle_path = Path(PICKLE_DIR, 'history', filename)
    title = filename.split('.')[0].split('/')[-1]
    obj: str = load_pickle(pickle_path)
    soup: BeautifulSoup = BeautifulSoup(obj, features='lxml')

    """
    Search for Top 10 tables in data.
    """
    try:
        missing_data = check_for_missing_data(soup)
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {soup}')
        results = None
    else:
        results = get_history_tables(soup) if not missing_data else None

    return title, results


def make_history_dfs():
    """
    Make Dataframes from all History Pickles.

    Save the Info tables and premiere dates.

    :return: None
    """

    """
    Load History pickles.
    """
    print('Working on History')
    history_dict = {}
    history_files = glob.glob(f'{PICKLE_DIR}/history/*.pickle')
    files_count = len(history_files)
    counter = 1

    """
    Loop over history pickles and get Top 10 table data.
    """
    for file in history_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results = read_history_soup(file)
            if isinstance(results, list):
                print_green(f'Found History data for {title}')
                history_dict[title] = results

        counter += 1

    """
    Save entire history dict as Pickle object.
    """
    save_pickle(history_dict, '!!!history_df_results!!!', extra_folder='summary')

    """
    Save just Netflix Movies as a CSV Dataframe.
    """
    for title, df in history_dict:
        result = df.to_dict()
    raise NotImplementedError