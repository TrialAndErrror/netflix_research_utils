from src.unogs.file_commands import load_from_json_data, setup_directories
from src.unogs.run_options import run_with_limit, run_all_movies
from src.unogs import DEBUG
from src.pickle_farm.farmer import run_all_pickles
from pathlib import Path
from src.unogs import OUTPUT_FOLDER


def get_subs_and_dubs():
    """
    Main function.

    Loads data from json file, then loops through loaded data to get subbed and dubbed
    languages for each movie in loaded data.

    :return: None
    """
    nf_dict = load_from_json_data('api_data.json')
    if nf_dict:

        if DEBUG:
            movie_data = run_with_limit(nf_dict)
        else:
            movie_data = run_all_movies(nf_dict)

    return run_all_pickles((Path(OUTPUT_FOLDER, 'pickles')))


def unogs_main():
    setup_directories()
    get_subs_and_dubs()


if __name__ == '__main__':
    unogs_main()
