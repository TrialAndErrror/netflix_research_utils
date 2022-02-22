from slugify import slugify
from pathlib import Path
import pandas as pd

from src.utils import read_json, write_json
from src.nametags import get_input_folder, get_output_folder


def nametag_main():
    output_folder = get_output_folder()
    input_folder = get_input_folder()

    nf_dict = read_json(Path(input_folder, 'nf_dict.json'))
    title_list = list(pd.read_csv(Path(input_folder, 'final_list_of_titles.csv'))['unique.unogs4.title.'].unique())
    nf_dict = {key: value for key, value in nf_dict.items() if key in title_list}

    replacement_dict = pd.read_csv(
        Path(input_folder, 'slug_replacements.csv'), header=None, index_col=0, squeeze=True
    ).to_dict()

    premiere_dates_by_slug = pd.read_csv(
        Path(input_folder, 'premiere_dates_df.csv'), index_col=1
    ).to_dict('index')

    missing_release_dates = {item[0]: item[1] for item in pd.read_csv(
        Path(input_folder, 'missing_release_dates.csv'), header=None
    ).to_dict('records')}

    all_nametags = []
    missing_dates = []

    for title, nfid in nf_dict.items():
        slug = replacement_dict.get(slugify(title), slugify(title))
        data = {
            'title': title,
            'nfid': nfid,
            'slug': slug,
        }

        try:
            data['date'] = premiere_dates_by_slug.get(slug, None)['Premiere Date']
        except TypeError:
            try:
                data['date'] = missing_release_dates.get(title, None)
            except TypeError:
                missing_dates.append(title)
                data['date'] = None

        all_nametags.append(data)

    print(f'Found {len(all_nametags)}')
    write_json(all_nametags, Path(output_folder, 'netflix_nametags.json'))

    print('\nNo Slug provided for following films (based on exclusion policy):')
    [print(item['title']) for item in all_nametags if item['slug'] == 'EXCLUDE']

    if len(missing_dates) > 0:
        print('\nNo Release Date found for following films:')
        [print(item) for item in missing_dates]


if __name__ == '__main__':
    nametag_main()
