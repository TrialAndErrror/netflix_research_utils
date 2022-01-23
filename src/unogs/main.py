from src.unogs.file_commands import load_from_json_data, save_results, setup_directories
from src.unogs.run_options import run_with_limit, run_all_movies
from src.unogs import DEBUG
from src.unogs.process_results import process_into_country_dicts
from src.unogs.process_df import process_into_country_dfs


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

        save_results(movie_data)

        process_into_country_dicts()

        process_into_country_dfs()


if __name__ == '__main__':
    setup_directories()
    get_subs_and_dubs()
