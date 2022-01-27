import warnings

import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from bioinfokit.analys import stat
from statsmodels.formula.api import ols

warnings.filterwarnings('ignore')
pd.set_option('display.expand_frame_repr', False)

ANOVA_MODEL = 'search_interest ~ group'


def perform_one_way_anova(dataframe):
    global ANOVA_MODEL
    model = ols(ANOVA_MODEL, data=dataframe).fit()
    return sm.stats.anova_lm(model, typ=2)


def run_tukey_test(res, dataframe, column_name):
    res.tukey_hsd(df=dataframe, res_var='search_interest', xfac_var=column_name, anova_model=ANOVA_MODEL)
    return res.tukey_summary, res.tukey_hsd(df=dataframe, res_var='search_interest', xfac_var=column_name,
                                            anova_model=ANOVA_MODEL)


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
    def __init__(self, df_csv, country, anova_model=ANOVA_MODEL):
        self.res = stat()
        self.dataframe: pd.DataFrame = self.load_and_process_df(df_csv)
        self.dataframe = self.dataframe[self.dataframe.country == country]
        try:
            self.name = self.dataframe.iloc[1].group_language
        except IndexError:
            print('Error: No results found. Cannot run analysis.')
            self.name = 'Unnamed Analysis'
        else:
            self.anova_model = anova_model
            self.country = country

    def load_and_process_df(self, csv_path):
        df = pd.read_csv(csv_path)
        return df[df['group_value'] == True].drop('Unnamed: 0', axis=1).drop('group_value', axis=1)[
            ['title', 'country', 'available', 'original_language', 'group', 'group_language', 'search_interest']]

    def run_analysis(self):
        if self.name != 'Unnamed Analysis':
            print(f'Running Analysis: {self.name} in {self.country}\n\n')
            anova_df = self.perform_one_way_anova()

            print(anova_df)
            dfi.export(anova_df, f'ANOVA_{self.name}_{self.country}.png')
            if anova_df.iloc[0]['PR(>F)'] < .05:
                tukey_test, tukey_obj = self.run_tukey_test('group')
                print(tukey_test)
                dfi.export(tukey_test, f'TUKEY_{self.name}_{self.country}.png')
                shapiro = self.test_shapiro_wilk()
                print(shapiro)
            else:
                print('\nNot significant, skipping tukey test')
        else:
            print('\n\nError loading data; skipping analysis\n\n')

    def perform_one_way_anova(self):
        print(f'One-Way ANOVA: {self.name}')
        return perform_one_way_anova(self.dataframe)

    def make_qq_plot(self):
        return make_qq_plot(self.res, self.name)

    def make_qq_hist(self):
        return make_qq_hist(self.res, self.name)

    def test_shapiro_wilk(self):
        print(f'\n\nShapiro-Wilk Test: {self.name}')
        w, pvalue = stats.shapiro(self.res.anova_model_out.resid)
        return (f'W: {w}; P-Value: {pvalue}')

    def run_tukey_test(self, column_name):
        print(f'\n\nTukey Test: {self.name} [{column_name}]')
        return run_tukey_test(self.res, self.dataframe, column_name)
