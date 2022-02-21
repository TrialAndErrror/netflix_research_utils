import pandas as pd

from slugify import slugify


def slugify_nf_dict(nf_id_dict):
    dict_from_csv = pd.read_csv('replacements.csv', header=None, index_col=0, squeeze=True).to_dict()

    """
    Handle the slug_to_titles dict, which gives us a mapping between titles and actual slugs
    """
    slug_to_titles_dict = {
        key: dict_from_csv.get(slugify(key), slugify(key))      # Run the slug through the dict, or just save slug
        for key in nf_id_dict
    }

    """
    Handle the new_dict, which maps slug to netflix IDs.
    """
    new_dict = {dict_from_csv.get(slugify(key), slugify(key)): value for key, value in nf_id_dict.items()}

    return slug_to_titles_dict, new_dict
