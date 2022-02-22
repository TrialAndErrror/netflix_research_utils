import os
from pathlib import Path
from src.flix import get_summary_dir, get_pickle_dir


def setup_directories():
    print('making directories')
    directories = ['history', 'info', 'language']
    for directory in directories:
        os.makedirs(Path(get_pickle_dir(), directory), exist_ok=True)
    get_summary_dir().mkdir(exist_ok=True)
