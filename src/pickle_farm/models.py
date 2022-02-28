from pathlib import Path
import pickle
import json

from typing import List

ALL_COUNTRIES = [
    'Argentina',
    'Australia',
    'Belgium',
    'Brazil',
    'Canada',
    'Colombia',
    'Czech Republic',
    'France',
    'Germany',
    'Greece',
    'Hong Kong',
    'Hungary',
    'Iceland',
    'India',
    'Israel',
    'Italy',
    'Japan',
    'Lithuania',
    'Malaysia',
    'Mexico',
    'Netherlands',
    'Philippines',
    'Poland',
    'Portugal',
    'Romania',
    'Russia',
    'Singapore',
    'Slovakia',
    'South Africa',
    'South Korea',
    'Spain',
    'Sweden',
    'Switzerland',
    'Thailand',
    'Turkey',
    'Ukraine',
    'United Kingdom',
    'United States'
]

ORIGINAL_LANGUAGE_REPLACE_DICT = {
    'British English': 'English'
}


class PickleReader:
    def __init__(self, path: Path):
        self.path: Path = path
        self.data: pickle or None = None
        self.title: str = ''
        self.nfid: int = 0

        self.language_data: dict = {}

        self.original_language: str = 'No Language Detected'
        self.dub_language_dict: dict = {}
        self.sub_language_dict: dict = {}

        self.get_data()

    def get_data(self):
        """
        Read data from pickle path and assign all attributes.

        :return: None
        """
        with open(self.path, 'rb') as file:
            self.data: dict = pickle.load(file)
        try:
            data = self.data.copy()
        except AttributeError:
            print(f'Error reading file: {self.path}')
        else:
            self.title = data.pop('title')
            print(f'Successfully loaded Pickle: {self.title}')

            self.nfid = data.pop('nfid', None)

            self.language_data = {country: dict() for country in ALL_COUNTRIES}
            self.language_data.update(check_for_languages(data['languages']))

            self.make_sub_and_dub_dicts()

            self.original_language = get_original_language(self.dub_language_dict)

    def replace_language(self, old_lang, new_lang):
        new_dict = {
            country: {sub_or_dub: [item.replace(old_lang, new_lang) for item in s_data] for (sub_or_dub, s_data) in
                      c_data.items()} for (country, c_data) in self.language_data.items()}
        self.language_data = new_dict

    def make_sub_and_dub_dicts(self):
        self.sub_language_dict = split_subs_and_dubs(self.language_data, 'Sub')
        self.dub_language_dict = split_subs_and_dubs(self.language_data, 'Dub')

    def save_data(self):
        """
        Save data back to original pickle path.

        :return: None
        """
        with open(self.path, 'w+b') as file:
            pickle.dump(self.data, file)

    def make_dataframe_entries(self, columns: List[str]) -> list:
        """
        Iterate over language_data to find language that match columns provided.
        Creates list of dictionaries that can be used as an entry for a DataFrame.

        :param columns: list
        :return: list
        """
        entry_list = []
        sub_columns = [item for item in columns if item.startswith('sub_')]
        dub_columns = [item for item in columns if item.startswith('dub_')]

        for country, lang_dict in self.language_data.items():
            entry = dict()
            entry['title'] = self.title
            entry['Original Language'] = replace_original_language(self.original_language)
            entry['Country'] = country

            for column in sub_columns:
                entry[column] = bool(column.split('_')[1] in lang_dict.get('Sub', list()))

            for column in dub_columns:
                entry[column] = bool(column.split('_')[1] in lang_dict.get('Dub', list()))

            entry['slug'] = self.path.stem

            entry_list.append(entry)

        return entry_list

    def __repr__(self):
        if self.title:
            return f'{self.title} (PickleReader)'
        return 'Unnamed PickleReader'

    def __str__(self):
        if self.title:
            return f'{self.title} (PickleReader)'
        return 'Unnamed PickleReader'

    def to_json(self):
        data_dict = {
            'nfid': self.nfid,
            'title': self.title,
            'original_language': self.original_language,
            'dub_language_dict': self.dub_language_dict,
            'sub_language_dict': self.sub_language_dict,
            'language_data': self.language_data,
            'data': self.data,
        }
        return json.dumps(data_dict)

    def get_all_languages(self):
        dub_languages = []
        for language_list in self.dub_language_dict.values():
            dub_languages.extend([f'dub_{language}' for language in language_list])
        sub_languages = []

        for language_list in self.sub_language_dict.values():
            sub_languages.extend([f'sub_{language}' for language in language_list])

        all_languages = list(set(dub_languages + sub_languages))

        return all_languages


def check_for_languages(data_dict: dict) -> dict:
    """
    Check for specified language type and return a cleaned list of languages that appear in the title.

    :return: dict
    """

    """
    Private function for just splitting string-based list of languages into list, with error handling.
    """

    def get_language_list(country_dict: dict, lang_type: str) -> list:
        languages: str = country_dict.get(lang_type)
        try:
            language_list = [item.strip() for item in languages.split(',')]
        except TypeError:
            language_list = []
        return language_list

    results = {}

    """
    Iterate over each country in the dictionary.
    
    Structure of data expected:
    {
        'Country Name':
            'Sub': ['list', 'of', 'languages'],
            'Dub': ['list', 'of', 'languages'],
    }
    """

    for country, country_dict in data_dict.items():
        results[country] = {
            'Sub': get_language_list(country_dict, 'Sub'),
            'Dub': get_language_list(country_dict, 'Dub')
        }

    return results


def split_subs_and_dubs(data_dict: dict, lang_type: str) -> dict:
    """
    Filter languages in dictionary by lang_type

    :param data_dict: dict
    :param lang_type: str

    :return: dict
    """

    results = {}
    for country, data in data_dict.items():
        if len(data) > 0:
            results[country] = [item for item in data[lang_type] if len(item) > 0]
    return results


def get_original_language(dub_dict) -> str:
    """
    Iterate over dubbing dictionary until original language is found.

    Returns None if no original language is found.

    :param dub_dict: dict
    :return: str or None
    """
    for country, lang_list in dub_dict.items():
        for entry in lang_list:
            if entry.strip().endswith('[Original]'):
                return entry.split('[')[-2].strip()


def replace_original_language(original_language: str) -> str:
    return ORIGINAL_LANGUAGE_REPLACE_DICT.get(original_language, original_language)
