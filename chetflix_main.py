import os
from pathlib import Path

from src.utils import copy_file

from src.won.run import get_site_data
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
    for path in [home_dir, src_dir, compile_folder]:
        if not path.exists():
            raise FileNotFoundError(f'Cannot locate {path} folder; please ensure directories are properly configured')

    """
    Run WON Gatherer to get nf_dict.json
    
    (If the nf_dict already exists, then allow to skip)
    
    1. Chdir to src/won
    2. Run won/run/get_site_data and return file name
    3. copy won/output/file_name to compile/input/nf_dict.json
    """
    os.chdir(Path(src_dir, 'won'))
    file_path = get_site_data()
    copy_file(file_path, Path(compile_folder, 'nf_dict.json'))

    """
    Run Netflix Nametags to set up the identifiers
    
    1. Chdir to nametags
    2. Run main
    3. Copy output/netflix_nametags.json to unogs/inputs
    4. Copy output/netflix_nametags.json to trends
    5. Copy output/netflix_nametags.json to flix
    6. Copy output/netflix_nametags.json to compile/inputs
    """

    """
    Run UNOGS data
    
    1. Chdir to src/unogs
    2. run unogs_main() and return folder name
    3. copy folder/final_unogs_df.csv to compile/input/final_unogs_df.csv
    """
    os.chdir(Path(src_dir, 'unogs'))
    unogs_output_folder = unogs_main()
    copy_file(Path(unogs_output_folder, 'final_unogs_df.csv'), Path(compile_folder, 'final_unogs_df.csv'))

    """
    Run Google Trends
    
    1. Chdir to src/trends
    2. Run trends_main() and return output dir
    3. Copy output_dur/trends_data_output to compile/input/google_trends_data.csv
    """
    os.chdir(Path(src_dir, 'trends'))

    """
    Run FlixPatrol Data
    
    1. Chdir to src/flix
    2. Run flixpatrol_main
    3. Copy flix/pickle_jar/summary/!!!history_df_results!!!.pickle to compile/input/!!!history_df_results!!!.pickle
    4. Copy flix/pickle_jar/summary/!!!country_df_results!!!.pickle to compile/input/!!!country_df_results!!!.pickle
    """

    """
    Run Compile
    
    1. Chdir to src/compile
    2. Run compile_main()
    """
    raise NotImplementedError('Overall Process is not complete! Please run modules individually.')


if __name__ == '__main__':
    chetflix_main()
