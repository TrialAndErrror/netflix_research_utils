import os
from pathlib import Path

from src.utils import write_file

from src.flix import PICKLE_DIR, SUMMARY_DIR
from src.flix.utils.directories import setup_directories
from src.flix.utils.slug_utils import slugify_nf_dict
from src.utils import read_file

from src.flix.functions.info import make_info_dfs, flix_info
from src.flix.functions.history import make_history_dfs, flix_history
from src.flix.functions.countries import make_country_dfs, flix_countries


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
    setup_directories()

    # """
    # Update titles where the slug does not match the FlixPatrol url.
    # """
    # slug_replace_dict, nf_id_dict = slugify_nf_dict(nf_id_dict)
    # write_file(slug_replace_dict, Path(SUMMARY_DIR, 'slug_replace_dict.json'))

    """
    Gather all pickles from FlixPatrol data.
    """
    print('FlixFetch: fetching movie info')
    flix_info(nf_id_dict)
    print('fetching movie history')
    flix_history(nf_id_dict)
    print('fetching movie countries')
    flix_countries(nf_id_dict)

    """
    Process pickles into DataFrames.
    """
    slug_replace_dict = {item['slug']: item['title'] for item in nf_id_dict}

    make_info_dfs(slug_replace_dict)
    make_history_dfs(slug_replace_dict)
    make_country_dfs(slug_replace_dict)

    print('\n\nResults saved.\n\n')


def flixpatrol_main():
    """
    Run all FlixPatrol functions on all data.

    FlixPatrol main function.

    :return: None
    """
    os.makedirs(PICKLE_DIR, exist_ok=True)
    nf_dict_path = Path(os.getcwd(), 'netflix_nametags.json')
    if nf_dict_path.exists():
        data = read_file(nf_dict_path)
        run_all(data)
    else:
        raise FileNotFoundError(
            'Missing netflix_nametags.json; cannot continue without list of Netflix Originals titles.'
        )


if __name__ == '__main__':
    flixpatrol_main()
