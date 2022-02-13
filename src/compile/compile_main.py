import pandas as pd
from pathlib import Path
import os
from src.utils import read_file
from clean_gt_data import merge_unogs_and_gt, clean_gt
from clean_flix_top10 import clean_flixpatrol_data
from clean_flix_countries import clean_flix_countries
from clean_unogs_data import clean_unogs
from make_groups import perform_make_exclusive
from datetime import datetime

INPUT_DIR_NAME = 'input'
INPUT_PATH = Path(os.getcwd(), INPUT_DIR_NAME)

PARTS_DIR_NAME = 'parts'
PARTS_PATH = Path(os.getcwd(), PARTS_DIR_NAME)

FILE_PATH = {
    'unogs': Path(INPUT_PATH, 'final_unogs_df.csv'),
    'trends': Path(INPUT_PATH, 'google_trends_data.csv'),
    'nf_dict': Path(INPUT_PATH, 'nf_dict.json'),
    'flix_top10': Path(INPUT_PATH, '!!!history_df_results!!!.pickle'),
    'flix_country': Path(INPUT_PATH, '!!!language_df_results!!!.pickle')
}


def check_for_required_files():
    INPUT_PATH.mkdir(exist_ok=True)
    PARTS_PATH.mkdir(exist_ok=True)

    for file in FILE_PATH.values():
        if not file.exists():
            raise FileNotFoundError(f'Missing Required Input File: {file}')


def create_output_folder():
    output_folder = Path(os.getcwd(), f'Compile Results: {datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    output_folder.mkdir(exist_ok=True)
    return output_folder


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
    Load UNOGS dataframe and Google Trends Dataframe
    """
    unogs_df = load_or_create_unogs_df()

    nf_originals = read_file(FILE_PATH['nf_dict'])
    grouped_df = None
    if nf_originals:
        grouped_df = load_or_create_grouped_df(nf_originals, unogs_df)

    """
    Load Google Trends Dataframe
    """
    print('\nLoading Google Trends Data')
    gt_data = clean_gt(FILE_PATH['trends'])

    """
    Merge UNOGS and Google Trends data
    """
    final_df = merge_unogs_and_google_trends(unogs_df, gt_data)

    if isinstance(grouped_df, pd.DataFrame):
        merge_grouped_and_google_trends(grouped_df, gt_data)

    """
    Load and Merge FlixPatrol Top 10 Overall Data
    """
    print('\nLoading FlixPatrol Top 10 Data')
    flixpatrol_points_dataframe = clean_flixpatrol_data(FILE_PATH['flix_top10'])
    final_df = final_df.merge(flixpatrol_points_dataframe, left_on='slug', right_on='level_0', how='left')
    final_df = final_df[(final_df['Country'] == final_df['level_1']) | (final_df['level_1'].isna())]
    final_df.to_csv(Path(PARTS_PATH, '[p]unogs_gt_and_top10.csv'))

    if isinstance(grouped_df, pd.DataFrame):
        grouped_df = grouped_df.merge(flixpatrol_points_dataframe, left_on='slug', right_on='level_0', how='left')
        grouped_df = grouped_df[(grouped_df['Country'] == grouped_df['level_1']) | (grouped_df['level_1'].isna())]
        grouped_df.to_csv(Path(PARTS_PATH, '[p]grp_unogs_gt_and_top10.csv'))

    # flixpatrol_points_dataframe = clean_flixpatrol_data(FILE_PATH['flix_top10'])
    # final_df = final_df.merge(flixpatrol_points_dataframe,
    #                           left_on=['slug', 'Country'],
    #                           right_on=['level_0', 'level_1'],
    #                           how='left')
    # final_df.to_csv(Path(PARTS_PATH, '[p]unogs_gt_and_top10.csv'))
    #
    # if isinstance(grouped_df, pd.DataFrame):
    #     grouped_df = grouped_df.merge(flixpatrol_points_dataframe,
    #                                   left_on=['slug', 'Country'],
    #                                   right_on=['level_0', 'level_1'],
    #                                   how='left')
    #     grouped_df.to_csv(Path(PARTS_PATH, '[p]grp_unogs_gt_and_top10.csv'))

    """
    Load and Merge FlixPatrol Countries Data
    """
    print('\nLoading FlixPatrol Countries Data')
    flixpatrol_countries_dataframe = clean_flix_countries(FILE_PATH['flix_country'])
    final_df = final_df.merge(flixpatrol_countries_dataframe, left_on='slug', right_index=True, how='left')
    final_df.to_csv(Path(PARTS_PATH, '[p]unogs_gt_top10_and_countries.csv'))

    if isinstance(grouped_df, pd.DataFrame):
        grouped_df = grouped_df.merge(flixpatrol_countries_dataframe, left_on='slug', right_index=True, how='left')
        grouped_df.to_csv(Path(PARTS_PATH, '[p]grp_unogs_gt_top10_and_countries.csv'))

    """
    Save Final Results
    """
    output_folder = create_output_folder()

    final_path = Path(output_folder, "final_compiled_data.csv")
    grouped_path = Path(output_folder, "grp_compiled_data.csv")

    print(f'\nSaving Final Dataframe to {final_path}')
    final_df.to_csv(final_path)
    grouped_df.to_csv(grouped_path)

    """
    Filter data down to Netflix Originals data only and save.
    """
    if nf_originals:
        final_nfo_path = Path(output_folder, "final_netflix_original_data.csv")
        print(f'\nSaving Final Netflix Originals Dataframe to {final_nfo_path}')
        final_nf_dict = final_df[final_df['title'].isin(nf_originals.keys())]
        final_nf_dict.to_csv(final_nfo_path)
    else:
        print(
            'No netflix data found. '
            'Include nf_dict.json if '
            'you want to filter to '
            'netflix originals only.'
        )

    print('Compile Complete.')


def merge_with_gt(df, gt_data, filename):
    df_path = Path(PARTS_PATH, filename)

    if not df_path.exists():
        result = merge_unogs_and_gt(df, gt_data)
        result.to_csv()
    else:
        result = pd.read_csv(df_path)

    return result


def merge_grouped_and_google_trends(grouped_df, gt_data):
    return merge_with_gt(grouped_df, gt_data, '[p]grp_unogs_and_gt.csv')


def merge_unogs_and_google_trends(unogs_df, gt_data):
    return merge_with_gt(unogs_df, gt_data, '[p]unogs_and_gt.csv')


def load_or_create_unogs_df():
    print('\nLoading UNOGS Data')
    unogs_df_path = Path(PARTS_PATH, '[p]unogs_df.csv')

    if not unogs_df_path.exists():
        unogs_df = clean_unogs(FILE_PATH['unogs'])
        unogs_df.to_csv(unogs_df_path)
    else:
        unogs_df = pd.read_csv(unogs_df_path)

    return unogs_df


def load_or_create_grouped_df(nf_originals, unogs_df):
    print('\nGrouping UNOGS Data')
    grouped_df_path = Path(PARTS_PATH, '[p]grp_unogs_df.csv')
    if not grouped_df_path.exists():
        grouped_df = unogs_df.copy()
        grouped_nf_df = grouped_df[grouped_df['title'].isin(nf_originals.keys())]
        grouped_df = perform_make_exclusive(grouped_nf_df)
        grouped_df.to_csv(grouped_df_path)
    else:
        grouped_df = pd.read_csv(grouped_df_path)

    return grouped_df


if __name__ == '__main__':
    compile_main()
