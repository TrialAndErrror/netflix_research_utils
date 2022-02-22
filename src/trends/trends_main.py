from pathlib import Path

from src.trends.functions.files import load_netflix_nametags, setup_directories
from src.trends.functions.process import create_date_range_column, process_df_lines


def trends_main():
    print('Starting Google Trends processing...')

    pickle_dir, output_dir = setup_directories()

    print('Loading Netflix Data')
    netflix_titles_df = load_netflix_nametags()

    print('Making Date Range Columns')
    total_df = create_date_range_column(netflix_titles_df)

    print('Fetching Data')
    new_df = process_df_lines(total_df)

    output_file_path = Path(output_dir, 'trends_data_output.csv')
    print(f'Saving Dataframe to {output_file_path}')
    new_df.to_csv(output_file_path)

    return output_file_path


if __name__ == '__main__':
    trends_main()

