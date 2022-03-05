import pandas as pd

df_structure = {
    'Canada': {
        'Dutch': {
            0: 'Dataframe in JSON Format',
            1: {
                'W': 'w-value',
                'P': 'p-value'
            }
        }
    }
}


def main(df):
    for country, country_data in df.items():
        for language, langauge_data in country_data.items():
            df = pd.DataFrame.from_langauge_data[0]
            shapiro = langauge_data[1]
    pass


if __name__ == '__main__':
    main()