import os

import requests
from src.flix import BASE_URL, PICKLE_DIR
from src.flix.utils import save_pickle, get_pickle_path, check_for_404
from slugify import slugify
from src.flix.data import NETFLIX_ORIGINALS
import time
from pathlib import Path
from src.flix.debug_messages import print_missing, print_found, print_pickle_exists, print_connection_error
from requests.exceptions import ConnectionError
from src.flix.history import flix_history
from src.flix.languages import flix_languages
from src.flix.process_pickle import make_dfs


def get_movie(title):
    print(f'Working on {title}')
    slug = slugify(title).replace('/', '')
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


def flix_main():
    missing_titles = []

    for movie in NETFLIX_ORIGINALS:
        missing = get_movie(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')


def run_all():
    print('making directories')
    directories = ['history', 'info', 'summary', 'language']

    for dir in directories:
        os.makedirs(dir, exist_ok=True)

    print('fetching movie info')
    flix_main()
    print('fetching movie history')
    flix_history()
    print('fetching movie languages')
    flix_languages()

    make_dfs()


if __name__ == '__main__':
    run_all()
