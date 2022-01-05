import os

from src.flix.utils import load_pickle, save_pickle
from src.flix import PICKLE_DIR
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re
import glob
from src.flix.debug_messages import print_green, print_red


def check_for_missing_data(soup: BeautifulSoup):
    # soup = BeautifulSoup(obj, "lxml")
    try:
        content_div = soup.find_all('div', {'class': 'content'})[-1]
    except IndexError:
        return True
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {soup}')
        return True
    else:
        return re.search('No streaming data', content_div.text)


def read_info_soup(filename):
    pickle_path = Path(PICKLE_DIR, 'info', filename)
    title = filename.split('.')[0].split('/')[-1]
    dataframes_dict = None
    obj: str = load_pickle(pickle_path)
    if not isinstance(obj, str):
        print('here')
    soup = BeautifulSoup(obj, features='lxml')

    results = None
    missing_data = check_for_missing_data(soup)

    if not missing_data:
        obj_soup = BeautifulSoup(obj, features='lxml')
        netflix_table = obj_soup.find(id='netflix')
        if netflix_table:
            html_snippet = str(netflix_table)
            data = pd.read_html(html_snippet)
            results = ('Netflix Info', data)

    return title, results


def get_history_tables(soup: BeautifulSoup, html_obj):
    results_list = []

    netflix_overall = soup.find(id='toc-netflix-1')
    netflix_movies = soup.select('#toc-netflix-2')
    netflix_kids = soup.select('#toc-netflix-40')
    netflix_official = soup.select('#toc-netflix-official')

    if netflix_overall:
        html_snippet = str(netflix_overall)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Overall', data))

    if netflix_movies:
        html_snippet = str(netflix_movies)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Movies', data))

    if netflix_kids:
        html_snippet = str(netflix_kids)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Kids', data))

    if netflix_official:
        html_snippet = str(netflix_official)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Official', data))

    if len(results_list) > 0:
        return results_list


# def read_language_soup(filename):
#     pickle_path = Path(PICKLE_DIR, 'history', filename)
#     title = filename.split('.')[0].split('/')[-1]
#     obj: str = load_pickle(pickle_path)
#     soup: BeautifulSoup = BeautifulSoup(obj, features='lxml')
#     results = None
#
#     try:
#         missing_data = check_for_missing_data(soup)
#     except TypeError:
#         print_red('Error: Object text might not exist')
#         print(f'Corrupted text: {soup}')
#         missing_data = True
#
#     if not missing_data:
#         results = get_history_tables(soup, obj)

def read_history_soup(filename):
    pickle_path = Path(PICKLE_DIR, 'history', filename)
    title = filename.split('.')[0].split('/')[-1]
    obj: str = load_pickle(pickle_path)
    soup: BeautifulSoup = BeautifulSoup(obj, features='lxml')
    results = None

    try:
        missing_data = check_for_missing_data(soup)
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {soup}')
        missing_data = True

    if not missing_data:
        results = get_history_tables(soup, obj)

    return title, results


def make_info_dfs(pickle_dir):
    info_files = glob.glob(f'{pickle_dir}/info/*.pickle')
    files_count = len(info_files)
    counter = 1

    info_dict = {}

    for file in info_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results = read_info_soup(file)
            if isinstance(results, tuple):
                print_green(f'Found top 10 data for {title}')
                info_dict[title] = results

        counter += 1

    save_pickle(info_dict, '!!!info_df_results!!!', extra_folder='info')


def make_history_dfs(pickle_dir):
    print('Working on History')
    history_dict = {}
    history_files = glob.glob(f'{pickle_dir}/history/*.pickle')
    files_count = len(history_files)
    counter = 1

    for file in history_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results = read_history_soup(file)
            if isinstance(results, list):
                print_green(f'Found History data for {title}')
                history_dict[title] = results

        counter += 1
    save_pickle(history_dict, '!!!history_df_results!!!', extra_folder='history')


# def make_langauge_dfs(pickle_dir):
#     print('Working on History')
#     history_dict = {}
#     history_files = glob.glob(f'{pickle_dir}/history/*.pickle')
#     files_count = len(history_files)
#     counter = 1
#
#     for file in history_files:
#         if not file.split('/')[-1].startswith('!!!'):
#             print(f'Working on {counter}/{files_count}')
#             title, results = read_history_soup(file)
#             if isinstance(results, list):
#                 print_green(f'Found History data for {title}')
#                 history_dict[title] = results
#
#         counter += 1
#     save_pickle(history_dict, '!!!history_df_results!!!', extra_folder='history')


def make_dfs(pickle_dir=PICKLE_DIR):
    make_info_dfs(pickle_dir)
    make_history_dfs(pickle_dir)

    print('\n\nResults saved.\n\n')


def test_debug():
    pass
    # top_10_filename = 'red-notice.pickle'
    # no_results_filename = 'quincy.pickle'
    # read_soup(no_results_filename)


if __name__ == '__main__':
    make_dfs()
