import re

from bs4 import BeautifulSoup

from src.flix.utils.debug_messages import print_red


def check_for_missing_data(soup: BeautifulSoup) -> bool:
    """
    Read soup object and look for the Content div;
    search for 'No Streaming Data' in Content;
    return bool reflecting whether the string is present
    (i.e. whether there is no Netflix data in the soup).

    :param soup: BeautifulSoup
    :return: bool
    """
    try:
        content_div = soup.find_all('div', {'class': 'content'})[-1]
    except IndexError:
        return True
    except TypeError:
        print_red('Error: Object text might not exist')
        print(f'Corrupted text: {soup}')
        return True
    else:
        return bool(re.search('No streaming data', content_div.text))
