import os

from src.utils import read_file, write_file
from slugify import slugify
from pathlib import Path
import pandas as pd


def nametag_main():
    output_folder = Path(os.getcwd(), 'output')
    output_folder.mkdir(exist_ok=True)

    input_folder = Path(os.getcwd(), 'inputs')
    input_folder.mkdir(exist_ok=True)

    nf_dict = read_file(Path(input_folder, 'nf_dict.json'))
    title_list = list(pd.read_csv(Path(input_folder, 'final_list_of_titles.csv'))['unique.unogs4.title.'].unique())
    nf_dict = {key: value for key, value in nf_dict.items() if key in title_list}

    replacement_dict = pd.read_csv(
        Path(input_folder, 'slug_replacements.csv'), header=None, index_col=0, squeeze=True
    ).to_dict()

    premiere_dates_by_slug = pd.read_csv(
        Path(input_folder, 'premiere_dates_df.csv'), index_col=1
    ).to_dict('index')

    all_nametags = []

    for key, value in nf_dict.items():
        slug = replacement_dict.get(slugify(key), slugify(key))

        data = {
            'title': key,
            'nfid': value,
            'slug': slug,
        }

        try:
            data['date'] = premiere_dates_by_slug.get(slug, None)['Premiere Date']
        except TypeError:
            print(f'No premiere date found for {key}')
            data['date'] = None

        all_nametags.append(data)

    print(f'Found {len(all_nametags)}')
    write_file(all_nametags, Path(output_folder, 'netflix_nametags.json'))


if __name__ == '__main__':
    nametag_main()
