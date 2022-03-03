import os

import pandas as pd
from pathlib import Path
import pickle

from notebook_utils.group_counts.counter_utils import count_rows, count_unique_titles, save_split_excel, save_json,\
    sort_list


class GroupCounter:
    def __init__(self, df, name):
        self.df: pd.DataFrame = df
        self.name = name

        self.countries: list = []
        self.languages: list = []

        self.language_rows: list = []
        self.language_titles: list = []

        self.subbed_rows: list = []
        self.subbed_titles: list = []

        self.dubbed_rows: list = []
        self.dubbed_titles: list = []

        self.country_rows: list = []
        self.country_titles: list = []

        self.rows_dict: dict = {}
        self.titles_dict: dict = {}

        self.output_path = Path(os.getcwd(), 'output')
        self.output_path.mkdir(exist_ok=True)

    def run_analysis(self):
        self.get_groups()
        self.count_titles()
        self.save_results()

    def get_groups(self):
        print('Making Groups...')
        self.countries = list(self.df.Country.unique())
        self.languages = list(self.df.Language.unique())

    def count_titles(self):
        self.count_languages()
        self.count_subbed()
        self.count_dubbed()
        self.count_countries()

    def count_languages(self):
        print('Counting Languages...')

        for language in self.languages:
            filtered_df = self.df[(self.df.Language == language) & (self.df.Group != "neither")]

            self.language_rows.append(count_rows(language, filtered_df))
            self.language_titles.append(count_unique_titles(language, filtered_df))

    def count_subbed(self):
        print('Counting Subbed...')

        for language in self.languages:
            filtered_df = self.df[(self.df.Language == language) & (self.df.Group == "sub")]

            self.subbed_rows.append(count_rows(language, filtered_df))
            self.subbed_titles.append(count_unique_titles(language, filtered_df))

    def count_dubbed(self):
        print('Counting Dubbed...')

        for language in self.languages:
            filtered_df = self.df[(self.df.Language == language) & (self.df.Group == "dub")]

            self.dubbed_rows.append(count_rows(language, filtered_df))
            self.dubbed_titles.append(count_unique_titles(language, filtered_df))

    def count_countries(self):
        print('Counting Countries...')
        for country in self.countries:
            filtered_df = self.df[(self.df.Country == country) & (self.df.Group != "neither")]

            self.country_rows.append(count_rows(country, filtered_df))
            self.country_titles.append(count_unique_titles(country, filtered_df))

    def save_results(self):
        print('Saving Results...')

        self.rows_dict = {
            'Languages': sort_list(self.language_rows),
            'Countries': sort_list(self.country_rows),
            'Subbed': sort_list(self.subbed_rows),
            'Dubbed': sort_list(self.dubbed_rows),
        }

        self.titles_dict = {
            'Languages': sort_list(self.language_titles),
            'Countries': sort_list(self.country_titles),
            'Subbed': sort_list(self.subbed_titles),
            'Dubbed': sort_list(self.dubbed_titles),
        }

        """
        Save JSON data files
        """
        save_json(Path(self.output_path, f'{self.name}_row_counts.json'), self.rows_dict)
        save_json(Path(self.output_path, f'{self.name}_title_counts.json'), self.titles_dict)

        """
        Save Excel Files
        """
        save_split_excel(Path(self.output_path, f'{self.name}_rows_review_sheet.xlsx'), self.rows_dict)
        save_split_excel(Path(self.output_path, f'{self.name}_titles_review_sheet.xlsx'), self.titles_dict)

        print('Results Saved!')


def analyze_df(path, title):
    df = pd.read_csv(path)
    counter_obj = GroupCounter(df, title)

    print(f'\nAnalyzing {title} Dataset')
    counter_obj.run_analysis()


def count_main():
    input_path = Path(os.getcwd(), 'input')
    input_path.mkdir(exist_ok=True)

    analyze_df(Path(input_path, 'final_short_dataset.csv'), 'full')

    analyze_df(Path(input_path, 'Dataset Excluding Distribution Titles.csv'), 'Non-Distribution')


if __name__ == '__main__':
    count_main()
