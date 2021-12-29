import logging
from pathlib import Path
import os


"""
Site URL

Not currently used, but helpful for reference.
"""
BASE_URL = "https://www.whats-on-netflix.com/originals/movies/"


"""
File Setup:

This is the directory that the resulting file will be created in.

We check to make sure it exists, and create it if it does not.
"""
OUTPUT_FILE = Path(os.getcwd(), 'output')
os.makedirs(OUTPUT_FILE, exist_ok=True)


"""
Logging Setup, for errors and troubleshooting
"""
logging.basicConfig(
    level=logging.DEBUG,
    filename='won_logs.log',
    format='%(asctime)s %(message)s',
)