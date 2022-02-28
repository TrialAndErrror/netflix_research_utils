import os
from datetime import datetime
from pathlib import Path

from src.compile import pd

from src.compile.functions.clean_unogs_data import clean_unogs, melt_grouped_df
from src.compile.functions.make_groups import perform_make_exclusive


def check_for_required_files():
    input_dir_name = 'inputs'
    input_path = Path(os.getcwd(), input_dir_name)
    parts_dir_name = 'parts'
    parts_path = Path(os.getcwd(), parts_dir_name)

    input_path.mkdir(exist_ok=True)
    parts_path.mkdir(exist_ok=True)

    file_path = {
        'unogs': Path(input_path, 'final_unogs_df.csv'),
        'trends': Path(input_path, 'google_trends_data.csv'),
        'nf_dict': Path(input_path, 'netflix_nametags.json'),
        'flix_top10': Path(input_path, 'history_results.json'),
        'flix_country': Path(input_path, 'country_results.json'),
    }

    for file in file_path.values():
        if not file.exists():
            raise FileNotFoundError(f'Missing Required Input File: {file}')

    return file_path, input_path, parts_path


def create_output_folder():
    output_folder = Path(os.getcwd(), 'output', f'Compile Results: {datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    output_folder.mkdir(exist_ok=True, parents=True)
    return output_folder


def new_clean_col_names(final_df):
    columns_to_remove = ['Unnamed: 0', 'level_0', 'level_1']
    for col_name in columns_to_remove:

        if col_name in final_df.columns:
            final_df = final_df.drop(col_name, axis=1)

    final_columns = [
        'title',
        'Original Language',
        'Country',
        'Group',
        'Group Value',
        'Language',
        'Primary Language',
        'Secondary Language',
        'Tertiary Language',
        'Google Trends Score',
        'slug',
        'Points',
        'Days',
        'ø/day',
        'Country Top 10'
    ]

    return final_df[final_columns]


def load_or_create_unogs_df(nf_originals, file_path, parts_path):
    original_languages_to_replace = {
            'Brazilian Portuguese': 'Portuguese',
            'Mandarin (Putonghua)': 'Mandarin',
            'European Spanish': 'Spanish',
            'Mandarin (Guoyu)': 'Mandarin',
            'English (India)': 'English',
            'Arabic (Lebanon)': 'Arabic'
        }

    nf_slugs = [item['slug'] for item in nf_originals]

    print('\nLoading UNOGS Data')
    unogs_df_path = Path(parts_path, '[p]unogs_df.csv')
    if not unogs_df_path.exists():
        unogs_df = pd.read_csv(file_path['unogs'])
        unogs_df = unogs_df[unogs_df['slug'].isin(nf_slugs)]
        unogs_df = clean_unogs(unogs_df)
        unogs_df.to_csv(unogs_df_path)
    else:
        unogs_df = pd.read_csv(unogs_df_path)

    print('\nGrouping UNOGS Data')
    grouped_df_path = Path(parts_path, '[p]grp_unogs_df.csv')
    if not grouped_df_path.exists():
        grouped_df = perform_make_exclusive(unogs_df)
        grouped_df.to_csv(grouped_df_path)
    else:
        grouped_df = pd.read_csv(grouped_df_path)

    print('\nMelting UNOGS Data')
    melted_df_path = Path(parts_path, '[p]melt_unogs_df.csv')
    if not melted_df_path.exists():
        grp_col_list = ['title', 'Original Language', 'Country', 'slug']
        grp_col_list.extend([item for item in grouped_df.columns if item.startswith('grp')])
        melted_df = melt_grouped_df(grouped_df[grp_col_list])
        melted_df = melted_df[
            ['title', 'Original Language', 'Country', 'Group', 'Group Value', 'Language', 'slug']
        ]

        melted_df['Original Language'] = melted_df['Original Language'].replace(original_languages_to_replace)
        melted_df.to_csv(melted_df_path)
    else:
        melted_df = pd.read_csv(melted_df_path, dtype={
            'Original Language': 'category',
            'Group': 'category',
            'Language': 'category'
        })

    return melted_df
