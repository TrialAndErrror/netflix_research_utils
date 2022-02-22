import pickle

from pytrends.exceptions import ResponseError
from pytrends.request import TrendReq

pytrend = TrendReq()


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