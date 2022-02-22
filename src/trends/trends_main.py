import pandas as pd
from pathlib import Path
import datetime
import pickle
import os

from pytrends.exceptions import ResponseError
from pytrends.request import TrendReq

from src.utils import read_json

pytrend = TrendReq()

PICKLE_FOLDER = Path(os.getcwd(), 'pickles')


def get_file_path(key, timeframe):
    return Path(PICKLE_FOLDER, f'{key}: {timeframe}.pickle')


def get_pytrends_data(keyword, slug, timeframe, file_path):
    try:
        pytrend.build_payload([keyword], timeframe=timeframe)
    except ResponseError as e:
        try:
            pytrend.build_payload([slug], timeframe=timeframe)
        except ResponseError as e:
            print(f'Error with {keyword}: {e}')
            return None
    else:
        try:
            data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
        except ResponseError as e:
            print(f'Error with {keyword}')
        else:
            with open(file_path, 'wb+') as outfile:
                pickle.dump(data, outfile)

            return data


def read_pytrends_data(file_path):
    with open(file_path, 'rb') as infile:
        data = pickle.load(infile)

    return data


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


def process_df_line(df):
    keyword = df.title
    slug = df.slug
    timeframe = df['Date Range']
    os.makedirs(PICKLE_FOLDER, exist_ok=True)
    print(f'({df["Unnamed: 0"]}) Working on {keyword}')
    result = load_or_fetch_data(keyword, slug, timeframe)
    try:
        result = result.T.reset_index()
    except AttributeError:
        result = None
    return result


def create_date_range_column(df):
    df['Premiere Date'] = pd.to_datetime(df['date'])
    df['End Date'] = df['Premiere Date'] + datetime.timedelta(days=30)
    df['Date Range'] = df['Premiere Date'].dt.strftime('%Y-%m-%d') + " " + df['End Date'].dt.strftime('%Y-%m-%d')
    return df


def debug():
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)
    process_df_line(total_df.loc[0])


def process_df_lines(df):
    results = []

    for title, timeframe, slug in zip(df['title'], df['Date Range'], df['slug']):
        data = load_or_fetch_data(title, slug, timeframe)
        if isinstance(data, pd.DataFrame):
            results.append(data.T)

    return pd.concat(results)


def trends_main():
    # run_trends_data()
    print('Starting Google Trends processing...')

    output_dir = Path(os.getcwd(), 'results')
    output_dir.mkdir(exist_ok=True)
    PICKLE_FOLDER.mkdir(exist_ok=True)

    print('Making Date Range Columns')

    netflix_nametags_file = Path(os.getcwd(), 'netflix_nametags.json')
    if not netflix_nametags_file.exists():
        raise FileNotFoundError('Missing Netflix Nametags file')

    netflix_titles_df = pd.DataFrame(read_json(netflix_nametags_file))
    total_df = create_date_range_column(netflix_titles_df)

    print('Fetching Data')
    new_df = process_df_lines(total_df)
    slug_lookup_dict = {item['title']: item['slug'] for item in read_json(Path('netflix_nametags.json'))}
    new_df = new_df.rename_axis('title').reset_index()
    new_df['slug'] = new_df['title'].apply(lambda x: slug_lookup_dict.get(x))

    new_df.to_csv(Path(output_dir, 'trends_data_output.csv'))
    return output_dir


if __name__ == '__main__':
    trends_main()

