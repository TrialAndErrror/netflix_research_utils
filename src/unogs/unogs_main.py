from src.unogs.file_commands import load_netflix_nametags, setup_directories, load_replacements
from src.unogs.run_options import run_with_limit, run_all_movies
from src.unogs import DEBUG
from src.pickle_farm.farmer import run_all_pickles


def get_subs_and_dubs():
    """
    Main function.

    Loads data from json file, then loops through loaded data to get subbed and dubbed
    languages for each movie in loaded data.

    :return: None
    """
    pickle_folder = setup_directories()

    nf_dict = load_netflix_nametags()

    if DEBUG:
        run_with_limit(nf_dict)
    else:
        run_all_movies(nf_dict)

    return run_all_pickles(pickle_folder, nf_dict, load_replacements())


def unogs_main():
    return get_subs_and_dubs()


if __name__ == '__main__':
    unogs_main()
