import os

import pandas as pd
from pathlib import Path
from src.pickle_farm.models import PickleReader
from datetime import datetime
from src.pickle_farm import LANGUAGE_COLUMNS, PICKLES_DIR, LANG_REPLACEMENTS, ENABLE_REPLACEMENTS


def run_all_pickles(pickle_dir: Path or str = PICKLES_DIR):
    """
    Process all pickles and save as dataframes.

    :return: None
    """

    """
    Set up directories
    """
    pickle_folder = Path(pickle_dir)
    output_folder = setup_dirs()

    """
    Process all pickles from pickle_folder, returning a dataframe and list of errors
    """
    df, error_list = process_pickles_into_df(pickle_folder.iterdir())

    """
    Save dataframe to output folder
    Also save country dataframes to a subfolder in the output folder
    """
    save_dataframes(df, output_folder)

    """
    Save error list to output folder
    """
    save_error_list(error_list, output_folder)


def setup_dirs():
    """
    Setup folders for saving data to.
    """

    """
    Make sure that the overall Results directory exists.
    """
    results_dir = Path(os.getcwd(), 'results')
    results_dir.mkdir(exist_ok=True)

    """
    Create directory for current results
    """
    output_folder = Path(results_dir, f'Results {datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    output_folder.mkdir(exist_ok=True)

    return output_folder


def save_error_list(error_list, output_folder):
    """
    Save error list to text file.

    :return: None
    """
    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    error_file = Path(output_folder, f'error_list {now}.txt')
    error_file.write_text('\n'.join(error_list))


def save_dataframes(df, output_folder):
    """
    Save Total Dataframe
    Save Country Dataframes to subfolder

    :return: None
    """

    """
    Save Total Dataframe
    """
    final_df_path = Path(output_folder, 'final_df.csv')
    print(f'Saving Overall Dataframe to {final_df_path}')
    df.to_csv(str(final_df_path))

    """
    Setup Country list and subfolder
    """
    countries = list(df['Country'].unique())
    countries_dir = Path(output_folder, 'country_dfs')
    countries_dir.mkdir(exist_ok=True)

    """
    Iterate over country list, saving each dataframe
    """
    for country in countries:
        print(f'Saving Country Dataframe: {country}')
        country_df = df[df['Country'] == country]
        country_df_path = Path(countries_dir, f'{country}.csv')
        country_df.to_csv(str(country_df_path))


def process_pickles_into_df(all_pickles):
    """
    Process all pickle files into one dataframe and return error list.

    :return: pd.DataFrame, list
    """

    all_entries = []
    error_list = []

    """
    Create PickleReader object for each pickle;
    append the dataframe entries to the all_entries list.
    """
    for pickle in all_pickles:
        obj = PickleReader(pickle)

        """
        Check to see if object has a title;
        If there is no title, that means there is no data, and so add to errors list.
        """
        
        if obj.title:
            """
            If replacements are enabled, make them now before making dataframe entries.
            """
            if ENABLE_REPLACEMENTS:
                for key, value in LANG_REPLACEMENTS.items():
                    obj.replace_language(key, value)

            all_entries.extend(obj.make_dataframe_entries(LANGUAGE_COLUMNS))
        else:
            error_list.append(str(pickle).split('/')[-1].split('.')[-2])

    """
    Create DataFrame from all_entries list
    """
    df = pd.DataFrame.from_records(all_entries)

    return df, error_list


def test_pickle(pickle_dir: str = PICKLES_DIR) -> PickleReader:
    """
    Test function to verify PickleReader functionality

    :return: PickleReader
    """
    pickle_folder = Path(pickle_dir)
    test_name = 'bruised.pickle'

    return PickleReader(Path(pickle_folder, test_name))


if __name__ == '__main__':
    run_all_pickles()
