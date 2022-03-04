import json
from pathlib import Path
from typing import Tuple, List

import pandas as pd

KEY_COLUMNS = {
    'Languages': ['Language', 'Count'],
    'Countries': ['Country', 'Count'],
    'Subbed': ['Sub Language', 'Count'],
    'Dubbed': ['Dub Language', 'Count'],
}


def count_rows(language: str, filtered_df: pd.DataFrame) -> Tuple[str, int]:
    return language, int(filtered_df.title.count())


def count_unique_titles(language: str, filtered_df: pd.DataFrame) -> Tuple[str, int]:
    return language, int(filtered_df.title.nunique())


def save_split_excel(output_path: Path, data_dict: dict):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    for key, value in data_dict.items():
        columns = KEY_COLUMNS.get(key, ['index', 'value'])
        df = pd.DataFrame.from_records(value, columns=columns).set_index(columns[0])
        df.to_excel(writer, sheet_name=f'{key}')
    writer.save()


def save_json(path: Path, data_dict: dict):
    with open(path, 'w+') as file:
        json.dump(data_dict, file, indent=2)


def sort_list(data_list):
    return sorted(data_list, key=lambda x: x[0])
