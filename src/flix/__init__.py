import os
from pathlib import Path
from colorama import init
init()

BASE_URL = 'https://flixpatrol.com/title/'

TEST_URL = 'https://flixpatrol.com/title/cobra-kai/'


def get_summary_dir():
    return Path(os.getcwd(), 'summary')


def get_pickle_dir():
    return Path(os.getcwd(), 'pickle_jar')
