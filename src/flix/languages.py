from slugify import slugify
from src.flix.utils import get_pickle_path, check_for_404, save_pickle
import requests
import time
from src.flix.debug_messages import print_connection_error, print_found, print_missing, print_pickle_exists
from src.flix import BASE_URL
from src.flix.data import NETFLIX_ORIGINALS


def get_languages(title):
    print(f'Working on {title}')
    slug = slugify(title).replace('/', '')
    print(f'Slug: {slug}')

    pickle_path = get_pickle_path(slug, extra_folder='language')
    if not pickle_path.exists():
        try:
            response = requests.get(f'{BASE_URL}/{slug}/streaming/')
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
                save_pickle(soup_data, slug, extra_folder='language')

            time.sleep(1)

    else:
        print_pickle_exists()


def flix_languages():
    missing_titles = []

    for movie in NETFLIX_ORIGINALS:
        missing = get_languages(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')