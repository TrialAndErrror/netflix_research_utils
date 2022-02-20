from colorama import Fore, Back, Style
import logging


def print_found():
    print_green('Movie Found!')


def print_missing():
    print_red('Movie Not Found!')


def print_connection_error():
    print_red('Connection Error; Skipping Title')
    logging.error('Connection Error; Skipping Title')


def print_pickle_exists():
    print_green('Pickle exists, skipping title!')


def print_red(message):
    print(Fore.RED + message)
    print(Style.RESET_ALL)


def print_green(message):
    print(Fore.GREEN + message)
    print(Style.RESET_ALL)

