"""
Initial Configuration
"""

import datetime
from pathlib import Path
import os
"""
Testing Variables:

DEBUG and MAX COUNT are global constants used to limit number of movies to download.
Set DEBUG to False to allow it to get all movies in the json_file.
"""

DEBUG = False
MAX_COUNT = 500

"""
Filename Setup:

Filename determines the name of the results file.
Currently set to "results" with a timestamp at the end.

Filenames are stored as a function so the timestamp can be called when the filename is needed.
"""


def add_timestamp():
    return datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")


def make_results_filename():
    return f'results_{add_timestamp()}.json'


def make_processed_filename():
    return f'movies_processed_{add_timestamp()}.json'


def make_all_data_filename():
    return f'all_data_{add_timestamp()}.json'


"""
Directory Setup:

Defines the directories for input and output data.
"""
home_dir = Path(os.getcwd())

INPUT_FOLDER = Path(home_dir, 'inputs')
OUTPUT_FOLDER = Path(home_dir, 'results')
PROCESSED_FOLDER = Path(home_dir, 'processed')
ALL_DATA = Path(home_dir, 'all_data')
DF_DATA = Path(home_dir, 'df_data')
