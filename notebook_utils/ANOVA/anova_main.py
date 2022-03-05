import pickle

from notebook_utils.ANOVA.anova_models import AnovaAnalysis
import pandas as pd
from pathlib import Path
import os
from src.utils import write_json, save_pickle, load_pickle

def anova_main():
    input_folder = Path(os.getcwd(), 'input')
    input_folder.mkdir(exist_ok=True)

    output_folder = Path(os.getcwd(), 'output')
    output_folder.mkdir(exist_ok=True)

    image_out_path = Path(os.getcwd(), 'images')
    image_out_path.mkdir(exist_ok=True)

    pickle_out_path = Path(os.getcwd(), 'cache')
    pickle_out_path.mkdir(exist_ok=True)

    df_path = Path(os.getcwd(), 'input', 'Dataset Excluding Distribution Titles.csv')
    df = pd.read_csv(df_path).rename(columns={'Google Trends Score': 'trends_score'})

    countries = list(df.Country.unique())
    languages = list(df.Language.unique())

    anova_model = 'trends_score ~ Group + Language'

    results_dict = {}
    results_counter = 0
    sig_results = []

    for country_name in countries:
        results_dict[country_name] = {}
        for language in languages:
            results, last_df = load_or_run_analysis(anova_model, country_name, df, image_out_path, language, pickle_out_path)

            if not isinstance(results, str):
                results_dict[country_name][language] = results
                sig_results.append({'Country': country_name, 'Language': language})
                results_counter += 1
            else:
                results_dict[country_name]['error'] = results
                results_dict[country_name]['dataframe'] = last_df.to_dict('index')
                break

    print(f'Found {results_counter} results.')

    out_path = Path(output_folder, 'anova_results.json')
    write_json(results_dict, out_path)

    print(f'File saved as {out_path}')

    sig_results_df = pd.DataFrame(columns=['Country', 'Language']).from_records(sig_results)
    sig_results_df.to_csv(Path(output_folder, 'significant_results.csv'))


def load_or_run_analysis(anova_model, country_name, df, image_out_path, language, pickle_out_path):
    pickle_path = Path(pickle_out_path, f'ANOVA_{language}_{country_name}.pickle')
    current_analysis = AnovaAnalysis(df, country_name, language, anova_model, image_out_path)

    if not pickle_path.exists():
        results = current_analysis.run_analysis()
        save_pickle(results, pickle_path)
    else:
        print(f'Loading {language} in {country_name} from file')
        results = load_pickle(pickle_path)

    return results, current_analysis.dataframe


if __name__ == '__main__':
    anova_main()
