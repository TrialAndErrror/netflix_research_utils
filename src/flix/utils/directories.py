import os
from pathlib import Path
from src.flix import get_summary_dir, get_pickle_dir


def setup_directories():
    print('making directories')
    directories = ['history', 'info', 'language']
    for dir in directories:
        os.makedirs(Path(get_pickle_dir(), dir), exist_ok=True)
    get_summary_dir().mkdir(exist_ok=True)