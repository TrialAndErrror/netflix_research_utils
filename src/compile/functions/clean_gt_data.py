import pandas as pd


def get_gt_column(row):
    country = row['Country']
    gt_data = row.get(f'gt_{country}')
    return gt_data


def merge_unogs_and_gt(unogs_df, gt_data):
    test = unogs_df.copy()
    sample = test.merge(gt_data, left_on=['title', 'slug', 'Country'], right_on=['title', 'slug', 'Country'], how='left')
    sample = sample.rename(columns={'value': 'Google Trends Score'})
    remaining_columns = [
        'title',
        'Original Language',
        'Country',
        'Group',
        'Language',
        'Google Trends Score',
        'slug'
    ]
    sample = sample[remaining_columns]
    sample['Google Trends Score'] = sample['Google Trends Score'].fillna(0)
    sample['Google Trends Score'] = sample['Google Trends Score'].astype(int)
    return sample


def clean_gt(file_path):
    """
    Load and process Google Trends dataframe.

    Rename country columns with gt_ prefix.
    """
    gt_data = pd.read_csv(file_path)
    # col_dict = {item: f'gt_{item}' for item in gt_data.columns if item != 'slug'}
    # gt_data = gt_data.rename(col_dict, axis=1)

    melted = gt_data.drop(columns=['Unnamed: 0'])
    melted = melted.melt(id_vars=['title', 'slug'])
    melted = melted.rename(columns={'variable': 'Country'})
    return melted
