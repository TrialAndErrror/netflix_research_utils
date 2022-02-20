import pandas as pd

from slugify import slugify


def slugify_nf_dict(nf_id_dict):
    # slug_to_titles_dict = {slugify(key): key for key in nf_id_dict}

    new_dict = {slugify(key): value for key, value in nf_id_dict.items()}
    return update_movie_titles(new_dict)

    # return slug_to_titles_dict, update_movie_titles(new_dict)


def update_movie_titles(nf_dict) -> dict:
    """
    Update slugs for movie titles that do not have an intuitive slug.

    :param nf_dict: dict
    :return: dict
    """

    """
    Read sheet of changes to dictionary using Pandas
    """
    dict_from_csv = pd.read_csv('../replacements.csv', header=None, index_col=0, squeeze=True).to_dict()

    for old_title, new_title in dict_from_csv.items():
        nf_dict[new_title] = nf_dict.pop(old_title)

    return nf_dict
