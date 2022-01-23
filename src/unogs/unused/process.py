from src.unogs.process_results import process_subs_and_dubs, read_file
from pathlib import Path
from src import OUTPUT_FOLDER

if __name__ == '__main__':
    test_file = 'results_12-04-2021_09-47-40.json'
    file_path = Path(OUTPUT_FOLDER, test_file)
    data = read_file(file_path)

    process_subs_and_dubs(data)
