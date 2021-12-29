import logging
from pathlib import Path
import os
from datetime import datetime
from colorama import init, Fore, Back, Style
init()

WON_DEBUG = False

"""
Main Site URL
"""
BASE_URL = "https://www.whats-on-netflix.com/originals/movies/"


"""
File Setup:

This is the directory that the resulting file will be created in.

We check to make sure it exists, and create it if it does not.
"""
OUTPUT_FILE_DIR = Path(os.getcwd(), 'output')
os.makedirs(OUTPUT_FILE_DIR, exist_ok=True)


def get_output_filename():
    return Path(OUTPUT_FILE_DIR, f'nf_originals_dict {datetime.now().strftime("%m-%d-%Y, %H:%M:%S")}')


"""
Logging Setup, for errors and troubleshooting
"""
logging.basicConfig(
    level=logging.DEBUG,
    filename='won_logs.log',
    format='%(asctime)s %(message)s',
)


def log_error(message):
    print(Fore.RED + message)
    print(Style.RESET_ALL)
    logging.error(message)


def log_debug(message):
    print(Fore.CYAN + message)
    print(Style.RESET_ALL)
    logging.debug(message)
