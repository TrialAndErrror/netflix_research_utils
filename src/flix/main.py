import os

import requests
from src.flix import BASE_URL, PICKLE_DIR
from src.flix.utils import save_pickle, get_pickle_path, check_for_404, get_slug
from slugify import slugify
from src.flix.data import NETFLIX_ORIGINALS
import time
from pathlib import Path
from src.flix.debug_messages import print_missing, print_found, print_pickle_exists, print_connection_error
from requests.exceptions import ConnectionError
from src.flix.history import flix_history
from src.flix.languages import flix_countries
from src.flix.process_pickle import make_dfs
from src.utils import read_file


def get_movie(title):
    print(f'Working on {title}')
    slug = get_slug(title)
    print(f'Slug: {slug}')

    pickle_path = get_pickle_path(slug, extra_folder='info')

    if not pickle_path.exists():
        try:
            response = requests.get(f'{BASE_URL}/{slug}')
        except ConnectionError:
            print_connection_error()
        else:
            soup_data = response.text

            movie_not_found = check_for_404(soup_data)

            if movie_not_found:
                print_missing()
                return slug
            else:
                print_found()
                save_pickle(soup_data, slug, extra_folder='info')

            time.sleep(1)

    else:
        print_pickle_exists()


def flix_main(nf_id_dict):
    missing_titles = []
    total_count = len(nf_id_dict)
    print(f'Working on {total_count} Movies...')
    count = 1
    for movie in nf_id_dict:
        print(f'{count}/{total_count}')
        missing = get_movie(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')

        count += 1


def update_movie_titles(nf_dict):
    update_dict = {
        'the-guilty': 'the-guilty-2021',
        'house-arrest': 'house-arrest-2019',
        'outlaws-netflix-original': 'outlaws'
    }

    for old_title, new_title in update_dict:
        nf_dict[new_title] = nf_dict.pop(old_title)

    return nf_dict


def run_all(nf_id_dict=NETFLIX_ORIGINALS):
    """
    Run all FlixPatrol steps.

    Main function.

    :param nf_id_dict: dict
    :return: None
    """

    """
    Setup directories
    """
    print('making directories')
    directories = ['history', 'info', 'summary', 'language']

    for dir in directories:
        os.makedirs(Path(PICKLE_DIR, dir), exist_ok=True)

    """
    Update titles where the slug does not match the FlixPatrol url.
    """
    nf_id_dict = update_movie_titles(nf_id_dict)

    """
    Gather all pickles from FlixPatrol data.
    """
    print('FlixFetch: fetching movie info')
    flix_main(nf_id_dict)
    print('fetching movie history')
    flix_history(nf_id_dict)
    print('fetching movie countries')
    flix_countries(nf_id_dict)

    """
    Process pickles into DataFrames.
    """
    make_dfs()


if __name__ == '__main__':
    os.makedirs(PICKLE_DIR, exist_ok=True)
    nf_dict_path = Path(os.getcwd(), 'nf_dict.json')
    if nf_dict_path.exists():
        data = read_file(nf_dict_path)
        run_all(data)
    else:
        run_all()
