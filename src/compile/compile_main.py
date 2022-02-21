from pathlib import Path

from src.compile.functions.utils import PARTS_PATH, FILE_PATH, check_for_required_files, create_output_folder, \
    clean_col_names, merge_grouped_and_google_trends, merge_unogs_and_google_trends, load_or_create_unogs_df
from src.utils import read_file
from src.compile.functions.clean_gt_data import clean_gt
from src.compile.functions.clean_flix_top10 import clean_flixpatrol_data
from src.compile.functions.clean_flix_countries import clean_flix_countries


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
    nf_nametags = read_file(FILE_PATH['nf_dict'])
    unogs_df, grouped_df = load_or_create_unogs_df(nf_nametags)

    # grouped_df = load_or_create_grouped_df(nf_nametags, unogs_df)

    """
    Load Google Trends Dataframe
    """
    print('\nLoading Google Trends Data')
    gt_data = clean_gt(FILE_PATH['trends'])

    """
    Merge UNOGS and Google Trends data
    """
    final_df = merge_unogs_and_google_trends(unogs_df, gt_data)

    grouped_df = merge_grouped_and_google_trends(grouped_df, gt_data)

    """
    Load and Merge FlixPatrol Top 10 Overall Data
    """
    print('\nLoading FlixPatrol Top 10 Data')

    flixpatrol_points_dataframe = clean_flixpatrol_data(FILE_PATH['flix_top10'])
    final_df = final_df.merge(flixpatrol_points_dataframe, left_on='slug', right_on='level_0', how='left')
    final_df = final_df[(final_df['Country'] == final_df['level_1']) | (final_df['level_1'].isna())]
    final_df.to_csv(Path(PARTS_PATH, '[p]unogs_gt_and_top10.csv'))

    grouped_df = grouped_df.merge(flixpatrol_points_dataframe, left_on='slug', right_on='level_0', how='left')
    grouped_df = grouped_df[(grouped_df['Country'] == grouped_df['level_1']) | (grouped_df['level_1'].isna())]
    grouped_df.to_csv(Path(PARTS_PATH, '[p]grp_unogs_gt_and_top10.csv'))

    """
    Load and Merge FlixPatrol Countries Data
    """
    print('\nLoading FlixPatrol Countries Data')
    flixpatrol_countries_dataframe = clean_flix_countries(FILE_PATH['flix_country'])
    final_df = final_df.merge(flixpatrol_countries_dataframe, left_on='slug', right_index=True, how='left')
    final_df.to_csv(Path(PARTS_PATH, '[p]unogs_gt_top10_and_countries.csv'))

    grouped_df = grouped_df.merge(flixpatrol_countries_dataframe, left_on='slug', right_index=True, how='left')
    grouped_df.to_csv(Path(PARTS_PATH, '[p]grp_unogs_gt_top10_and_countries.csv'))

    """
    Be sure to remove any unnecessary columns before saving.
    """
    final_df, grouped_df = clean_col_names(final_df, grouped_df)

    """
    Save Final Results
    """
    output_folder = create_output_folder()

    final_path = Path(output_folder, "final_compiled_data.csv")
    grouped_path = Path(output_folder, "grp_compiled_data.csv")

    print(f'\nSaving Final Dataframe to {final_path}')

    final_df.to_csv(final_path)
    grouped_df.to_csv(grouped_path)

    print('Compile Complete.')


if __name__ == '__main__':
    compile_main()
