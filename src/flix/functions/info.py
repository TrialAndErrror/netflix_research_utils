import glob
import os
from pathlib import Path
from typing import Tuple

import pandas as pd
from bs4 import BeautifulSoup

from src.flix import PICKLE_DIR, SUMMARY_DIR
from src.flix.utils.debug_messages import print_green
from src.flix.functions.utils import check_for_missing_data
from src.flix.utils.network import get_data
from src.flix.utils.pickle_utils import save_pickle, load_pickle
from src.utils import write_json


def flix_info(nf_id_dict):
    """
    Get info pages for all movies in netflix ID dict.

    :param nf_id_dict: dict
    :return: None
    """
    missing_titles = []
    total_count = len(nf_id_dict)
    print(f'Working on {total_count} Movies...')

    """
    Loop over all titles
    """
    count = 1
    for title in nf_id_dict:
        print(f'{count}/{total_count}')

        if title['slug'] == 'EXCLUDE':
            """
            Check if title is excluded.

            This occurs if the slug on FlixPatrol is not for this title, and there is no FlixPatrol page for this title.
            """
            print(f'Skipping {title["title"]} based on exclusion policy.\n')
        else:
            """
            Check if data is present by looking for "Missing Data" string in page
            """
            missing = get_data(title['slug'], url='', extra_folder='info')

            if missing:
                """
                If title is missing, add to missing titles list and save each time a title is added.
                """
                missing_titles.append(missing)
                save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')

        count += 1


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
            results = data[0]

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


def make_info_dfs(slug_replace_dict):
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

            if isinstance(results, pd.DataFrame):
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
    save_top10_dict(info_dict, 'info_results.json')

    """
    Save premiere dates as CSV Dataframe and Pickle.
    """
    title_replace_dict = {v: k for k, v in slug_replace_dict.items()}
    save_premiere_dates_df(premiere_dict, title_replace_dict)


def save_premiere_dates_df(premiere_dict, title_replace_dict):
    premiere_df = pd.DataFrame.from_records(premiere_dict).infer_objects()
    premiere_df['Premiere Date'] = pd.to_datetime(premiere_df['Premiere Date'], format='%m/%d/%Y')

    valid_df = premiere_df[premiere_df['Premiere Date'] > '01/01/2004']

    valid_df = valid_df.rename({'title': 'slug'}, axis=1)
    valid_df['title'] = valid_df['slug'].apply(lambda x: title_replace_dict.get(x, 'Unknown'))

    valid_df.to_csv(Path(SUMMARY_DIR, 'premiere_dates_df.csv'))


def save_top10_dict(data, filename):
    export_dict = {title: df.to_dict() for title, df in data.items()}
    write_json(export_dict, Path(os.getcwd(), SUMMARY_DIR, filename))
