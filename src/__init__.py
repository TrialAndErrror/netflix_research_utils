"""
Initial Configuration
"""

import datetime
"""
Testing Variables:

DEBUG and MAX COUNT are global constants used to limit number of movies to download.
Set DEBUG to False to allow it to get all movies in the json_file.
"""

DEBUG = False
MAX_COUNT = 100

"""
Filename Setup:

Filename determines the name of the results file.
Currently set to "results" with a timestamp at the end.
"""

RESULTS_FILENAME = f'results_{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.json'


