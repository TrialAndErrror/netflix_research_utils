import shutil
import warnings

import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from bioinfokit.analys import stat
from statsmodels.formula.api import ols

from pathlib import Path

warnings.filterwarnings('ignore')
pd.set_option('display.expand_frame_repr', False)


def perform_one_way_anova(dataframe, anova_model):
    model = ols(anova_model, data=dataframe).fit()
    return sm.stats.anova_lm(model, typ=2)


def run_tukey_test(res, dataframe, column_name, res_var, anova_model):
    res.tukey_hsd(df=dataframe, res_var=res_var, xfac_var=column_name, anova_model=anova_model)
    return res.tukey_summary, res.tukey_hsd(df=dataframe, res_var=res_var, xfac_var=column_name,
                                            anova_model=anova_model)


def make_qq_plot(res, plot_name):
    sm.qqplot(res.anova_std_residuals, line='45')
    plt.title(f'QQ Plot: {plot_name}')
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Standardized Residuals")
    return plt


def make_qq_hist(res, plot_name):
    plt.hist(res.anova_model_out.resid, bins='auto', histtype='bar', ec='k')
    plt.title(f'QQ Histogram: {plot_name}')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    return plt


def test_shapiro_wilk(res):
    w, pvalue = stats.shapiro(res.anova_model_out.resid)
    return {
        'w': w,
        'p-value': pvalue
    }


class AnovaAnalysis:
    def __init__(self, df: pd.DataFrame, country: str, language: str, anova_model, image_out_path: Path):
        self.res = stat()
        self.dataframe = df[df.Country == country]

        self.anova_model = anova_model
        self.country = country
        self.language = language

        self.image_out_path = image_out_path

    def run_analysis(self):
        print(f'Running Analysis: {self.language} in {self.country}\n\n')
        anova_filename = f'ANOVA_{self.language}_{self.country}.png'
        if not Path(self.image_out_path, anova_filename).exists():

            """
            Perform ANOVA test
            """
            # anova_df = self.perform_one_way_anova()
            try:
                anova_df = self.perform_one_way_anova()
            except ValueError as e:
                message = f'Error when running ANOVA on {self.language} in {self.country}: {e}'
                print(message)
                return message
            else:
                print(anova_df)
                dfi.export(anova_df, anova_filename)
                shutil.move(anova_filename, Path(self.image_out_path, anova_filename))
                if anova_df.iloc[0]['PR(>F)'] < .05:

                    """
                    Run Tukey Test for significant results
                    """
                    tukey_filename = f'TUKEY_{self.language}_{self.country}.png'
                    try:
                        tukey_test, tukey_obj = self.run_tukey_test('Group')
                    except ValueError as e:
                        message = f'Error when running Tukey Test on {self.language} in {self.country}: {e}'
                        print(message)
                        return message
                    else:
                        print(tukey_test)
                        dfi.export(tukey_test, tukey_filename)
                        shutil.move(tukey_filename, Path(self.image_out_path, tukey_filename))

                        """
                        Run Shapiro-Wilks test
                        """

                        shapiro = self.test_shapiro_wilk()
                        print(shapiro)
                        return tukey_test, shapiro
                else:
                    print('\nNot significant, skipping tukey test')
        else:
            print('ANOVA file found, skipping running')

    def perform_one_way_anova(self):
        print(f'One-Way ANOVA: {self.language}')
        return perform_one_way_anova(self.dataframe, self.anova_model)

    def make_qq_plot(self):
        return make_qq_plot(self.res, self.language)

    def make_qq_hist(self):
        return make_qq_hist(self.res, self.language)

    def test_shapiro_wilk(self):
        print(f'\n\nShapiro-Wilk Test: {self.language}')
        w, pvalue = stats.shapiro(self.res.anova_model_out.resid)
        return f'W: {w}; P-Value: {pvalue}'

    def run_tukey_test(self, column_name):
        print(f'\n\nTukey Test: {self.language} [{column_name}]')
        return run_tukey_test(self.res, self.dataframe, column_name, self.anova_model.split(' ~ ')[0], self.anova_model)

