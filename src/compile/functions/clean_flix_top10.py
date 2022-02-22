import pandas as pd
import numpy as np

from src.utils import read_json

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
    'United States']


def replace_indices_with_country(flix_dict):
    results = {}

    # These are the values that we don't want to end up in our final chart
    value_exclude_list = 'Country', 'Unnamed: 2', 'Weeks.1', 'Points.1'

    for movie_title, data_dict in flix_dict.items():
        results[movie_title] = {}

        # Make sure there's data, and then get the list of countries
        if data_dict:
            countries_list = [item for item in data_dict.get('Country').values()]

            # Loop over each country in the countries list to use as keys
            for index, entry in enumerate(countries_list):
                results[movie_title][entry] = {}

                # Get the values and assign them to the inner dictionary
                for key, values_dict in data_dict.items():
                    if key.strip() not in value_exclude_list:
                        results[movie_title][entry][key] = values_dict.get(index)

    return results


def reform_dict(target_dict):
    results = {}

    for outerkey, innerdict in target_dict.items():
        if innerdict:
            for innerkey, values in innerdict.items():
                results[(outerkey, innerkey)] = values

    return results


def make_into_dataframe(target_dict):
    df = pd.DataFrame.from_dict(target_dict, orient="index").stack().to_frame()
    return pd.DataFrame(df[0].values.tolist(), index=df.index)


def clean_flixpatrol_columns(dataframe, title):
    return dataframe.rename(columns={
        'Points': f'{title} Points',
        'Days': f'{title} Days',
        'ø/day': f'{title} ø/day'
    })


def clean_netflix_columns(dataframe, title):
    return dataframe.rename(columns={
        'Points': f'{title} Points',
        'Weeks': f'{title} Weeks'
    })


def prepare_dataframes_to_join(cleaned_movies_history):
    clean_netflix_overall_df = clean_flixpatrol_columns(
        make_into_dataframe(
            replace_indices_with_country(cleaned_movies_history)
        ), 'Movies')

    return clean_netflix_overall_df


def clean_flixpatrol_data(history_file):
    history_data = read_json(history_file)

    cleaned_movies_history = {}

    for key, value in history_data.items():
        cleaned_movies_history[key] = {}
        data_dict = add_missing_countries_to_data_dict(value)
        cleaned_movies_history[key] = data_dict

    dataframe = prepare_dataframes_to_join(cleaned_movies_history)

    return dataframe.reset_index()


def add_missing_countries_to_data_dict(data_dict):
    for country in ALL_COUNTRIES:
        if country not in data_dict['Country'].values():
            index_num = len(data_dict['Country'])
            data_dict['Country'][index_num] = country
            data_dict['Points'][index_num] = 0
            data_dict['Unnamed: 2'][index_num] = np.nan
            data_dict['Days'][index_num] = '0 days'
            data_dict['ø/day'][index_num] = 0.0
    return data_dict
