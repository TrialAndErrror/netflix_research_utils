import os

import pandas as pd
from pathlib import Path
from src.pickle_farm.models import PickleReader
from datetime import datetime
from src.pickle_farm import LANGUAGE_COLUMNS, PICKLES_DIR


def run_all_pickles(pickle_dir: str = PICKLES_DIR):
    pickle_folder = Path(pickle_dir)

    all_pickles = pickle_folder.iterdir()

    all_entries = []
    error_list = []
    for pickle in all_pickles:
        obj = PickleReader(pickle)
        if obj.title:
            all_entries.extend(obj.make_dataframe_entries(LANGUAGE_COLUMNS))
        else:
            error_list.append(str(pickle).split('/')[-1].split('.')[-2])

    df = pd.DataFrame.from_records(all_entries)
    df.to_csv('final_df.csv')

    print('List of Errors:')
    [print(item) for item in error_list]

    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    error_file = Path(os.getcwd(), f'error_list {now}.txt')
    error_file.write_text('\n'.join(error_list))


def test_pickle(pickle_dir: str = PICKLES_DIR) -> PickleReader:
    pickle_folder = Path(pickle_dir)
    test_name = 'bruised.pickle'

    return PickleReader(Path(pickle_folder, test_name))


if __name__ == '__main__':
    run_all_pickles()
