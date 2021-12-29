"""
All XPaths for What's on Netflix
"""

"""
XPaths for Table Data
"""
SEARCH_BAR = '/html/body/div[1]/div/div[2]/div/div/div[1]/div/article/div/div[2]/div/div[2]/label/input'
ENTRY_TABLE = '/html/body/div[1]/div/div[2]/div/div/div[1]/div/article/div/div[2]/div/table/tbody'


def get_row_xpath(num):
    return f'{ENTRY_TABLE}/tr[{num}]'


"""
Individual cells in the entry table.
"""
EXPAND_BUTTON_CELL = '/td[1]'
TITLE_CELL = '/td[3]'
GENRE_CELL = '/td[4]'
RATING_CELL = '/td[5]'
IMDB_CELL = '/td[6]'


def get_title_cell(row_num):
    return f'{ENTRY_TABLE}/tr[{row_num}]{TITLE_CELL}'


def get_netflix_url_cell(row_num):
    return f'{ENTRY_TABLE}/tr[{row_num + 1}]/td/table/tbody/tr[6]/td[2]/a'


"""
XPaths for Table Entries
"""

"""
XPaths for Navigation 
"""
PAGINATE_BAR = '//*[@id="example_paginate"]'
PREVIOUS_BUTTON = '//*[@id="example_previous"]'
NEXT_BUTTON = '//*[@id="example_next"]'