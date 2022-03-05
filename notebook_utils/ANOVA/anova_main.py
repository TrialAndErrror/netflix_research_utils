import pickle

from notebook_utils.ANOVA.anova_models import AnovaAnalysis
import pandas as pd
from pathlib import Path
import os


def anova_main():
    input_folder = Path(os.getcwd(), 'input')
    input_folder.mkdir(exist_ok=True)

    output_folder = Path(os.getcwd(), 'output')
    output_folder.mkdir(exist_ok=True)

    image_out_path = Path(os.getcwd(), 'images')
    image_out_path.mkdir(exist_ok=True)

    df_path = Path(os.getcwd(), 'input', 'final_short_dataset.csv')
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
            current_analysis = AnovaAnalysis(df, country_name, language, anova_model, image_out_path)

            results = current_analysis.run_analysis()
            if results:
                results_dict[country_name][language] = results
                if not isinstance(results, str):
                    sig_results.append({'Country': country_name, 'Language': language})
                    results_counter += 1

    print(f'Found {results_counter} results.')

    out_path = Path(output_folder, 'results.pickle')
    with open(out_path, 'w+b') as file:
        pickle.dump(results_dict, file)

    print(f'File saved as {out_path}')

    sig_results_df = pd.DataFrame(columns=['Country', 'Language']).from_records(sig_results)
    sig_results_df.to_csv(Path(output_folder, 'significant_results.csv'))


if __name__ == '__main__':
    anova_main()
