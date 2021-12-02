from selenium import webdriver

from src.region_blocks import check_all_region_blocks, process_region_blocks
from src import DEBUG, MAX_COUNT


def process_movie_entry(driver, movie_data, nfid, title):
    """
    Process one movie entry

    :param driver: Webdriver
    :param movie_data: dict
    :param nfid: int
    :param title: str
    :return: None
    """

    """
    Notify user that the program is still running
    """
    print(f'Working on {title}')

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
        movie_data[title] = process_region_blocks(driver, region_blocks, title)


def run_with_limit(nf_dict):
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

    """
    Process each movie in the dictionary.
    """
    for title, nfid in nf_dict.items():
        process_movie_entry(driver, movie_data, nfid, title)

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


def run_all_movies(nf_dict):
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

    """
    Process each movie in the dictionary.
    """
    for title, nfid in nf_dict.items():
        process_movie_entry(driver, movie_data, nfid, title)

    """
    Close and quit Webdriver
    """
    driver.close()
    driver.quit()

    return movie_data
