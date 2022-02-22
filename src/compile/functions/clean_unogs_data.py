import re

import pandas as pd

REMOVE_LIST = [
        'Unnamed: 0',
        'Unnamed: 0.1',
        'dub_Pol',
        'dub_Hin',
        'dub_Ar',
        'dub_Po',
        'dub_Ita',
        'dub_Itali',
        'dub_Spanish -',
        'dub_Br',
        'dub_I',
        'dub_Spani',
]

MANUAL_REMOVAL = [
        # 'sub_Arabic (Saudi Arabia)',
        # 'sub_Traditional Chinese (Hong Kong SAR China)',
        # 'sub_Arabic (Egypt)',
        # 'sub_Canadian French',
        # 'sub_Serbian (Latin)',
        # 'sub_Brazilian Portuguese',
        # 'sub_Mandarin',
        # 'sub_Mandarin (Guoyu)',
        'dub_European Spanish [English-Delayed]',
        'dub_Polish - Dubbing',
        # 'dub_Mandarin (Putonghua)',
        'dub_English [Hindi-Delayed]',
        # 'dub_Polish - Lektor',
        'dub_European Spanish [English-Pending]',
        'dub_Brazilian Portuguese [English-Pending]',
        'dub_Hindi [English-Delayed]',
        'dub_Japanese [English-Delayed]',
        'dub_Hindi [English-Pending]',
        'dub_I',
        'dub_Polish -',
        # 'dub_Mandarin (Guoyu)',
        'dub_Br',
        # 'dub_Arabic (Palestine)',
        'dub_European Spanish - Dubbed',
        'dub_Brazilian Portuguese [English-Delayed]',
        # 'dub_Arabic (Egypt)',
        'dub_Brazilian Portugues',
        'dub_Portugues',
        # 'dub_Mexican Spanish',
        'dub_Spanish -',
        # 'dub_Brazilian',
        '',
]


def find_and_remove_pattern(pattern, mylist):
    """
    Generic function for finding column names based on Regular Expression pattern matching.\n",
    
    :param pattern:",
    :param mylist:",
    :return: None",
    """
    r = re.compile(pattern)
    matches = list(filter(r.match, mylist))
    return [item for item in mylist if item not in matches]


def remove_season_columns(mylist):
    """
    Remove Audio Description columns by looking for - A pattern
    
    (i.e. start of ' - Audio Description')
    """

    return find_and_remove_pattern('.* - A', mylist)


def remove_irrelevant_language_cols(mylist):
    """
    Remove irrelevant language columns, as indicated in R script.
    """
    
    criteria = [
        '\[Original\]',
        'Undefined',
        'Audio',
        'Multiple',
        'Dialogue'
    ]
    new_list = mylist.copy()
    for item in criteria:
        new_list = find_and_remove_pattern(f'.*{item}', new_list)
    return new_list


def remove_specific_columns(mylist):
    """
    Remove extra specified columns.
    """
    removal_list = REMOVE_LIST + MANUAL_REMOVAL
    # removal_list = REMOVE_LIST
    return [item for item in mylist if item not in removal_list]


def perform_all_cleaning(col_list):
    operations = [
        remove_season_columns,
        remove_irrelevant_language_cols,
        remove_specific_columns,
    ]

    for operation in operations:
        col_list = operation(col_list)

    return col_list


def replace_columns(df):
    replace_dict = {
        'sub_English (India)': 'sub_English',
        'sub_Arabic (Egypt)': 'sub_Arabic',
        'sub_Serbian (Latin)': 'sub_Serbian',
        'sub_Arabic (Lebanon)': 'sub_Arabic',
        'sub_Traditional Chinese (Hong Kong SAR China)': 'sub_Traditional Chinese',
        'sub_Arabic (Saudi Arabia)': 'sub_Arabic',

        'dub_Mandarin (Putonghua)': 'dub_Mandarin',
        'dub_Arabic (Palestine)': 'dub_Arabic',
        'dub_Arabic (Syria)': 'dub_Arabic',
        'dub_Arabic (Egypt)': 'dub_Arabic',
        'dub_Mandarin (Guoyu)': 'dub_Mandarin'
    }

    def consolidate_column(row, replace_dict):
        for key, value in replace_dict.items():
            try:
                row[value] = bool(row[key] or row[value])
            except KeyError:
                pass

    def consolidate_all_columns(df):
        df.apply(lambda x: consolidate_column(x, replace_dict), axis=1)
        languages_to_drop = list(replace_dict.keys())
        sub_df = df.drop(languages_to_drop, axis=1, errors='ignore')
        return sub_df

    return consolidate_all_columns(df)


def clean_unogs(unogs_df: pd.DataFrame):
    col_list = perform_all_cleaning(unogs_df.columns)
    cleaned_unogs_df = unogs_df[col_list]
    # cleaned_unogs_df.to_csv('clean_unogs_df.csv')
    return replace_columns(cleaned_unogs_df)

