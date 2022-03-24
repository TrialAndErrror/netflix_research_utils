from pathlib import Path

from src.compile import pd

from src.compile.functions.utils import check_for_required_files, create_output_folder, \
    new_clean_col_names, load_or_create_unogs_df
from src.utils import read_json
from src.compile.functions.clean_gt_data import clean_gt, merge_unogs_and_gt
from src.compile.functions.clean_flix_top10 import clean_flixpatrol_data
from src.compile.functions.clean_flix_countries import merge_with_flix_countries

import ray
ray.init()


def compile_main():
    """
    Compile all dataframes into one complete dataset.

    Saves dataframes as final_compiled_data.csv in the current directory.

    :return: None
    """

    """
    Setup directories and make sure all required files are present
    """
    file_path, input_path, parts_path = check_for_required_files()

    """
    Load UNOGS dataframe and Google Trends Dataframe
    """
    nf_nametags = read_json(file_path['nf_dict'])
    melted_df = load_or_create_unogs_df(nf_nametags, file_path, parts_path)

    top_3_languages_df = pd.read_csv(Path(input_path, 'top_3_languages.csv'))
    melted_df = pd.merge(melted_df, top_3_languages_df[
        ['Country', 'Primary Language', 'Secondary Language', 'Tertiary Language']
    ], how='left', left_on='Country', right_on='Country')

    """
    Load Google Trends Dataframe
    """
    print('\nLoading Google Trends Data')
    gt_data = clean_gt(file_path['trends'])

    """
    Merge UNOGS and Google Trends data
    """
    final_df = merge_unogs_and_gt(melted_df, gt_data)

    """
    Load and Merge FlixPatrol Top 10 Overall Data
    """
    print('\nLoading FlixPatrol Top 10 Data')

    flixpatrol_points_dataframe = clean_flixpatrol_data(file_path['flix_top10'])
    flixpatrol_points_dataframe.to_csv(Path(parts_path, 'flixpatrol_top10_df.csv'))
    final_df = final_df.merge(
        flixpatrol_points_dataframe,
        left_on=['slug', 'Country'],
        right_on=['slug', 'Country'],
        how='left'
    )
    final_df[['Points', 'Days', 'ø/day']] = final_df[['Points', 'Days', 'ø/day']].fillna(0)

    final_df.to_csv(Path(parts_path, '[p]unogs_gt_and_top10.csv'))

    """
    Load and Merge FlixPatrol Countries Data
    """
    print('\nLoading FlixPatrol Countries Data')
    final_df = merge_with_flix_countries(final_df, file_path['flix_country'])
    final_df.to_csv(Path(parts_path, '[p]unogs_gt_top10_and_countries.csv'))

    """
    Be sure to remove any unnecessary columns before saving.
    """
    final_df = new_clean_col_names(final_df)
    if 'Unnamed: 0' in final_df.columns:
        final_df = final_df.drop(columns=['Unnamed: 0'])
    """
    Save Final Results
    """
    output_folder = create_output_folder()
    # final_path = Path(output_folder, "final_full_dataset.csv")
    # print(f'\nSaving Final Dataframe to {final_path}')
    # final_df.to_csv(final_path)

    final_short_path = Path(output_folder, "final_short_dataset.csv")
    final_short_df = final_df[final_df['Group Value'] == True].drop(columns=['Group Value'])
    final_short_df.to_csv(final_short_path)

    """
    Split data based on Wiki groups
    """
    wiki_groups = read_json(Path(input_path, 'wiki_groups.json'))
    group_output_folder = Path(output_folder, 'wiki_groups')
    group_output_folder.mkdir(exist_ok=True)
    for group, title_list in wiki_groups.items():
        group_df = final_short_df[final_short_df['title'].isin(title_list)]
        group_df.to_csv(Path(group_output_folder, f'Group Data - {group}.csv'))

    """
    Save dataframe of all films excluding those in the International Distribution group
    """
    distribution_titles = wiki_groups.get('Distribution', None)
    if distribution_titles:
        print('Saving Dataset Without Distribution Titles')
        non_international_df = final_short_df[~final_short_df['title'].isin(distribution_titles)]
        non_international_df.to_csv(Path(group_output_folder, f'Dataset Excluding Distribution Titles.csv'))

    print('Compile Complete.')
    return final_short_path


if __name__ == '__main__':
    compile_main()
