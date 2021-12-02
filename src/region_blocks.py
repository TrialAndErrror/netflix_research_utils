import logging

from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By

"""
XPATH Constants:

These are the absolute references to the elements that we need to interact with.
"""
COUNTRY_NAME_SUFFIX = '/span'
DUB_LIST_SUFFIX = '/div/div[1]'
SUB_LIST_SUFFIX = '/div/div[2]'
BUTTON_SUFFIX = '/button[1]'


def click_more_button(driver, xpath, title):
    """
    Find and click the "more" button for Subbed or Dubbed languages list.

    UNOGS only shows one language at first, and makes you click to see more.

    xpath parameter provided is the XPATH to the div containing the list of languages;
    we add the button suffix to tell it to click the button specifically.

    title parameter is used for logging; if we cannot find a "more" button,
    the log will indicate the title to double-check whether there should have been
    a "more" button.

    :param driver: Webdriver
    :param xpath: str
    :param title: str
    :return: None
    """

    button = driver.find_element(By.XPATH, xpath + BUTTON_SUFFIX)

    try:
        button.click()
    except ElementNotInteractableException:
        """
        Log if there was no "more" button; if the title has multiple languages, and
        the "more" button was not found, this would indicate an actual issue.
        """
        logging.debug(f'Button at {xpath} not interactable.')
        logging.debug(f'Looks like {title} may have limited language availability')


def process_region_blocks(driver, region_blocks, title):
    """
    Process all region blocks for a given movie page

    :param driver: Webdriver
    :param region_blocks: list(str, Webdriver.element)
    :param title: str
    :return: dict
    """
    languages = {}

    """
    Looping through every region block for the given movie:
    """
    for xpath, region_block in region_blocks:
        """
        Get the XPATH for the Country Div,
        then extract the title of the country as country_name
        """
        country_xpath = xpath + COUNTRY_NAME_SUFFIX
        country_div = driver.find_element(By.XPATH, country_xpath)
        country_name = country_div.text

        """
        Get the XPATH of the divs for Sub list and Dub list.
        """
        subs_div_xpath = xpath + SUB_LIST_SUFFIX
        dubs_div_xpath = xpath + DUB_LIST_SUFFIX

        """
        If there is a "more" button in the list of Subs and/or Dubs, click it.
        """
        click_more_button(driver, subs_div_xpath, title)
        click_more_button(driver, dubs_div_xpath, title)

        """
        Get the element for the Subs div and Dubs div using its XPATH.
        """
        subs_div = driver.find_element(By.XPATH, subs_div_xpath)
        dubs_div = driver.find_element(By.XPATH, dubs_div_xpath)

        """
        Read the Subs div and Dubs div to get a list of languages available.
        
        .text attribute of a div gives you the text in the div;
        
        then split on the ':' because the Dubs div starts with "Audio" and Subs div
        starts with "Subtitles";
        
        then select element 1 (the second element, because python is a 0-index language)
        which is the string representation of the list of languages.
        
        Note that they are strings and not lists; if we want lists later, we can use split
        again to split on commas and make a list.
        
        """
        subs_list_str = subs_div.text.split(':', maxsplit=1)[1]
        dubs_list_str = dubs_div.text.split(':', maxsplit=1)[1]

        """
        Add the list of subbed and dubbed languages to our languages dict;
        the key is the title of the movie.
        
        Ex:
        "Japan": {
            "Sub": "Japanese",
            "Dub": "Japanese [Original]"
        }
        
        """
        languages[country_name] = {
            'Sub': subs_list_str,
            'Dub': dubs_list_str
        }

    """
    Example of final languages dictionary:
    "Kiba: The Fangs of Fiction": {
        "Japan": {
            "Sub": "Japanese",
            "Dub": "Japanese [Original]"
        }
    }
    """
    return languages


LANGUAGE_BLOCK_XPATH = "/html/body/div[7]/div[3]/div[5]/div[3]"


def check_all_region_blocks(driver):
    """
    Uses the WebDriver to find up to 100 language blocks on a movie's page.

    :param driver: Webdriver
    :return: list(str, Webdriver.element)
    """
    region_blocks = []

    for num in range(1, 100):
        try:
            """
            Check to see if the language block exists with the current num.
            """
            xpath = LANGUAGE_BLOCK_XPATH + f'/div[{num}]'
            region_block = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            """
            If no block exists with that num, Webdriver raises NoSuchElementException.
            This means that we have reached the end of the list of language divs, 
            so we can break out of the loop and move forward with this movie.
            """
            break
        else:
            """
            If the block exists, add the expath and the block element to our
            list of region blocks.
            """
            region_blocks.append((xpath, region_block))

    return region_blocks
