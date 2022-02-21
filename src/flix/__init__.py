from colorama import init
import os
from pathlib import Path
init()

BASE_URL = 'https://flixpatrol.com/title/'

TEST_URL = 'https://flixpatrol.com/title/cobra-kai/'

PICKLE_DIR = Path(os.getcwd(), 'pickle_jar')
SUMMARY_DIR = Path(os.getcwd(), 'summary')

