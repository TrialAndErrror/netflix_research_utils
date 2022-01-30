from pathlib import Path
from notebook_utils.anova_models import AnovaAnalysis
import pandas as pd


REGRESSION_EXAMPLES = {
    '1': '1. search_interest ~ group'
}


def get_anova_loop() -> str:
    [print(value) for value in REGRESSION_EXAMPLES.values()]
    anova_loop = True
    while anova_loop:
        anova_model = input('Choose Number or Enter Custom OLS Regression Formula:')
        if '~' not in anova_model:
            chosen = REGRESSION_EXAMPLES.get(anova_model)
            if chosen:
                result = chosen.split('. ')[1]
                print(f'Using ({result}) as ANOVA model\n')
                return result
            else:
                print('Error: invalid syntax. Please include a ~ in your ANOVA formula or choose a number.')
        else:
            print(f'Using ({anova_model}) as ANOVA model\n')
            return anova_model


def get_df_file_loop() -> Path:
        df_loop = True
        while df_loop:
            df_path = input('Enter filename/path for Dataframe CSV File: ')
            result = Path(df_path)
            if not result.exists():
                print('Error: File not found. Please enter a valid filename or path to csv file.')
            else:
                print(f'Loading {result.absolute()}\n')
                return result


def get_country_loop(df: pd.DataFrame) -> str:
    countries = list(df.country.unique())
    df_loop = True
    while df_loop:
        print(f'Countries available: {countries}')
        country = input('Enter country to analyze: ')
        if country not in countries:
            country = country.capitalize()
            if country not in countries:
                print(f'Error: Country {country} not found in {countries}.'
                      f'\nPlease choose a valid country name, including capitalization')
            else:
                print(f'Using {country} for analysis.\n')
                return country
        else:
            print(f'Using {country} for analysis.\n')
            return country


def anova_interactive():
    print('\n\nANOVA Analysis by Country' + '-'*75 + '\n')
    while True:
        anova_model = get_anova_loop()
        df_path = get_df_file_loop()
        country = get_country_loop(pd.read_csv(df_path))

        current_analysis = AnovaAnalysis(df_path, country, anova_model)
        current_analysis.run_analysis()

        response = input('Run another analysis? Y/N')
        if response.upper() in ['N', 'NO', 'STOP', 'EXIT', 'CLOSE', 'S', 'X', 'Q']:
            break


if __name__ == '__main__':
    anova_interactive()
