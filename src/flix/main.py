import os

import requests
import re
from src.flix import BASE_URL, TEST_URL, PICKLE_DIR
from src.flix.utils import save_pickle, get_pickle_path, check_for_404
from slugify import slugify
from src.flix.data import NETFLIX_ORIGINALS
import time
from pathlib import Path
from src.flix.debug_messages import print_missing, print_found, print_pickle_exists, print_connection_error
from requests.exceptions import ConnectionError


def get_movie(title):
    print(f'Working on {title}')
    slug = slugify(title).replace('/', '')
    print(f'Slug: {slug}')

    pickle_path = get_pickle_path(slug)
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
                save_pickle(soup_data, slug)

            time.sleep(1)

    else:
        print_pickle_exists()


def flix_main():
    missing_titles = []

    for movie in NETFLIX_ORIGINALS:
        missing = get_movie(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!')


if __name__ == '__main__':
    flix_main()
