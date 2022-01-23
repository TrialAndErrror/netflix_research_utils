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

    results_dir = Path(os.getcwd(), 'results')
    results_dir.mkdir(exist_ok=True)

    output_folder = Path(results_dir, f'Results {datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    output_folder.mkdir(exist_ok=True)
    final_df_path = Path(output_folder, 'final_df.csv')
    print(f'Saving Overall Dataframe to {final_df_path}')
    df.to_csv(str(final_df_path))

    countries = list(df['Country'].unique())
    countries_dir = Path(output_folder, 'country_dfs')
    countries_dir.mkdir(exist_ok=True)
    for country in countries:
        print(f'Saving Country Dataframe: {country}')
        country_df = df[df['Country'] == country]
        country_df_path = Path(countries_dir, f'{country}.csv')
        country_df.to_csv(str(country_df_path))

    print('List of Errors:')
    [print(item) for item in error_list]

    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    error_file = Path(output_folder, f'error_list {now}.txt')
    error_file.write_text('\n'.join(error_list))


def test_pickle(pickle_dir: str = PICKLES_DIR) -> PickleReader:
    pickle_folder = Path(pickle_dir)
    test_name = 'bruised.pickle'

    return PickleReader(Path(pickle_folder, test_name))


if __name__ == '__main__':
    run_all_pickles()
