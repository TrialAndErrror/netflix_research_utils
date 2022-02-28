import logging
import os
from datetime import datetime
from pathlib import Path


def replace_specified_original_languages(df, original_language_replacements):
    for entry in original_language_replacements:
        try:
            df.loc[df.title == entry['title'], "Original Language"] = entry['Original Language']
        except KeyError:
            logging.warning(f'Original Language Replacement failed for {entry["title"]}; Key not found.')


def setup_dirs():
    """
    Setup folders for saving data to.
    """

    """
    Make sure that the overall Results directory exists.
    """
    results_dir = Path(os.getcwd(), 'pickle_results')
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
    final_df_path = Path(output_folder, 'final_unogs_df.csv')
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