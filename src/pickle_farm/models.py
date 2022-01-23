from pathlib import Path
import pickle

TEST_COLUMNS = ['sub_English', 'dub_Spanish', 'sub_Dutch']


class PickleReader:
    def __init__(self, path: Path):
        self.path: Path = path
        self.data: pickle or None = None
        self.title: str or None = None
        self.nfid: int or None = None

        self.language_data: dict or None = None

        self.original_language: str or None = None
        self.dub_language_dict: dict or None = None
        self.sub_language_dict: dict or None = None

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

            self.language_data = check_for_languages(data['languages'])

            self.make_sub_and_dub_dicts()

            self.original_language = get_original_language(self.dub_language_dict)

    def replace_language(self, old_lang, new_lang):
        new_dict = {country: {sub_or_dub: [item.replace(old_lang, new_lang) for item in s_data] for (sub_or_dub, s_data) in c_data.items()} for (country, c_data) in self.language_data.items()}
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

    def make_dataframe_entries(self, columns: list[str]) -> list:
        """
        Iterate over language_data to find language that match columns provided.
        Creates list of dictionaries that can be used as an entry for a DataFrame.

        :param columns: list
        :return: list
        """
        entry_list = []
        sub_columns = [item for item in columns if item.startswith('sub_')]
        dub_columns = [item for item in columns if item.startswith('dub_')]

        for country, lang_list in self.language_data.items():
            entry = dict()
            entry['title'] = self.title
            entry['Original Language'] = self.original_language
            entry['Country'] = country

            for column in sub_columns:
                entry[column] = bool(column.split('_')[1] in lang_list['Sub'])

            for column in dub_columns:
                entry[column] = bool(column.split('_')[1] in lang_list['Dub'])

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
            language_list = languages.split(',')
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
        results[country] = data[lang_type]
    return results


def get_original_language(dub_dict):
    """
    Iterate over dubbing dictionary until original language is found.

    Returns None if no original language is found.

    :param dub_dict: dict

:   :return: str or None
    """
    for country, lang_list in dub_dict.items():
        for entry in lang_list:
            if entry.strip().endswith('[Original]'):
                return entry.split('[')[-2].strip()




