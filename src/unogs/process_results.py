import os
from pathlib import Path
from src.utils import read_file, write_file
from src.unogs import PROCESSED_FOLDER, OUTPUT_FOLDER, make_processed_filename


def add_languages_to_dict(data_dict: dict, title: str, languages: list):
    """
    Takes in list of languages and adds title to each language entry in data_dict

    :param data_dict: dict
    :param title: str
    :param languages: list
    :return: None
    """
    if len(languages) > 0:
        for language in languages:

            if language not in data_dict:
                """
                 If the language is not in the data_dict, create an empty list.
                 """
                data_dict[language] = list()

            """
            Add the title to the end of list.
            """
            data_dict[language].append(title)

        return data_dict


def process_languages_str(info: dict, content_type: str):
    """
    Takes in info string, processes languages, and returns list of languages.

    content_type is 'Dub' or 'Sub'

    :param info: str
    :param content_type: str
    :return: list
    """

    """
    Check if the movie has an entry for the content_type.
    """
    languages = []

    category = info.get(content_type, None)
    if category:
        """
        Split string of languages into list based on commas.
        """
        languages = category.split(',')

    return languages


def sort_by_language(data: dict):
    """
    Sort movies by Subbed and Dubbed language and separate into dictionaries.

    :param data: dict
    :return:
    """
    countries_dict = {}
    print('Starting work on Subs and Dubs')
    """
    Iterate over data dictionary to process subs and dubs
    """
    count = 1
    total = len(data)
    for title, info in data.items():
        print(f'Processing movie {count} of {total}')
        for country, languages in info.items():
            if country not in countries_dict:
                countries_dict[country] = {
                    'Sub': {},
                    'Dub': {}
                }

            dub_lang_list = process_languages_str(languages, 'Dub')
            add_languages_to_dict(countries_dict[country]['Dub'], title, dub_lang_list)

            sub_lang_list = process_languages_str(languages, 'Sub')
            add_languages_to_dict(countries_dict[country]['Sub'], title, sub_lang_list)

        count += 1

    return countries_dict


def save_results(data: dict):
    """
    Generate filename and save file based on content type.

    :param data: dict
    :return:
    """

    out_file = Path(PROCESSED_FOLDER, make_processed_filename())
    print(f'Saving Movies by Country and Language to {out_file.as_posix()}')
    write_file(data, out_file)


def process_subs_and_dubs(results_filename):
    """
    Load languages data for movies, sort by sub and dub languages, and save to file.

    :param results_filename: str
    :return: None
    """
    filename = Path(OUTPUT_FOLDER, results_filename)
    data = read_file(filename)

    countries_dict = sort_by_language(data)

    """
    Write Countries dictionary to file
    """
    save_results(countries_dict)

    return data, countries_dict


def format_by_country(all_results):
    total_dict = {}

    for results_dict in all_results:
        for country, c_value in results_dict.items():

            if not country in total_dict:
                total_dict[country] = {}

            for sub_or_dub, s_value in c_value.items():
                if not sub_or_dub in total_dict[country]:
                    total_dict[country][sub_or_dub] = {}

                for language, l_value in s_value.items():
                    if not language in total_dict[country][sub_or_dub]:
                        total_dict[country][sub_or_dub][language] = []
                    total_dict[country][sub_or_dub][language].extend(l_value)

    return total_dict


def save_country_dicts(total_dict):
    countries_path = Path(PROCESSED_FOLDER, 'results_by_country')
    countries_path.mkdir(exist_ok=True)
    for key, country_dict in total_dict.items():
        out_file = Path(countries_path, f'{key}.json')
        write_file(country_dict, out_file)


if __name__ == '__main__':
    results_dir = Path(OUTPUT_FOLDER)
    files_list = [item for item in os.listdir(results_dir) if item.endswith('.json')]
    all_results = []
    movie_by_title_dict = {}

    for file in files_list:
        data, new_dict = process_subs_and_dubs(file)
        movie_by_title_dict.update(data)
        if new_dict:
            all_results.append(new_dict)

    out_file = Path(PROCESSED_FOLDER, 'total_results_by_title.json')
    write_file(movie_by_title_dict, out_file)

    total_dict = format_by_country(all_results)

    out_file = Path(PROCESSED_FOLDER, 'total_results_by_country.json')
    write_file(total_dict, out_file)

    save_country_dicts(total_dict)
