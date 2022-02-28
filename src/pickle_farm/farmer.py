import pandas as pd
import re
from pathlib import Path
from src.pickle_farm.models import PickleReader
from slugify import slugify

from src.pickle_farm.utils import replace_specified_original_languages, setup_dirs, save_error_list, save_dataframes


def run_all_pickles(pickle_dir: Path or str, nf_dict: list, original_language_replacements: dict):
    """
    Process all pickles contained in netflix dict and save as dataframes.

    :return: None
    """

    """
    Set up directories
    """
    pickle_folder = Path(pickle_dir)
    output_folder = setup_dirs()

    """
    Process all pickles from pickle_folder, except for ones where the slug indicates that they should be excluded from search.
    """
    pickle_file_list = [f'{item["slug"]}' for item in nf_dict if item["slug"] != 'EXCLUDE']

    """
    Exclude pickles that do not appear in the slugged version of the Netflix Nametags dict
    """
    slugged_title_list = [f'{slugify(item["title"])}' for item in nf_dict]

    pickle_files = [item for item in pickle_folder.iterdir() if (item.stem in pickle_file_list or item.stem in slugged_title_list)]

    """
    Get list of all lanugages used across the films
    """
    language_list = get_languages_list(pickle_files)

    """
    Create dataframe using list of languages generated above as the entire set of langauges.
    """
    df, error_list = process_pickles_into_df(pickle_files, language_list)

    replace_specified_original_languages(df, original_language_replacements)

    """
    Save dataframe to output folder
    Also save country dataframes to a subfolder in the output folder
    """
    save_dataframes(df, output_folder)

    """
    Save error list to output folder
    """
    save_error_list(error_list, output_folder)

    return output_folder


def get_languages_list(all_pickles) -> list:
    languages_list = []
    for pickle in all_pickles:
        pickle_languages = PickleReader(pickle).get_all_languages()
        for language in pickle_languages:
            if re.match(r'(?i).*\d more', language):
                raise ValueError(f'Language values for {pickle} reflect incomplete collection attempt.')
        languages_list.extend(pickle_languages)
        languages_list = list(set(languages_list))

    return languages_list


def process_pickles_into_df(all_pickles, language_list):
    """
    Process all pickle files into one dataframe and return error list.

    :return: pd.DataFrame, list
    """

    all_entries = []
    error_list = []

    """
    Create PickleReader object for each pickle;
    append the dataframe entries to the all_entries list.
    """
    for pickle in all_pickles:
        obj = PickleReader(pickle)

        """
        Check to see if object has a title;
        If there is no title, that means there is no data, and so add to errors list.
        """
        
        if obj.title:
            all_entries.extend(obj.make_dataframe_entries(language_list))
        else:
            error_list.append(str(pickle).split('/')[-1].split('.')[-2])

    """
    Create DataFrame from all_entries list
    """
    df = pd.DataFrame.from_records(all_entries)

    return df, error_list
