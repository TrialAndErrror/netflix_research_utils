import logging

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

from src.won.xpaths import NEXT_BUTTON, get_row_xpath, EXPAND_BUTTON_CELL, get_title_cell, get_netflix_url_cell
from src.won import OUTPUT_FILE, BASE_URL
from src.utils import write_file


def setup_driver():
    """
    Setup for Webdriver.

    This is the core of Selenium, and includes the setting to wait for 2 seconds for each new request.

    :return: webdriver
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    return driver


def expand_all_rows(driver):
    """
    Iterate over each row in the Netflix Movie table, and click on the first cell in order to expand the data for each
    row.

    :param driver: webdriver

    """

    """
    We iterate over all 25 rows in reverse, since clicking to expand increases the number of rows;
    starting with the bottom means we won't have to compensate for the new rows that are created.
    """
    for row_num in range(25, 1, -1):
        xpath = f'{get_row_xpath(row_num)}{EXPAND_BUTTON_CELL}'
        button = driver.find_element(By.XPATH, xpath)

        """
        Try to click on the button to expand
        """
        try:
            button.click()
        except ElementNotInteractableException:
            """
            Log if the expand button is not found
            """
            logging.debug(f'Expand Button not found for row {row_num} at XPath {xpath}.')


def get_all_movies(driver: webdriver):
    """
    Iterate over table rows and gather the Title and Netflix ID from each row.

    :param driver: webdriver
    """
    movie_info = {}
    for row_num in range(1, 50, 2):
        """
        Get text for title
        """
        title_xpath = get_title_cell(row_num)
        title_text = driver.find_element(By.XPATH, title_xpath).text

        """
        Get the hyperlink reference for the Netflix URL,
        then split by slashes and take the last bit to get the netflix id.
        """
        netflix_xpath = get_netflix_url_cell(row_num)
        netflix_url = driver.find_element(By.XPATH, netflix_xpath).get_element("href")
        netflix_id = netflix_url.split('/')[-1]

        """
        Add title and netflix ID to our dictionary
        """
        movie_info[title_text] = netflix_id

    """
    Once done with the loop, write results to a file.
    """
    print('Finished Collecting Netflix IDs')
    write_file(movie_info, OUTPUT_FILE)


def turn_page(driver: webdriver):
    """
    Attempt to turn the page.

    :param driver: webdriver
    :return: bool
    """
    next_button = driver.find_element(By.XPATH, NEXT_BUTTON)
    try:
        next_button.click()
    except ElementNotInteractableException:
        """
        Log if the next button is not interactable.
        
        If we run into this issue multiple times, then it means there's a problem.
        Theoretically this should only be raised once, at the very end, 
        so we return False so that we can exit the loop and close the driver.
        """
        logging.debug(f'Next Button not interactable; we have reached the end of the list.')
        return False
    else:
        return True


def get_site_data():
    """
    Fetch all site data from What's On Netflix
    """

    """
    Setup Webdriver and load base page
    """
    driver: webdriver = setup_driver()
    driver.get(BASE_URL)

    """
    Loop through each page of results and store the data.
    """
    more_pages: bool = True
    while more_pages:
        expand_all_rows(driver)
        get_all_movies(driver)
        more_pages = turn_page(driver)

    """
    Close and quit the 
    """
    driver.close()
    driver.quit()


if __name__ == '__main__':
    get_site_data()
