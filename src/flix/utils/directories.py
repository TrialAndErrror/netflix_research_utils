import os
from pathlib import Path

from src.flix import PICKLE_DIR, SUMMARY_DIR


def setup_directories():
    print('making directories')
    directories = ['history', 'info', 'language']
    for dir in directories:
        os.makedirs(Path(PICKLE_DIR, dir), exist_ok=True)
    SUMMARY_DIR.mkdir(exist_ok=True)