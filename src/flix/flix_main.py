import os
from pathlib import Path


from src.flix import PICKLE_DIR
from src.flix.functions.info import make_info_dfs
from src.flix.functions.history import make_history_dfs
from src.flix.functions.countries import make_country_dfs
from src.utils import read_file


def run_all(nf_id_dict):
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
    #
    # """
    # Update titles where the slug does not match the FlixPatrol url.
    # """
    # nf_id_dict = slugify_nf_dict(nf_id_dict)
    # """
    # Gather all pickles from FlixPatrol data.
    # """
    # print('FlixFetch: fetching movie info')
    # flix_info(nf_id_dict)
    # print('fetching movie history')
    # flix_history(nf_id_dict)
    # print('fetching movie countries')
    # flix_countries(nf_id_dict)

    """
    Process pickles into DataFrames.
    """
    # make_info_dfs()
    # make_history_dfs()
    make_country_dfs()

    print('\n\nResults saved.\n\n')


def flixpatrol_main():
    """
    Run all FlixPatrol functions on all data.

    FlixPatrol main function.

    :return: None
    """
    os.makedirs(PICKLE_DIR, exist_ok=True)
    nf_dict_path = Path(os.getcwd(), 'nf_dict.json')
    if nf_dict_path.exists():
        data = read_file(nf_dict_path)
        run_all(data)
    else:
        raise FileNotFoundError('Missing nf_dict.json; cannot continue without list of Netflix Originals titles.')


if __name__ == '__main__':
    flixpatrol_main()
