import logging

from src.file_commands import load_from_json_data, save_results, setup_directories
from src.run_options import DEBUG, run_with_limit, run_all_movies


"""
Logging Setup:

Logging allows error messages to be logged along the way.
"""
logging.basicConfig(
    level=logging.DEBUG,
    filename='logs.log',
    format='%(asctime)s %(message)s',
)


def get_subs_and_dubs():
    """
    Main function.

    Loads data from json file, then loops through loaded data to get subbed and dubbed
    languages for each movie in loaded data.

    :return: None
    """
    nf_dict = load_from_json_data('api_data.json')

    if DEBUG:
        movie_data = run_with_limit(nf_dict)
    else:
        movie_data = run_all_movies(nf_dict)

    save_results(movie_data)


if __name__ == '__main__':
    setup_directories()
    get_subs_and_dubs()
