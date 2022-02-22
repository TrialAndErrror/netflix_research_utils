import datetime
from pathlib import Path

import pandas as pd

from src.trends.functions.files import get_file_path, read_pytrends_data
from src.trends.functions.network import get_pytrends_data
from src.utils import read_json


def load_or_fetch_data(keyword, slug, timeframe):
    if not str(timeframe) == 'nan':

        if keyword == 'Unknown':
            keyword = slug

        file_path = get_file_path(slug, timeframe)

        print(f'Working on {keyword}')

        if file_path.exists():
            print('Pickle Found')
            return read_pytrends_data(file_path)
        else:
            print('Fetching Data')
            return get_pytrends_data(keyword, slug, timeframe, file_path)


def create_date_range_column(df):
    df['Premiere Date'] = pd.to_datetime(df['date'])
    df['End Date'] = df['Premiere Date'] + datetime.timedelta(days=30)
    df['Date Range'] = df['Premiere Date'].dt.strftime('%Y-%m-%d') + " " + df['End Date'].dt.strftime('%Y-%m-%d')
    return df


def process_df_lines(df):
    results = []

    for title, timeframe, slug in zip(df['title'], df['Date Range'], df['slug']):
        data = load_or_fetch_data(title, slug, timeframe)
        if isinstance(data, pd.DataFrame):
            results.append(data.T)

    return add_slug_column(pd.concat(results))


def add_slug_column(new_df):
    slug_lookup_dict = {item['title']: item['slug'] for item in read_json(Path('netflix_nametags.json'))}
    new_df = new_df.rename_axis('title').reset_index()
    new_df['slug'] = new_df['title'].apply(lambda x: slug_lookup_dict.get(x))
    return new_df
