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
    result_date = '0/00/0000'

    obj_soup = BeautifulSoup(obj, features='lxml')
    if not missing_data:
        netflix_table = obj_soup.find(id='netflix')
        if netflix_table:
            html_snippet = str(netflix_table)
            data = pd.read_html(html_snippet)
            results = ('Netflix Info', data)
    try:
        premiere_date = obj_soup.find('span', {'title': 'Premiere'})
        result_date = premiere_date.text
    except AttributeError:
        print(f'Premiere date not found for {title}\n')
    else:
        print(f'Premiere Date: {result_date}\n')
    return title, results, result_date


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


def get_languages_list(soup):
    try:
        df = pd.read_html(str(soup))
    except ValueError:
        print_red('No tables found')
    else:
        my_list = list(df[0].loc[:, 0])
        return my_list


def read_language_soup(filename):
    pickle_path = Path(PICKLE_DIR, 'language', filename)
    title = filename.split('.')[0].split('/')[-1]
    obj: str = load_pickle(pickle_path)
    soup: BeautifulSoup = BeautifulSoup(obj, features='lxml')
    netflix_table = soup.find(id='toc-netflix')
    results = None

    # results = None
    # try:
    #     missing_data = check_for_missing_data(soup)
    # except TypeError:
    #     print_red('Error: Object text might not exist')
    #     print(f'Corrupted text: {soup}')
    #     missing_data = True

    # if not missing_data:
    if netflix_table:
        results = get_languages_list(netflix_table)

    return title, results


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


def make_info_dfs():
    info_files = glob.glob(f'{PICKLE_DIR}/info/*.pickle')
    files_count = len(info_files)
    counter = 1

    info_dict = {}
    premiere_dict = []

    for file in info_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results, premiere_date = read_info_soup(file)
            if isinstance(results, tuple):
                print_green(f'Found Info data for {title}')
                info_dict[title] = results
            premiere_dict.append({
                'title': title,
                'Premiere Date': premiere_date
            })
        counter += 1

    save_pickle(info_dict, '!!!info_df_results!!!', extra_folder='summary')
    premiere_df = pd.DataFrame.from_records(premiere_dict)
    premiere_df.to_csv('./pickle_jar/summary/premiere_dates_df.csv')
    save_pickle(premiere_dict, '!!!premiere_dates!!!', extra_folder='summary')


def make_history_dfs():
    print('Working on History')
    history_dict = {}
    history_files = glob.glob(f'{PICKLE_DIR}/history/*.pickle')
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
    save_pickle(history_dict, '!!!history_df_results!!!', extra_folder='summary')


def make_langauge_dfs(dir=PICKLE_DIR):
    print('Working on Languages')
    language_dict = {}
    language_files = glob.glob(f'{dir}/language/*.pickle')
    files_count = len(language_files)
    counter = 1

    for file in language_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')
            title, results = read_language_soup(file)
            if isinstance(results, list):
                print_green(f'Found Language data for {title}')
                language_dict[title] = results

        counter += 1
    save_pickle(language_dict, '!!!language_df_results!!!', extra_folder='summary')


def make_dfs():
    make_info_dfs()
    make_history_dfs()
    make_langauge_dfs()

    print('\n\nResults saved.\n\n')


def debug_lang_df():
    dir = Path(os.getcwd(), 'src', 'flix', 'pickle_jar')
    make_langauge_dfs(dir)


if __name__ == '__main__':
    make_dfs()
