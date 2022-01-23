import os
import re

import pandas as pd
from pathlib import Path
from src.utils import read_file
# from slugify import slugify


def make_language_header(prefix: str, language: str):
    """
    Strip whitespace around languages to make column headers more readable.
    """
    return f'{prefix}_{language.strip()}'


def add_missing_languages(header: str, data: dict):
    """
    Iterate over data dict, grabbing each language presented.
    Some are listed as '', so we rename those to Undefined.
    """
    lang_list = []
    for language, movie_list in data.items():
        if len(language) < 1:
            language = 'Undefined'
        lang_list.append(make_language_header(header, language))
    return lang_list


def remove_duplicates(language_list: list):
    """
    Removes duplicates by making language list into a set, and then back into a list for ease of working with.
    """
    return list(set(language_list))


def get_lang_headers(country_dicts):
    """
    Create lists for our dubbed and subbed languages
    """
    dub_languages = []
    sub_languages = []

    """
    Iterate through each country that the title is available in
    """
    for country, value in country_dicts.items():
        """
        Add dubbed and subbed languages to their respective lists.
        """
        dub_languages.extend(add_missing_languages('dub', value['Dub']))
        sub_languages.extend(add_missing_languages('sub', value['Sub']))

    """
    Remove duplicate entries from our language list, since we just need one column per language.
    """
    dub_languages = remove_duplicates(dub_languages)
    sub_languages = remove_duplicates(sub_languages)

    """
    Returns results as two lists: dubbed languages and subbed languages.
    """
    return dub_languages, sub_languages


def read_files():
    data_folder = Path(os.getcwd(), 'df_source_data')
    master_json = Path(data_folder, 'total_results_by_title.json')
    # country_files = os.listdir(Path(data_folder, 'results_by_country'))

    master_dict = read_file(master_json)
    master_country_dict = read_file(Path(data_folder, 'total_results_by_country.json'))

    return master_dict, master_country_dict


def process_into_country_dfs():
    print('Working...')
    master_dict, master_country_dict = read_files()
    dub_languages, sub_languages = get_lang_headers(master_country_dict)

    country_dfs = {}

    movie_titles = list(master_dict.keys())
    total_count = len(movie_titles)
    count = 1
    for title in movie_titles:
        print(f'({count}/{total_count}) Working on {title}')
        for country, data in master_dict[title].items():
            if not country_dfs.get(country):
                country_dfs[country] = []

            entry = {'title': title}
            for sub_or_dub, c_data in data.items():
                language_list = [f'{sub_or_dub.lower()}_{item}' for item in c_data.split(',')]

                for language in dub_languages + sub_languages:
                    entry.update({
                        language: bool(language in language_list)
                    })

                orig_languages = [lang.split('_', maxsplit=1)[1].split('[')[-2].strip() for lang in language_list if lang.strip().endswith('[Original]')]
                if 2 > len(orig_languages) > 0:
                    entry.update({
                        'Original Language': orig_languages[0]
                    })
                elif len(orig_languages) >= 2:
                    print('Found multiple Original Languages:')
                    for language in orig_languages:
                        print(language)
                    print(f'Using {orig_languages[0]}')
                    entry.update({
                        'Original Language': orig_languages[0]
                    })
                elif len(orig_languages) < 1:
                    entry.update({
                        'Original Language': 'Unknown'
                    })

            country_dfs[country].append(entry)
            count += 1

    country_df_dir = Path(os.getcwd(), 'country_dfs')
    title_df_dir = Path(os.getcwd(), 'title_dfs')
    country_df_dir.mkdir(exist_ok=True)
    title_df_dir.mkdir(exist_ok=True)

    value: pd.DataFrame
    for key, value in country_dfs.items():
        print(f'Saving Dataframe: {key}.csv')
        pd.DataFrame.from_records(value).to_csv(Path(country_df_dir, f'{key}.csv'))


if __name__ == '__main__':
    process_into_country_dfs()

