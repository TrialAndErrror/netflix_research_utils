import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By

from src.won.xpaths import NEXT_BUTTON, get_row_xpath, EXPAND_BUTTON_CELL, get_title_cell, get_netflix_url_cell, ENTRY_TABLE
from src.won import get_output_filename, BASE_URL, log_error, log_debug
from src.utils import write_file

END_FLAG = False


def setup_driver():
    """
    Setup for Webdriver.

    This is the core of Selenium, and includes the setting to wait for 2 seconds for each new request.

    :return: webdriver
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    return driver


def scroll_to_element(element, driver):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def count_rows(driver):
    xpath = f'{ENTRY_TABLE}/tr'
    rows = driver.find_elements(By.XPATH, xpath)
    return len(rows)


def expand_all_rows(driver, rows):
    """
    Iterate over each row in the Netflix Movie table, and click on the first cell in order to expand the data for each
    row.

    :param driver: webdriver

    """

    """
    We iterate over all 25 rows in reverse, since clicking to expand increases the number of rows;
    starting with the bottom means we won't have to compensate for the new rows that are created.
    """
    for row_num in range(rows, 0, -1):
        xpath = f'{get_row_xpath(row_num)}{EXPAND_BUTTON_CELL}'
        button = driver.find_element(By.XPATH, xpath)

        """
        Scroll to the element so that no ads are in the way.
        """
        scroll_to_element(button, driver)
        """
        Try to click on the button to expand
        """
        try:
            button.click()
        except ElementNotInteractableException:
            """
            Log if the expand button is not found
            """
            log_error(f'Expand Button not found for row {row_num} at XPath {xpath}.')

        time.sleep(.3)


def get_all_movies(driver: webdriver, movie_info: dict, rows: int):
    """
    Iterate over table rows and gather the Title and Netflix ID from each row.

    :param driver: webdriver
    """
    for row_num in range(1, rows * 2, 2):
        print(f'Found Row {row_num}: ', end='')
        """
        Get text for title
        """
        title_xpath = get_title_cell(row_num)
        try:
            title_element = driver.find_element(By.XPATH, title_xpath)
        except NoSuchElementException:
            log_error(f'Could not find title element at {title_xpath}; check script')
            continue
        else:
            """
            Scroll to title element and grab the text.
            """
            scroll_to_element(title_element, driver)
            title_text = title_element.text
            print(f'{title_text} ', end='')

            """
            Get the hyperlink reference for the Netflix URL,
            then split by slashes and take the last bit to get the netflix id.
            """
            netflix_xpath = get_netflix_url_cell(row_num)
            try:
                netflix_element = driver.find_element(By.XPATH, netflix_xpath)
                netflix_url = netflix_element.get_attribute("href")
            except NoSuchElementException:
                log_error(f'Could not find netflix url element at {netflix_xpath}; check script')
                continue
            else:
                netflix_id = netflix_url.split('/')[-1]
                print(f'(ID #{netflix_id}) ')

                """
                Add title and netflix ID to our dictionary
                """
                movie_info[title_text] = netflix_id

    return movie_info


def turn_page(driver: webdriver):
    """
    Attempt to turn the page.

    :param driver: webdriver
    :return: bool
    """
    global END_FLAG
    next_button = driver.find_element(By.XPATH, NEXT_BUTTON)
    is_active = "disabled" not in next_button.get_attribute("class")
    try:
        next_button.click()
    except ElementNotInteractableException:
        """
        Log if the next button is not interactable.
        
        If we run into this issue multiple times, then it means there's a problem.
        Theoretically this should only be raised once, at the very end, 
        so we return False so that we can exit the loop and close the driver.
        """
        if END_FLAG:
            log_error('Next Button found to not be interactable multiple times; something went wrong!')
        else:
            log_debug(f'Next Button not interactable; we may have reached the end of the list.')
            END_FLAG = True
        return False
    else:
        return is_active


def get_site_data():
    """
    Fetch all site data from What's On Netflix
    """

    """
    Setup Webdriver and load base page
    """
    driver: webdriver = setup_driver()
    driver.get(BASE_URL)

    print('Waiting 10 seconds to load page...')
    time.sleep(10)
    """
    Set up dictionary to hold results
    """
    movie_info = {}
    file_name = get_output_filename()
    """
    Loop through each page of results and store the data.
    """
    more_pages: bool = True
    while more_pages:
        """
        Expand rows and get movie data
        """
        row_count = count_rows(driver)
        expand_all_rows(driver, row_count)
        movie_info = get_all_movies(driver, movie_info, row_count)

        """
        Write file once page is done; this way, if it crashes at end, we don't lose data.
        """
        write_file(movie_info, file_name)

        """
        Check if there are more pages, and click next button.
        """
        more_pages = turn_page(driver)

    """
    Once done with the loop, write results to a file.
    """
    print('Finished Collecting Netflix IDs')
    # write_file(movie_info, file_name)

    """
    Close and quit the driver.
    """
    driver.close()
    driver.quit()


if __name__ == '__main__':
    get_site_data()
