import pandas as pd
from pathlib import Path
import os

from clean_gt_data import merge_unogs_and_gt, clean_gt
from clean_flix_top10 import clean_flixpatrol_data
from clean_flix_countries import clean_flix_countries
from clean_unogs_data import clean_unogs
INPUT_DIR_NAME = 'input'
INPUT_PATH = Path(os.getcwd(), INPUT_DIR_NAME)

FILE_PATH = {
    'unogs': Path(INPUT_PATH, 'final_unogs_df.csv'),
    'trends': Path(INPUT_PATH, 'google_trends_data.csv'),
    'flix_top10': Path(INPUT_PATH, '!!!history_df_results!!!.pickle'),
    'flix_country': Path(INPUT_PATH, '!!!language_df_results!!!.pickle')
}


def check_for_required_files():
    INPUT_PATH.mkdir(exist_ok=True)

    for file in FILE_PATH.values():
        if not file.exists():
            raise FileNotFoundError(f'Missing Required Input File: {file}')


def compile_main():
    """
    Compile all dataframes into one complete dataset.

    Saves dataframes as final_compiled_data.csv in the current directory.

    :return: None
    """

    """
    Setup directories and make sure all required files are present
    """
    check_for_required_files()

    """
    Load UNOGS dataframe
    """
    unogs_df = clean_unogs(FILE_PATH['unogs'])
    gt_data = clean_gt(FILE_PATH['trends'])

    """
    Merge UNOGS and Google Trends to create Final DF
    """
    final_df = merge_unogs_and_gt(unogs_df, gt_data)

    """
    Load and Merge FlixPatrol Top 10 Overall Data
    """
    flixpatrol_points_dataframe = clean_flixpatrol_data(FILE_PATH['flix_top10'])
    final_df = final_df.merge(flixpatrol_points_dataframe, left_on='slug', right_on='level_0', how='left')

    """
    Load and Merge FlixPatrol Countries Data
    """
    flixpatrol_countries_dataframe = clean_flix_countries(FILE_PATH['flix_countries'])
    final_df = final_df.merge(flixpatrol_countries_dataframe, left_on='slug', right_index=True, how='left')

    """
    Save Final Results
    """
    final_df.to_csv('final_compiled_data.csv')


if __name__ == '__main__':
    compile_main()
