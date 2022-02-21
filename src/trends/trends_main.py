import pandas as pd
from pytrends.request import TrendReq
from pathlib import Path
import datetime
import pickle
import os
import json
from pytrends.exceptions import ResponseError

pytrend = TrendReq()

PICKLE_FOLDER = Path(os.getcwd(), 'old_data/pickles')


def get_file_path(key, timeframe):
    return Path(PICKLE_FOLDER, f'{key}: {timeframe}')


def get_pytrends_data(keyword, timeframe, file_path):
    pytrend.build_payload([keyword], timeframe=timeframe)
    try:
        data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    except ResponseError as e:
        # data = f'Error: {e}'
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
    if keyword == 'Unknown':
        keyword = slug

    file_path = get_file_path(keyword, timeframe)

    print(f'Working on {keyword}')
    if file_path.exists():
        print('Pickle Found')
        return read_pytrends_data(file_path)
    else:
        print('Fetching Data')
        return get_pytrends_data(keyword, timeframe, file_path)


def process_df_line(df):
    keyword = df.title
    timeframe = df['Date Range']
    os.makedirs(PICKLE_FOLDER, exist_ok=True)
    print(f'({df["Unnamed: 0"]}) Working on {keyword}')
    result = load_or_fetch_data(keyword, timeframe)
    try:
        result = result.T.reset_index()
    except AttributeError:
        result = None
    return result


def create_date_range_column(df):
    df['Premiere Date'] = pd.to_datetime(df['Premiere Date'])
    df['End Date'] = df['Premiere Date'] + datetime.timedelta(days=30)
    df['Date Range'] = df['Premiere Date'].dt.strftime('%Y-%m-%d') + " " + df['End Date'].dt.strftime('%Y-%m-%d')
    return df


def debug():
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)
    process_df_line(total_df.loc[0])


def run_trends_data():
    output_dir = Path(os.getcwd(), 'old_data/results')
    output_dir.mkdir(exist_ok=True)
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)
    applied_df = total_df.apply(lambda df_param: process_df_line(df_param), axis=1, result_type='expand')
    df = pd.concat([total_df, applied_df], axis='columns')
    df.to_csv(Path(output_dir, 'trends_data_output.csv'))


def process_df_lines(df):
    results = [
        load_or_fetch_data(title, slug, timeframe).T
        for title, timeframe, slug
        in zip(df['title'], df['Date Range'], df['slug'])
    ]

    return pd.concat(results)


def trends_main():
    # run_trends_data()
    print('Starting Google Trends processing...')

    output_dir = Path(os.getcwd(), 'old_data/results')
    output_dir.mkdir(exist_ok=True)

    print('Making Date Range Columns')
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)

    print('Fetching Data')
    new_df = process_df_lines(total_df)
    new_df.to_csv(Path(output_dir, 'trends_data_output.csv'))
    return output_dir


if __name__ == '__main__':
    trends_main()

