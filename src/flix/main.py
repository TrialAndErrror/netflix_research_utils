import requests
import re
from src.flix import BASE_URL, TEST_URL
from src.flix.utils import save_pickle
from slugify import slugify
from src.flix.data import NETFLIX_ORIGINALS


def get_movie(title):
    print(f'Working on {title}')
    slug = slugify(title)
    print(f'Slug: {slug}')
    response = requests.get(f'{BASE_URL}/{slug}')
    soup_data = response.text

    movie_not_found = re.search('Page Not Found', soup_data)
    if movie_not_found:
        return slug
    else:
        save_pickle(soup_data, slug)


def main():
    missing_titles = []

    for movie in NETFLIX_ORIGINALS:
        missing = get_movie(movie)

        if missing:
            missing_titles.append(missing)
            save_pickle(missing_titles, '!!!missing_titles!!!')


if __name__ == '__main__':
    main()
