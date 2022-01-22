from selenium import webdriver

from src.unogs.region_blocks import check_all_region_blocks, process_region_blocks
from src.unogs import DEBUG, MAX_COUNT
from src.unogs.file_commands import load_pickle, save_pickle
from slugify import slugify


def process_movie_entry(driver: webdriver, nfid: str, title: str):
    """
    Process one movie entry

    :param driver: Webdriver
    :param nfid: str
    :param title: str
    :return: None
    """

    """
    Identify url based on netflix id, then load page in Webdriver
    """
    url = f"https://unogs.com/title/{nfid}"
    driver.get(url)

    """
    Check for region blocks, returning XPATH and element of each region block.
    """
    region_blocks = check_all_region_blocks(driver)

    """
    If region blocks found, loop through them and process them.
    """
    if len(region_blocks) > 0:
        data = {
            'nfid': nfid,
            'title': title,
        }
        languages = process_region_blocks(driver, region_blocks, title)
        data['languages'] = languages
        save_pickle(data, f'{slugify(title)}.pickle')

        return languages


def run_with_limit(nf_dict: dict):
    """
    Loop through all NetFlix titles in nf_dict and get subs and dubs.

    Uses MAX_COUNT to limit number of movies to fetch.

    :param nf_dict: dict
    :return: dict
    """

    """
    Create WebDriver.
    Tells WebDriver to generally wait 2 seconds between requests.
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    count = 0
    movie_data = {}
    total_count = MAX_COUNT
    """
    Process each movie in the dictionary.
    """
    for title, nfid in nf_dict.items():
        """
        Notify user that the program is still running
        """
        print(f'Working on {title}: [{count}/{total_count}]')

        """
        Try to load data from pickle.
        If pickle doesn't exist, then we process the movie entry
        """

        try:
            data = load_pickle(f'{slugify(title)}.pickle')
        except FileNotFoundError:
            result = process_movie_entry(driver, nfid, title)
        else:
            result = data.get('languages')

        """
        Process movie entry.
        If result found, we save it in the movie_data dictionary.
        """
        if result:
            movie_data[title] = result
        """
        Count keeps track of number of movies processed.
        Set DEBUG to False to allow it to process the entire file.
        Set MAX COUNT to an integer to set the maximum number of movies to process.
        """
        count += 1
        if count >= MAX_COUNT and DEBUG:
            break

    """
    Close and quit Webdriver
    """
    driver.close()
    driver.quit()

    return movie_data


def run_all_movies(nf_dict: dict):
    """
    Loop through all NetFlix titles in nf_dict and get subs and dubs.

    :param nf_dict: dict
    :return: dict
    """

    """
    Create WebDriver.
    Tells WebDriver to generally wait 2 seconds between requests.
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    movie_data = {}
    count = 1
    total_count = len(nf_dict)
    """
    Process each movie in the dictionary.
    """
    for title, nfid in nf_dict.items():
        print(f'Working on {title}: [{count}/{total_count}]')

        try:
            data = load_pickle(f'{slugify(title)}.pickle')
        except FileNotFoundError:
            result = process_movie_entry(driver, nfid, title)
        else:
            result = data.get('languages')

        """
        Process movie entry.
        If result found, we save it in the movie_data dictionary.
        """
        if result:
            movie_data[title] = result

        count += 1

    """
    Close and quit Webdriver
    """
    driver.close()
    driver.quit()

    return movie_data
