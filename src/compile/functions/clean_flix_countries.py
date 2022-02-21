from src.utils import read_file
import pandas as pd


def clean_flix_countries(file_path):
    country_info = read_file(file_path)
    total_countries = []

    for item in country_info.values():
        total_countries.extend(item)

    total_countries = list(set(total_countries))

    countries_dict = {}

    for item, values in country_info.items():
        countries_dict[item] = {
            country: bool(country in values) for country in total_countries
        }
        countries_dict[item]['Total Count'] = len(values)

    countries_df = pd.DataFrame.from_dict(countries_dict).T
    countries_df = countries_df.rename({item: f't10c_{item}' for item in countries_df.columns}, axis=1)

    return countries_df
