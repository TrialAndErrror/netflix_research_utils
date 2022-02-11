import pandas as pd
from slugify import slugify


def merge_unogs_and_gt(unogs_df, gt_data):
    test = unogs_df.copy()
    # test['slug'] = test['title'].apply(lambda x: slugify(x))
    sample = test.merge(gt_data, left_on='slug', right_on='slug', how='left')
    return sample


def clean_gt(file_path):
    """
    Load and process Google Trends dataframe.

    Rename country columns with gt_ prefix.
    """
    gt_data = pd.read_csv(file_path)
    col_dict = {item: f'gt_{item}' for item in gt_data.columns}
    col_dict['Unnamed: 0'] = 'slug'
    gt_data = gt_data.rename(col_dict, axis=1)

    return gt_data
