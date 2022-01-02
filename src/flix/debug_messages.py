from colorama import Fore, Back, Style


def print_found():
    print(Fore.GREEN + 'Movie Found!')
    print(Style.RESET_ALL)


def print_missing():
    print_red('Movie Not Found!')


def print_connection_error():
    print_red('Connection Error; Skipping Title')


def print_red(message):
    print(Fore.RED + message)
    print(Style.RESET_ALL)


def print_pickle_exists():
    print(Fore.GREEN + 'Pickle exists, skipping title!')
    print(Style.RESET_ALL)



