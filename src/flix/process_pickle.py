import os

from src.flix.utils import load_pickle, save_pickle
from src.flix import PICKLE_DIR
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re
from debug_messages import print_green


def check_for_missing_data(obj):
    soup = BeautifulSoup(obj, "lxml")
    content_div = soup.find_all('div', {'class': 'content'})[-1]
    return not re.search('No streaming data', content_div)


def read_soup(filename):
    title = filename.split('.')[0]
    df = None
    obj = load_pickle(Path(PICKLE_DIR, filename))

    missing_data = check_for_missing_data(obj)

    if not missing_data:
        df = pd.read_html(obj)[-1]

    return title, df


def make_dfs():
    files = os.listdir(PICKLE_DIR)
    files_count = len(files)
    counter = 1

    df_dict = {}

    for file in files:
        print(f'Working on {counter}/{files_count}')
        title, df = read_soup(file)
        if df:
            print_green(f'Found top 10 data for {title}')
            df_dict[title] = df

        counter += 1

    save_pickle(df_dict, '!!!df_results!!!!')
    print('\n\nResults saved.\n\n')



if __name__ == '__main__':
    top_10_filename = 'red-notice.pickle'
    no_results_filename = 'quincy.pickle'
    read_soup(no_results_filename)
