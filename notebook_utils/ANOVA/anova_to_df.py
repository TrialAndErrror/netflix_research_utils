import os

import pandas as pd
from src.utils import load_pickle, read_json
from pathlib import Path
import json

df_structure = {
    'Canada': {
        'Dutch': {
            0: 'Dataframe in JSON Format',
            1: {
                'W': 'w-value',
                'P': 'p-value'
            }
        }
    }
}


def get_significance_groups(row):
    """
    Return whether the

    :param row:
    :return:
    """

    """
    First group in group name is the one that has a higher mean.
    """

    if row['Diff'] >= 0:
        return f'{row["group1"]}_{row["group2"]}'
    else:
        return f'{row["group2"]}_{row["group1"]}'


def main(df, prefix):
    master_df = pd.DataFrame(columns=[
        'Country',
        'Language',
        'Combination',
        # Positive Difference Values
        'neither_sub',
        'neither_dub',
        'neither_both',
        'sub_dub',
        'sub_both',
        'dub_both',
        # Negative Difference Values
        'sub_neither',
        'dub_neither',
        'both_neither',
        'dub_sub',
        'both_sub',
        'both_dub'
    ])

    df_list = []
    df_list.append(master_df)

    for country, country_data in df.items():
        for language, language_data in country_data.items():
            if language_data:
                sub_df = make_sub_df(country, language, language_data)
                df_list.append(sub_df)

    total_df = pd.concat(df_list).set_index('Combination')

    # if 'Unnamed: 0' in total_df.columns:
    #     total_df = total_df.pop('Unnamed: 0')

    out_folder = Path(os.getcwd(), 'output')
    out_folder.mkdir(exist_ok=True)

    outfile_path = Path(out_folder, f'{prefix}_anova_results.csv')
    total_df.to_csv(outfile_path)

    return outfile_path


def make_sub_df(country, language, language_data):
    sub_df = pd.DataFrame(language_data[0]).T
    shapiro = language_data[1]
    sub_df['sig_group'] = sub_df.apply(lambda x: get_significance_groups(x), axis=1)
    sub_df['Combination'] = f'{country}_{language}'
    sub_df = sub_df.pivot(values=['p-value'], columns=['sig_group'], index='Combination').droplevel(0, axis=1)
    sub_df['Country'] = country
    sub_df['Language'] = language
    sub_df = sub_df.reset_index()
    return sub_df


if __name__ == '__main__':
    data = read_json(Path('/home/wade/PycharmProjects/chetflix/notebook_utils/ANOVA/output/anova_results.json'))
    main(data, prefix='test')
