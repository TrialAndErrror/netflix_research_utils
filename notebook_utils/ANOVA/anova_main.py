from notebook_utils.ANOVA.anova_models import AnovaAnalysis
import pandas as pd
from pathlib import Path
import os
from src.utils import write_json, save_pickle, load_pickle
from notebook_utils.ANOVA.anova_to_df import main


def anova_main():
    df_path = Path(os.getcwd(), 'input', 'Dataset Excluding Distribution Titles.csv')
    df = pd.read_csv(df_path).rename(columns={'Google Trends Score': 'trends_score'})

    gt_anova_model = 'trends_score ~ Group'
    perform_anova_analysis(df, gt_anova_model, prefix='gt')

    top10_anova_model = 'trends_score ~ Points'
    perform_anova_analysis(df, top10_anova_model, prefix='top10')


def perform_anova_analysis(df, model, prefix):
    """

    :param df:
    :param model:
    :param prefix:
    :return:
    """

    """
    Setup directories
    """
    input_folder = Path(os.getcwd(), 'input')
    input_folder.mkdir(exist_ok=True)

    output_folder = Path(os.getcwd(), 'output')
    output_folder.mkdir(exist_ok=True)

    image_out_path = Path(os.getcwd(), 'images')
    image_out_path.mkdir(exist_ok=True)

    pickle_out_path = Path(os.getcwd(), 'cache')
    pickle_out_path.mkdir(exist_ok=True)

    """
    Get groups
    """
    countries = list(df.Country.unique())
    languages = list(df.Language.unique())

    results_dict = {}
    error_dict = {}
    sig_results = []

    for country_name in countries:
        results_dict[country_name] = {}
        error_dict[country_name] = {}
        for language in languages:
            results, last_df = load_or_run_analysis(model, country_name, df, image_out_path, language,
                                                    pickle_out_path, prefix)
            if not isinstance(results, str):
                results_dict[country_name][language] = results
                sig_results.append({'Country': country_name, 'Language': language})
            else:
                error_dict[country_name][language] = {}
                error_dict[country_name][language]['error'] = results
                error_dict[country_name][language]['dataframe'] = last_df.to_dict('index')

    print(f'Found {len(sig_results)} results.')

    results_out_path = Path(output_folder, f'{prefix}_anova_results.json')
    write_json(results_dict, results_out_path)

    error_out_path = Path(output_folder, f'{prefix}_anova_errors.json')
    write_json(error_dict, error_out_path)

    print(f'File saved as {results_out_path}')

    sig_results_df = pd.DataFrame(columns=['Country', 'Language']).from_records(sig_results)
    sig_results_df.to_csv(Path(output_folder, f'{prefix}_significant_results.csv'))

    processed_path = main(results_dict, prefix)
    print(f'ANOVA Results Processed and saved as {processed_path}')


def load_or_run_analysis(anova_model, country_name, df, image_out_path, language, pickle_out_path, prefix):
    pickle_path = Path(pickle_out_path, f'{prefix}_ANOVA_{language}_{country_name}.pickle')
    current_analysis = AnovaAnalysis(df, country_name, language, anova_model, image_out_path)

    if not pickle_path.exists():
        results = current_analysis.run_analysis()
        save_pickle(results, pickle_path)
    else:
        print(f'{prefix}: Loading {language} in {country_name} from file')
        results = load_pickle(pickle_path)

    return results, current_analysis.dataframe


if __name__ == '__main__':
    anova_main()
