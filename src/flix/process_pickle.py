from typing import List, Tuple, Optional, Text

from src.flix.utils import load_pickle, save_pickle, save_premiere_dates_df, save_top10_dict
from src.flix import PICKLE_DIR
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re
import glob
from src.flix.debug_messages import print_green, print_red


def check_for_missing_data(soup: BeautifulSoup) -> bool:
    """
    Read soup object and look for the Content div;
    search for 'No Streaming Data' in Content;
    return bool reflecting whether the string is present
    (i.e. whether there is no Netflix data in the soup).

    :param soup: BeautifulSoup
    :return: bool
    """
    try:
        content_div = soup.find_all('div', {'class': 'content'})[-1]
    except IndexError:
        return True
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {soup}')
        return True
    else:
        return bool(re.search('No streaming data', content_div.text))


def read_info_soup(filename) -> (str, Tuple[str, pd.DataFrame], str):
    """
    Load Pickle Data from Filename;
    Process for Netflix Info table and Premiere Date

    :param filename: str

    :return: str, tuple(str, pd.Dataframe), str
    """
    pickle_path = Path(PICKLE_DIR, 'info', filename)
    title = filename.split('.')[0].split('/')[-1]

    """
    Load object from Pickle, then load as BeautifulSoup object.
    """
    obj: str = load_pickle(pickle_path)
    soup = BeautifulSoup(obj, features='lxml')

    """
    Check for Top 10 data;
    if present, search for Netflix Info table and add to results
    """
    results = None

    missing_data = check_for_missing_data(soup)
    if not missing_data:
        netflix_table = soup.find(id='netflix')
        if netflix_table:
            html_snippet = str(netflix_table)
            data = pd.read_html(html_snippet)
            results = ('Netflix Info', data)

    """
    Look for Premiere Date;
    if present, store as Result Date
    """
    try:
        premiere_date = soup.find('span', {'title': 'Premiere'})
        result_date = premiere_date.text
    except AttributeError:
        print(f'Premiere date not found for {title}\n')
        result_date = None
    else:
        print(f'Premiere Date: {result_date}\n')

    return title, results, result_date


def get_history_tables(soup: BeautifulSoup) -> List[tuple, pd.DataFrame]:
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
        results_list.append(('Netflix Movies', data))

    """
    Support for Top 10 Overall, Top 10 Kids, and Netflix Official List has been deprecated.
    
    Uncomment to re-enable:
    
    
    netflix_overall = soup.find(id='toc-netflix-1')
    if netflix_overall:
        html_snippet = str(netflix_overall)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Overall', data))
        
    netflix_kids = soup.select('#toc-netflix-40')
    
    if netflix_kids:
        html_snippet = str(netflix_kids)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Kids', data))

    netflix_official = soup.select('#toc-netflix-official')
    if netflix_official:
        html_snippet = str(netflix_official)
        data = pd.read_html(html_snippet)
        results_list.append(('Netflix Official', data))
    """

    if len(results_list) > 0:
        return results_list


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


def make_info_dfs():
    """
    Make Dataframes from all Info Pickles.

    Save the Info tables and premiere dates.

    :return: None
    """
    info_dict = {}
    premiere_dict = []

    """
    Load all Info pickles.
    """
    info_files = glob.glob(f'{PICKLE_DIR}/info/*.pickle')
    files_count = len(info_files)

    """
    Loop over all info files and create info dict.
    """
    counter = 1
    for file in info_files:
        if not file.split('/')[-1].startswith('!!!'):
            print(f'Working on {counter}/{files_count}')

            title, results, premiere_date = read_info_soup(file)

            if isinstance(results, tuple):
                print_green(f'Found Info data for {title}')
                info_dict[title] = results

            if premiere_date:
                premiere_dict.append({
                    'title': title,
                    'Premiere Date': premiere_date
                })

        counter += 1

    """
    Save results as JSON and Pickle.
    """
    save_pickle(info_dict, '!!!info_df_results!!!', extra_folder='summary')
    save_top10_dict(info_dict, '!!!info_df_results!!!.json')

    """
    Save premiere dates as CSV Dataframe and Pickle.
    """
    save_premiere_dates_df(premiere_dict)


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
    raise NotImplementedError


def make_country_dfs(dir=PICKLE_DIR):
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
    country_files = glob.glob(f'{dir}/language/*.pickle')
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
    save_pickle(country_dict, '!!!language_df_results!!!', extra_folder='summary')


def make_dfs():
    """
    Make all dataframes.

    Main Function.

    :return: None
    """
    make_info_dfs()
    make_history_dfs()
    make_country_dfs()

    print('\n\nResults saved.\n\n')


if __name__ == '__main__':
    make_dfs()
