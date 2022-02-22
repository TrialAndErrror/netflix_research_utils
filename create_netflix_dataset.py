import os
from pathlib import Path

from src.utils import copy_file

from src.won.run import get_site_data
from src.nametags.main import nametag_main
from src.unogs.unogs_main import unogs_main
from src.trends.trends_main import trends_main
from src.flix.flix_main import flixpatrol_main
from src.compile.compile_main import compile_main


def chetflix_main():
    """
    Run all Netflix Processing functions

    :return: None
    """
    home_dir = Path(os.getcwd())
    src_dir = Path(home_dir, 'src')
    compile_folder = Path(src_dir, 'compile', 'inputs')
    nametag_folder = Path(src_dir, 'nametags')

    for path in [home_dir, src_dir, compile_folder, nametag_folder]:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    """
    Run WON Gatherer to get nf_dict.json

    (If the nf_dict already exists, then allow to skip)

    1. Chdir to src/won
    2. Run won/run/get_site_data and return file name
    3. copy won/output/file_name to compile/input/nf_dict.json
    """
    won_folder = Path(src_dir, 'won')
    nf_data_outfile = Path(won_folder, 'output', 'nf_dict.json')
    if nf_data_outfile.exists():
        print('Skipping What\'s On Netflix function because nf_dict.json already exists.')
    else:
        os.chdir(won_folder)
        get_site_data()
    copy_file(nf_data_outfile, Path(nametag_folder, 'inputs', 'nf_dict.json'))

    """
    Run Netflix Nametags to set up the identifiers

    1. Chdir to nametags
    2. Run main
    3. Copy output/netflix_nametags.json to unogs/inputs
    4. Copy output/netflix_nametags.json to trends
    5. Copy output/netflix_nametags.json to flix
    6. Copy output/netflix_nametags.json to compile/inputs
    """
    os.chdir(nametag_folder)
    nametag_main()

    nametags_file = Path(src_dir, 'nametags', 'output', 'netflix_nametags.json')
    copy_file(nametags_file, Path(src_dir, 'unogs', 'inputs', 'netflix_nametags.json'))
    copy_file(nametags_file, Path(src_dir, 'trends', 'netflix_nametags.json'))
    copy_file(nametags_file, Path(src_dir, 'flix', 'netflix_nametags.json'))
    copy_file(nametags_file, Path(src_dir, 'compile', 'inputs', 'netflix_nametags.json'))

    """
    Run UNOGS data

    1. Chdir to src/unogs
    2. run unogs_main() and return folder name
    3. copy folder/final_unogs_df.csv to compile/input/final_unogs_df.csv
    """
    unogs_folder = Path(src_dir, 'unogs')

    os.chdir(unogs_folder)
    unogs_output_folder = unogs_main()
    copy_file(Path(unogs_output_folder, 'final_unogs_df.csv'), Path(compile_folder, 'final_unogs_df.csv'))

    """
    Run Google Trends

    1. Chdir to src/trends
    2. Run trends_main() and return output dir
    3. Copy output_dir/trends_data_output to compile/input/google_trends_data.csv
    """
    trends_folder = Path(src_dir, 'trends')

    os.chdir(trends_folder)
    trends_file_path = trends_main()
    copy_file(trends_file_path, Path(compile_folder, 'google_trends_data.csv'))

    """
    Run FlixPatrol Data

    1. Chdir to src/flix
    2. Run flixpatrol_main
    3. Copy flix/summary/history_results.json to compile/input/history_results.json
    4. Copy flix/summary/country_results.json to compile/input/country_results.json
    """
    flixpatrol_folder = Path(src_dir, 'flix')

    os.chdir(flixpatrol_folder)
    flixpatrol_main()
    copy_file(Path(flixpatrol_folder, 'summary', 'history_results.json'), Path(compile_folder, 'history_results.json'))
    copy_file(Path(flixpatrol_folder, 'summary', 'country_results.json'), Path(compile_folder, 'country_results.json'))

    """
    Run Compile
    
    1. Chdir to src/compile
    2. Run compile_main()
    """
    os.chdir(Path(src_dir, 'compile'))
    grouped_df_path = compile_main()

    print(f'Saved compiled dataset to {grouped_df_path}')


if __name__ == '__main__':
    chetflix_main()
