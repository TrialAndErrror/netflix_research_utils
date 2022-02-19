from src.flix.utils import get_pickle_path, check_for_404, save_pickle, get_slug
import requests
import time
from src.flix.debug_messages import print_connection_error, print_found, print_missing, print_pickle_exists
from src.flix import BASE_URL
from http.client import RemoteDisconnected
from ssl import SSLEOFError


def get_countries(title):
    """
    Get FlixPatrol Top10 by Country data for an individual title.

    :param title: str
    :return: None
    """
    s = requests.session()
    print(f'Working on {title}')

    """
    Get slug for title
    """
    slug = get_slug(title)
    print(f'Slug: {slug}')

    """
    Check if pickle exists.
    """
    pickle_path = get_pickle_path(slug, extra_folder='language')
    if not pickle_path.exists():
        """
        If pickle does not exist, fetch data from site.
        """
        try:
            response = s.get(f'{BASE_URL}{slug}/streaming/')
        except ConnectionError:
            print_connection_error()
        except RemoteDisconnected:
            print_connection_error()
        except SSLEOFError:
            print_connection_error()
        else:
            soup_data = response.text

            """
            Check for 404
            """
            movie_not_found = check_for_404(soup_data)

            """
            If movie not found, print to terminal.
            Otherwise, save data as pickle
            """
            if movie_not_found:
                print_missing()
                return slug
            else:
                print_found()
                save_pickle(soup_data, slug, extra_folder='language')

            time.sleep(1)

    else:
        print_pickle_exists()


def flix_countries(nf_id_dict):
    missing_titles = []

    for movie in nf_id_dict:
        missing = get_countries(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!', extra_folder='summary')
