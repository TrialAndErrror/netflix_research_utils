from src.utils import read_json
from src.compile import pd


def clean_flix_countries(file_path):
    country_info = read_json(file_path)
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

    df_to_melt = countries_df.reset_index()

    melted_top10_df = pd.melt(df_to_melt, id_vars=['index'])

    melted_top10_df['Top 10 Country'] = melted_top10_df['variable'].apply(lambda x: x.split('_')[1])
    melted_top10_df = melted_top10_df.rename(columns={'value': 'Country Top 10'})

    return melted_top10_df[['index', 'Top 10 Country', 'Country Top 10']]


def merge_with_flix_countries(working_df, flixpatrol_df_path):
    flixpatrol_countries_dataframe = clean_flix_countries(flixpatrol_df_path)
    working_df = working_df.merge(flixpatrol_countries_dataframe, left_on=['slug', 'Country'], right_on=['index', 'Top 10 Country'], how='left')

    """
    Option 1: Fill NA values in Top 10 Country with the Country from the row,
    and fil NA values in Country Top 10 (bool) with False, since they inherently didn't appear.
    """
    working_df['Top 10 Country'] = working_df['Top 10 Country'].fillna(working_df['Country'])
    working_df['Country Top 10'] = working_df['Country Top 10'].fillna(False)

    """
    Option 2: Just filter to values where Top 10 Country matches with the Country of the row.
    This results in losing a lot of rows where the movie was not present in Top 10 Country dataset.
    """
    # working_df = working_df[working_df['Country'] == working_df['Top 10 Country']]
    return working_df
