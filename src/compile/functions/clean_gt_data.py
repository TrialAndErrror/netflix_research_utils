import pandas as pd
from slugify import slugify


def get_gt_column(row):
    country = row['Country']
    gt_data = row.get(f'gt_{country}')
    return gt_data


def merge_unogs_and_gt(unogs_df, gt_data):
    test = unogs_df.copy()
    # test['slug'] = test['title'].apply(lambda x: slugify(x))
    sample = test.merge(gt_data, left_on='slug', right_on='slug', how='left')
    sample['google_trends_score'] = sample.apply(lambda x: get_gt_column(x), axis=1)
    remaining_columns = [
        'title',
        'Original Language',
        'Country',
        'google_trends_score'
    ]
    remaining_columns.extend(
        [item for item in sample.columns
         if (
                 item.startswith('sub_')
                 or item.startswith('dub_')
                 or item.startswith('grp_')
         )
         ]
    )
    remaining_columns.append('slug')
    sample = sample[remaining_columns]
    return sample


def clean_gt(file_path):
    """
    Load and process Google Trends dataframe.

    Rename country columns with gt_ prefix.
    """
    gt_data = pd.read_csv(file_path)
    col_dict = {item: f'gt_{item}' for item in gt_data.columns if item != 'slug'}
    gt_data = gt_data.rename(col_dict, axis=1)

    return gt_data
