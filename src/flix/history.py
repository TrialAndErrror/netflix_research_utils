import time
import requests
from requests.exceptions import ConnectionError
from pathlib import Path
from slugify import slugify


from src.flix import BASE_URL, PICKLE_DIR
from src.flix.utils import save_pickle, get_pickle_path, check_for_404
from src.flix.data import NETFLIX_ORIGINALS
from src.flix.debug_messages import print_missing, print_found, print_pickle_exists, print_connection_error
from src.flix.process_pickle import make_dfs


def get_movie(title):
    print(f'Working on {title}')
    slug = slugify(title).replace('/', '')
    print(f'Slug: {slug}')

    pickle_path = get_pickle_path(slug, extra_folder='history')
    if not pickle_path.exists():
        try:
            response = requests.get(f'{BASE_URL}/{slug}/top10/')
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
                save_pickle(soup_data, slug, extra_folder='history')

            time.sleep(1)

    else:
        print_pickle_exists()


def flix_history():
    missing_titles = []

    for movie in NETFLIX_ORIGINALS:
        missing = get_movie(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='history')

    # pickle_history_dir = Path(PICKLE_DIR, 'history')
    make_dfs()


if __name__ == '__main__':
    flix_history()
