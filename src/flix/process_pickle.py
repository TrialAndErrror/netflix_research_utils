import os

from src.flix.utils import load_pickle, save_pickle
from src.flix import PICKLE_DIR
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re
import glob
from src.flix.debug_messages import print_green, print_red


def check_for_missing_data(obj):
    soup = BeautifulSoup(obj, "lxml")
    try:
        content_div = soup.find_all('div', {'class': 'content'})[-1]
    except IndexError:
        return True
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {obj}')
        return True
    else:
        return re.search('No streaming data', content_div.text)


def read_info_soup(filename):
    title = filename.split('.')[0].split('/')[-1]
    dataframes_dict = None
    obj: BeautifulSoup = load_pickle(Path(PICKLE_DIR, filename))

    missing_data = check_for_missing_data(obj)

    if not missing_data:
        netflix_table = obj.select('#netflix')
        if netflix_table:

            data_dict = {
                'Recent Netflix': netflix_table,
            }

            dataframes_dict = {key: pd.read_html(value) for key, value in data_dict.items() if value}

    return title, dataframes_dict


def make_history_tables(obj):
    netflix_overall = obj.select('#toc-netflix-1')
    netflix_movies = obj.select('#toc-netflix-2')
    netflix_kids = obj.select('#toc-netflix-40')
    netflix_official = obj.select('#toc-netflix-40')

    data_dict = {
        'Overall': netflix_overall,
        'Movies': netflix_movies,
        'Kids': netflix_kids,
        'Official': netflix_official
    }

    results_dict = {key: pd.read_html(value) for key, value in data_dict.items() if value}
    if len(results_dict) > 0:
        return results_dict


def read_history_soup(filename):
    title = filename.split('.')[0].split('/')[-1]
    dataframes_dict = None
    obj: BeautifulSoup = load_pickle(Path(PICKLE_DIR, filename))

    try:
        missing_data = check_for_missing_data(obj)
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {obj}')
        missing_data = True

    if not missing_data:
       dataframes_dict = make_history_tables(obj)

    return title, dataframes_dict


def make_dfs(pickle_dir=PICKLE_DIR):
    # files = os.listdir(PICKLE_DIR)
    files = glob.glob(f'{pickle_dir}/*.pickle')
    files_count = len(files)
    counter = 1

    info_dict = {}
    history_dict = {}

    for file in files:
        print(f'Working on {counter}/{files_count}')
        title, df = read_info_soup(file)
        title, history_df = read_history_soup(file)
        if isinstance(df, pd.DataFrame):
            print_green(f'Found top 10 data for {title}')
            info_dict[title] = df
        if isinstance(history_df, pd.DataFrame):
            print_green(f'Found History data for {title}')
            history_dict[title] = history_df

        counter += 1

    save_pickle(info_dict, '!!!info_df_results!!!')
    save_pickle(history_dict, '!!!history_df_results!!!')

    print('\n\nResults saved.\n\n')


def test_debug():
    top_10_filename = 'red-notice.pickle'
    no_results_filename = 'quincy.pickle'
    read_soup(no_results_filename)


if __name__ == '__main__':
    make_dfs()