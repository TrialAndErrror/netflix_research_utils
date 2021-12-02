from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename='logs.log',
    format='%(asctime)s %(message)s',
)

from selenium.common.exceptions import NoSuchElementException

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)


# def wait_for_element(driver, by, query):
#     try:
#         # element = WebDriverWait(driver, 10).until(
#         #     EC.presence_of_element_located((by, query))
#         # )
#         element = driver.find_element(by, query)
#     except Exception as e:
#         driver.close()
#         driver.quit()
#         raise e
#     else:
#         return element
#     finally:
#         driver.close()
#         driver.quit()
#
#
# def search_for_title(title):
#     driver = webdriver.Chrome()
#     # driver.implicitly_wait(10)
#     driver.get("https://unogs.com/search/silicon%20valley")
#     time.sleep(10)
#     assert "Netflix" in driver.title
#     search_bar = wait_for_element(driver, By.NAME, "q")
#     # time.sleep(2)
#     # search_bar.clear()
#     search_bar.click()
#     search_bar.send_keys(title)
#     search_bar.send_keys(Keys.RETURN)
#
#     results_count = wait_for_element(driver, By.CLASS_NAME, "alert-info")
#
#     input('Press any key to quit')
#     driver.close()
#     driver.quit()
#
#

US_XPATH = {
    'main': '//*[@id="78"]',
    'MSB': "/html/body/div[6]/div/div/div[3]/div[3]/div[5]/div[3]/div[38]/div/div[3]/button[1]",
    'MDB': "/html/body/div[6]/div/div/div[3]/div[3]/div[5]/div[3]/div[38]/div/div[2]/button[1]",
    'Dub Languages': "/html/body/div[6]/div/div/div[3]/div[3]/div[5]/div[3]/div[38]/div/div[2]",    # div[38] is sequential here, so it needs to be adjusted
    'Sub Languages': "/html/body/div[6]/div/div/div[3]/div[3]/div[5]/div[3]/div[38]/div/div[3]"     # div[38] is sequential here, so it needs to be adjusted
}

CLOSE_BUTTON_XPATH = "/html/body/div[6]/div/div/div[1]/button/span"

REGION_BLOCK_XPATH = "/html/body/div[6]/div/div/div[3]/div[3]/div[5]/div[3]"


def run_search(driver, query):
    search_bar = None
    # search_bar = driver.find_element(By.NAME, "q")
    search_bar = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/form/div/input')

    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)


def check_for_region_block(driver):
    try:
        region_block = driver.find_element(By.XPATH, REGION_BLOCK_XPATH)
    except NoSuchElementException:
        logging.debug(f'XPath for Region Block not found; moving on...')
        return False
    else:
        return region_block


def expand_languages(driver, xpath_for_more_button):
    try:
        more_languages_button = driver.find_element(By.XPATH, xpath_for_more_button)
    except NoSuchElementException:
        pass
    else:
        more_languages_button.click()


def close_modal(driver):
    close_button = driver.find_element(By.XPATH, CLOSE_BUTTON_XPATH)
    close_button.click()
    time.sleep(2)


def run_app(query, xpath):
    url = "https://unogs.com/"

    driver = webdriver.Firefox()
    driver.get(url)

    run_search(driver, query)

    movie_tags = driver.find_elements(By.CLASS_NAME, "titleitem")
    for movie in movie_tags:
        movie.click()
        time.sleep(2)

        region_block_found = check_for_region_block(driver)
        if region_block_found:
            div_num = 1
            while div_num > 0:
                try:
                    current_xpath = REGION_BLOCK_XPATH + f'/div[{div_num}]'
                    langauge_block = driver.find_element(By.XPATH, current_xpath)
                except NoSuchElementException:
                    div_num = 0
                    pass
                else:
                    subtitle_xpath = current_xpath + f'/div/div[2]/button[1]'
                    expand_languages(driver, subtitle_xpath)
                    dubbed_xpath = current_xpath + f'/div/div[3]/button[1]'
                    expand_languages(driver, dubbed_xpath)
                    # langauge_block = driver.find_element(By.XPATH, current_xpath)
                    div_num = 0
        close_modal(driver)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    run_app("International Velvet", US_XPATH)
