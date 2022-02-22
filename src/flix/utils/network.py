import re

import requests
import time

from http.client import RemoteDisconnected
from ssl import SSLEOFError
from requests.exceptions import ConnectionError

from src.flix.utils.pickle_utils import get_pickle_path, save_pickle
from src.flix.utils.debug_messages import print_connection_error, print_missing, print_pickle_exists, print_found
from src.flix import BASE_URL


def get_data(slug, url, extra_folder=''):
    """
    Get  data for an individual title.

    :param slug: str
    :param url: str
    :param extra_folder: str
    :return: None
    """
    s = requests.session()
    print(f'Working on {slug}')

    """
    Check if pickle exists.
    """
    pickle_path = get_pickle_path(slug, extra_folder=extra_folder)
    if not pickle_path.exists():
        """
        If pickle does not exist, fetch data from site.
        """
        try:
            response = s.get(f'{BASE_URL}{slug}/{url}')
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
                save_pickle(soup_data, slug, extra_folder=extra_folder)

            time.sleep(1)

    else:
        print_pickle_exists()


def check_for_404(soup_data):
    return re.search('Page Not Found', soup_data)
