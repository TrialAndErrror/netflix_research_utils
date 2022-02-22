import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.compile.functions.clean_gt_data import merge_unogs_and_gt
from src.compile.functions.clean_unogs_data import clean_unogs
from src.compile.functions.make_groups import perform_make_exclusive

INPUT_DIR_NAME = 'inputs'
INPUT_PATH = Path(os.getcwd(), INPUT_DIR_NAME)
PARTS_DIR_NAME = 'parts'
PARTS_PATH = Path(os.getcwd(), PARTS_DIR_NAME)



def check_for_required_files():
    file_path = {
        'unogs': Path(INPUT_PATH, 'final_unogs_df.csv'),
        'trends': Path(INPUT_PATH, 'google_trends_data.csv'),
        'nf_dict': Path(INPUT_PATH, 'netflix_nametags.json'),
        'flix_top10': Path(INPUT_PATH, 'history_results.json'),
        'flix_country': Path(INPUT_PATH, 'country_results.json'),
    }

    INPUT_PATH.mkdir(exist_ok=True)
    PARTS_PATH.mkdir(exist_ok=True)

    for file in file_path.values():
        if not file.exists():
            raise FileNotFoundError(f'Missing Required Input File: {file}')

    return file_path

def create_output_folder():
    output_folder = Path(os.getcwd(), 'output', f'Compile Results: {datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    output_folder.mkdir(exist_ok=True, parents=True)
    return output_folder


def clean_col_names(final_df, grouped_df):
    columns_to_remove = ['Unnamed: 0', 'level_0', 'level_1']
    for col_name in columns_to_remove:

        if col_name in final_df.columns:
            final_df = final_df.drop(col_name, axis=1)

        if col_name in grouped_df.columns:
            grouped_df = grouped_df.drop(col_name, axis=1)

    return final_df, grouped_df


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


def load_or_create_unogs_df(nf_originals):
    nf_slugs = [item['slug'] for item in nf_originals]

    print('\nLoading UNOGS Data')
    unogs_df_path = Path(PARTS_PATH, '[p]unogs_df.csv')
    if not unogs_df_path.exists():
        unogs_df = pd.read_csv(FILE_PATH['unogs'])
        unogs_df = unogs_df[unogs_df['slug'].isin(nf_slugs)]
        unogs_df = clean_unogs(unogs_df)
        unogs_df.to_csv(unogs_df_path)
    else:
        unogs_df = pd.read_csv(unogs_df_path)

    print('\nGrouping UNOGS Data')
    grouped_df_path = Path(PARTS_PATH, '[p]grp_unogs_df.csv')
    if not grouped_df_path.exists():
        grouped_df = perform_make_exclusive(unogs_df)
        grouped_df.to_csv(grouped_df_path)
    else:
        grouped_df = pd.read_csv(grouped_df_path)

    return unogs_df, grouped_df

# def load_or_create_grouped_df(nf_originals, unogs_df):
#     print('\nGrouping UNOGS Data')
#     grouped_df_path = Path(PARTS_PATH, '[p]grp_unogs_df.csv')
#     nf_slugs = [item['slug'] for item in nf_originals]
#     if not grouped_df_path.exists():
#         grouped_df = clean_unogs(unogs_df)
#         grouped_nf_df = grouped_df[grouped_df['slug'].isin(nf_slugs)]
#         grouped_df = perform_make_exclusive(grouped_nf_df)
#         grouped_df.to_csv(grouped_df_path)
#     else:
#         grouped_df = pd.read_csv(grouped_df_path)
#
#     return grouped_df