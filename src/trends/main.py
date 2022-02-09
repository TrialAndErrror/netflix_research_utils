import pandas as pd
from pytrends.request import TrendReq
from pathlib import Path
import datetime
import pickle
import os
import json
from pytrends.exceptions import ResponseError

pytrend = TrendReq()

PICKLE_FOLDER = Path(os.getcwd(), 'pickles')


def get_file_path(key, timeframe):
    return Path(PICKLE_FOLDER, f'{key}: {timeframe}')


def get_pytrends_data(keyword, timeframe, file_path):
    pytrend.build_payload([keyword], timeframe=timeframe)
    try:
        data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    except ResponseError as e:
        data = f'Error: {e}'
        print(f'Error with {keyword}')
    with open(file_path, 'wb+') as outfile:
        pickle.dump(data, outfile)

    return data


def read_pytrends_data(file_path):
    with open(file_path, 'rb') as infile:
        data = pickle.load(infile)

    return data


def load_or_fetch_data(keyword, timeframe):
    file_path = get_file_path(keyword, timeframe)

    if file_path.exists():
        return read_pytrends_data(file_path)
    else:
        return get_pytrends_data(keyword, timeframe, file_path)


def process_df_line(df):
    keyword = df.title
    timeframe = df['Date Range']
    os.makedirs(PICKLE_FOLDER, exist_ok=True)
    print(f'({df["Unnamed: 0"]}) Working on {keyword}')
    result = load_or_fetch_data(keyword, timeframe)
    try:
        result = result.reset_index()
    except AttributeError:
        result = None
    return result


def create_date_range_column(df):
    df['Premiere Date'] = pd.to_datetime(df['Premiere Date'])
    df['End Date'] = df['Premiere Date'] + datetime.timedelta(days = 30)
    df['Date Range'] = df['Premiere Date'].dt.strftime('%Y-%m-%d') + " " + df['End Date'].dt.strftime('%Y-%m-%d')
    return df


def debug():
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)
    process_df_line(total_df.loc[0])


def run_trends_data():
    premiere_dates_df = pd.read_csv('./premiere_dates_df.csv')
    total_df = create_date_range_column(premiere_dates_df)
    applied_df = total_df.apply(lambda df_param: process_df_line(df_param), axis='columns', result_type='expand')
    df = pd.concat([total_df, applied_df], axis='columns')
    df.to_csv('trends_data_output.csv')


if __name__ == '__main__':
    run_trends_data()

