from pathlib import Path
import numpy as np
import sys
import pickle
from src.unogs import INPUT_FOLDER, OUTPUT_FOLDER, PROCESSED_FOLDER, PICKLE_FOLDER
from src.utils import read_file, write_file


def setup_directories():
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    PROCESSED_FOLDER.mkdir(exist_ok=True)
    PICKLE_FOLDER.mkdir(exist_ok=True)


def load_from_json_data(filename: str):
    """
    Load file from JSON data.

    Option 1) Load from filename provided in parameters, which should be data from the
    UNOGS API

    Option 2) Load form nf_dict, which is a dictionary in the format of:
    {
        Movie Name: Netflix ID
    }

    If Option 1 is used, the script will create nf_dict and save it.

    :param filename: str
    :return: dict
    """
    nf_path = Path(INPUT_FOLDER, 'nf_dict.json')

    """
    If nf_dict doesn't exist, create it
    """
    if not nf_path.exists():
        create_nf_data_file(filename, nf_path)

    """
    Load from nf_dict
    """
    data = read_file(nf_path)
    if data:
        return data
    else:
        print(f'Error: File {filename} not found. Place data in the inputs folder: {INPUT_FOLDER}')
        sys.exit()


def create_nf_data_file(filename, nf_path):
    """
    Load from filename provided
    """
    path = Path(INPUT_FOLDER, filename)
    json_data = read_file(path)
    if not json_data:
        print(f'Unable to locate NF Data File; Make sure that you have the data saved as {path}')
        sys.exit()

    """
    Split into lists of movies, then create dictionary.
    """
    all_movies = list(np.concatenate([item['results'] for item in json_data]).flat)
    nf_lookup = {item['title']: item['nfid'] for item in all_movies}
    """
    Save nf_dict
    """
    write_file(nf_lookup, nf_path)


# def save_results(movie_data: dict):
#     """
#     Save results to json file.
#
#     Filename is provided by global RESULTS_FILENAME constant.
#
#     :param movie_data: dict
#     :return: None
#     """
#     write_file(movie_data, Path(OUTPUT_FOLDER, make_results_filename()))


def save_pickle(data, filename: str):
    path = Path(PICKLE_FOLDER, filename)

    with open(path, 'w+b') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    path = Path(PICKLE_FOLDER, filename)
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data
