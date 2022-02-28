import re

from src.compile import pd

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
    'dub_European Spanish [English-Delayed]',
    'dub_Polish - Dubbing',
    'dub_English [Hindi-Delayed]',
    'dub_European Spanish [English-Pending]',
    'dub_Brazilian Portuguese [English-Pending]',
    'dub_Hindi [English-Delayed]',
    'dub_Japanese [English-Delayed]',
    'dub_Hindi [English-Pending]',
    'dub_I',
    'dub_Polish -',
    'dub_Br',
    'dub_European Spanish - Dubbed',
    'dub_Brazilian Portuguese [English-Delayed]',
    'dub_Brazilian Portugues',
    'dub_Portugues',
    'dub_Spanish -',
    '',
]

REPLACE_DICT = {
    'sub_English (India)': 'sub_English',
    'sub_Arabic (Egypt)': 'sub_Arabic',
    'sub_Serbian (Latin)': 'sub_Serbian',
    'sub_Arabic (Lebanon)': 'sub_Arabic',
    'sub_Traditional Chinese (Hong Kong SAR China)': 'sub_Traditional Chinese',
    'sub_Arabic (Saudi Arabia)': 'sub_Arabic',
    'sub_European Spanish': 'sub_Spanish',
    'sub_British English': 'sub_English',
    'sub_Polish - Lektor': 'sub_Polish',
    'sub_Brazilian Portuguese': 'sub_Portuguese',

    'dub_Mandarin (Putonghua)': 'dub_Mandarin',
    'dub_Arabic (Palestine)': 'dub_Arabic',
    'dub_Arabic (Syria)': 'dub_Arabic',
    'dub_Arabic (Egypt)': 'dub_Arabic',
    'dub_Mandarin (Guoyu)': 'dub_Mandarin',
    'dub_European Spanish': 'dub_Spanish',
    'dub_British English': 'dub_English',
    'dub_Polish - Lektor': 'dub_Polish',
    'dub_Mexican Spanish': 'dub_Spanish',
    'dub_Brazilian': 'dub_Portuguese',
    'dub_Brazilian Portuguese': 'dub_Portuguese',
}


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
    def consolidate_column(row, replace_dict):
        for key, value in replace_dict.items():
            try:
                row[value] = bool(row.get(key, False) or row.get(value, False))
            except KeyError:
                pass

    def consolidate_all_columns(df):
        df.apply(lambda x: consolidate_column(x, REPLACE_DICT), axis=1)
        languages_to_drop = list(REPLACE_DICT.keys())
        sub_df = df.drop(languages_to_drop, axis=1, errors='ignore')
        return sub_df

    def replace_china_columns(df):
        df['sub_Mandarin (Simplified)'] = df.pop('sub_Simplified Chinese')
        df['dub_Mandarin (Simplified)'] = df.pop('dub_Mandarin')
        df['sub_Cantonese (Traditional)'] = df.pop('sub_Traditional Chinese')
        df['dub_Cantonese (Traditional)'] = df.pop('dub_Cantonese')
        return df

    pass_1 = consolidate_all_columns(df)
    result_df = replace_china_columns(pass_1)

    return result_df


def clean_unogs(unogs_df: pd.DataFrame) -> pd.DataFrame:
    col_list = perform_all_cleaning(unogs_df.columns)
    cleaned_unogs_df = unogs_df[col_list]
    result = replace_columns(cleaned_unogs_df)
    return result


def melt_grouped_df(grouped_df) -> pd.DataFrame:
    melted_df = pd.melt(grouped_df, id_vars=['title', 'Original Language', 'Country', 'slug'],
                        value_vars=[item for item in list(grouped_df.columns) if item.startswith('grp')])

    melted_df['Group'], melted_df['Language'] = melted_df['variable'].apply(lambda x: x.split('_')[1]), melted_df[
        'variable'].apply(lambda x: x.split('_')[-1])

    melted_df = melted_df.rename(columns={'value': 'Group Value'})

    melted_df = melted_df[
        ['title', 'Original Language', 'Country', 'Group', 'Language', 'Group Value', 'slug']]

    return melted_df
