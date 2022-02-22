import os
from pathlib import Path


def get_output_folder():
    output_folder = Path(os.getcwd(), 'output')
    output_folder.mkdir(exist_ok=True)
    return output_folder


def get_input_folder():
    input_folder = Path(os.getcwd(), 'inputs')
    input_folder.mkdir(exist_ok=True)
    return input_folder
