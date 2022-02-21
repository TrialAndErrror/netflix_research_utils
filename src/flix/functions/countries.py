import glob
import os
from pathlib import Path
from typing import Optional, List, Text

import pandas as pd
from bs4 import BeautifulSoup

from src.flix import PICKLE_DIR, SUMMARY_DIR
from src.flix.utils.debug_messages import print_red, print_green
from src.flix.utils.pickle_utils import save_pickle, load_pickle
from src.flix.utils.network import get_data

from src.utils import write_file


def flix_countries(nf_id_dict):
    missing_titles = []

    for slug in nf_id_dict:
        missing = get_data(slug, url='streaming/', extra_folder='country')

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')


def get_countries_list(soup) -> Optional[List]:
    """
    Search Netflix Top 10 Table soup for all Countries listed;
    convert Series of the Column to a list.

    :param soup: BeautifulSoup
    :return: list
    """
    try:
        df = pd.read_html(str(soup))
    except ValueError:
        print_red('No tables found')
    else:
        my_list = list(df[0].loc[:, 0])
        return my_list


def read_country_soup(filename) -> (Text, List):
    """
    Load pickle file, convert data to soup object, and get countries from the Netflix Countries table.

    :param filename: str
    :return: (str, list)
    """

    """
    Load pickle and initialize soup object.
    """
    pickle_path = Path(PICKLE_DIR, 'language', filename)
    title = filename.split('.')[0].split('/')[-1]
    obj: str = load_pickle(pickle_path)
    soup: BeautifulSoup = BeautifulSoup(obj, features='lxml')

    """
    Search soup for Netflix table;;
    if present, parse languages from table dataframe.
    """
    netflix_table = soup.find(id='toc-netflix')
    results = None

    if netflix_table:
        results = get_countries_list(netflix_table)

    return title, results


def make_country_dfs(slug_replace_dict):
    """
    Make Dataframes from all Country Pickles.

    Return the Info tables and premiere dates.

    :return: None
    """

    """
    Load History pickles.
    """
    print('Working on Languages')
    country_dict = {}
    country_files = glob.glob(f'{PICKLE_DIR}/language/*.pickle')
    files_count = len(country_files)
    counter = 1

    """
    Loop over country files and make dict of results.
    """
    for file in country_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results = read_country_soup(file)
            if isinstance(results, list):
                print_green(f'Found Country data for {title}')
                country_dict[title] = results

        counter += 1

    write_file(country_dict, Path(SUMMARY_DIR, 'country_results.json'))
