import pandas as pd

from src.flix.utils import load_pickle


def replace_indices_with_country(dict):
    results = {}

    # These are the values that we don't want to end up in our final chart
    value_exclude_list = 'Country', 'Unnamed: 2', 'Weeks.1', 'Points.1'

    for movie_title, data_dict in dict.items():
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


def reform_dict(dict):
    results = {}

    for outerkey, innerdict in dict.items():
        if innerdict:
            for innerkey, values in innerdict.items():
                results[(outerkey, innerkey)] = values

    return results


def make_into_dataframe(dict):
    data = reform_dict(dict)
    return pd.DataFrame.from_dict(data).T


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
    netflix_overall = {}
    netflix_movies = {}
    netflix_official = {}
    netflix_kids = {}

    for movie in cleaned_movies_history:
        netflix_overall[movie] = cleaned_movies_history[movie].get('Netflix Overall')
        netflix_movies[movie] = cleaned_movies_history[movie].get('Netflix Movies')
        netflix_official[movie] = cleaned_movies_history[movie].get('Netflix Official')
        netflix_kids[movie] = cleaned_movies_history[movie].get('Netflix Kids')

    clean_netflix_overall_df = clean_flixpatrol_columns(
        make_into_dataframe(
            replace_indices_with_country(netflix_overall)
        ), 'Overall')

    clean_netflix_movies_df = clean_flixpatrol_columns(
        make_into_dataframe(
            replace_indices_with_country(netflix_movies)
        ), 'Movies')

    clean_netflix_kids_df = clean_flixpatrol_columns(
        make_into_dataframe(
            replace_indices_with_country(netflix_kids)
        ), 'Kids')

    clean_netflix_official_df = clean_netflix_columns(
        make_into_dataframe(
            replace_indices_with_country(netflix_official)
        ), 'Official')

    return [
        clean_netflix_overall_df,
        clean_netflix_movies_df,
        clean_netflix_kids_df,
        clean_netflix_official_df
    ]


def clean_flixpatrol_data(history_file):
    history_data = load_pickle(history_file)

    cleaned_movies_history = {}

    for key, value in history_data.items():
        cleaned_movies_history[key] = {}
        for data_tuple in value:
            cleaned_movies_history[key][data_tuple[0]] = data_tuple[1][0].to_dict()

    dataframes_to_join = prepare_dataframes_to_join(cleaned_movies_history)

    overall_df = dataframes_to_join[0].join(dataframes_to_join[1:], how="outer")
    mergeable_flix = overall_df.reset_index()
    return mergeable_flix
