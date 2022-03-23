from pathlib import Path
from typing import Optional, List, Text

import pandas as pd
from bs4 import BeautifulSoup
from slugify import slugify

from src.flix import get_summary_dir, get_pickle_dir
from src.flix.utils.debug_messages import print_red, print_green
from src.flix.utils.pickle_utils import save_pickle, load_pickle
from src.flix.utils.network import get_data

from src.utils import write_json


def flix_countries(nf_id_dict):
    missing_titles = []

    for title in nf_id_dict:
        if title['slug'] == 'EXCLUDE':
            """
            Check if title is excluded.

            This occurs if the slug on FlixPatrol is not for this title, and there is no FlixPatrol page for this title.
            """
            print(f'Skipping {title["title"]} based on exclusion policy.\n')
        else:
            missing = get_data(title['slug'], url='streaming/', extra_folder='country')

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


def read_country_soup(filename: Path) -> (Text, List):
    """
    Load pickle file, convert data to soup object, and get countries from the Netflix Countries table.

    :param filename: str
    :return: (str, list)
    """

    """
    Load pickle and initialize soup object.
    """
    # pickle_path = Path(os.getcwd(), 'pickle_jar', 'language', filename)
    # title = filename.split('.')[0].split('/')[-1]
    title = filename.stem
    obj: str = load_pickle(filename)
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


def make_country_dfs(nf_dict):
    """
    Make Dataframes from all Country Pickles.

    Return the Info tables and premiere dates.

    :return: None
    """

    """
    Load History pickles.
    """
    print('Working on Countries')
    country_dict = {}

    pickle_file_list = [f'{item["slug"]}' for item in nf_dict]
    slugged_title_list = [f'{slugify(item["title"])}' for item in nf_dict]
    country_files = [item for item in Path(get_pickle_dir(), "country").iterdir() if (item.stem in pickle_file_list or item.stem in slugged_title_list)]
    files_count = len(country_files)
    counter = 1

    """
    Loop over country files and make dict of results.
    """
    for file in country_files:
        print(f'Working on {counter}/{files_count}')
        title, results = read_country_soup(file)
        if isinstance(results, list):
            print_green(f'Found Country data for {title}')
            country_dict[title] = results

        counter += 1

    write_json(country_dict, Path(get_summary_dir(), 'country_results.json'))
