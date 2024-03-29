import sys, os

sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
sys.path.append( os.path.join(os.path.dirname(__file__)) )
from general_utils import get_plot_folder_path

import pandas as pd
from pandas import Series, DataFrame

from matplotlib.pyplot import figure, xticks, savefig, subplots, show

from sklearn.base import RegressorMixin
from ts_functions import PREDICTION_MEASURES, plot_evaluation_results, plot_forecasting_series

from regressor import SimpleAvgRegressor, PersistenceRegressor, RollingMeanRegressor

from statsmodels.tsa.arima.model import ARIMA
from ds_charts import bar_chart


def split_dataframe(data, trn_pct=0.70):
    trn_size = int(len(data) * trn_pct)
    df_cp = data.copy()
    train: DataFrame = df_cp.iloc[:trn_size, :]
    test: DataFrame = df_cp.iloc[trn_size:]
    return train, test


def compare(data, target, index_target, name):

    measure = 'R2'
    flag_pct=False

    eval_results = {}
    regs = ['simple_avg', 'rolling_mean', 'persistence']

    for r in regs:
        train, test, prd_trn, prd_tst = forecast(data, target, index_target, f'{name}', 
            variant=r)

        eval_results[r] = PREDICTION_MEASURES[measure](test.values, prd_tst)

    figure()
    bar_chart(list(eval_results.keys()), list(eval_results.values()), title = 'Basic Regressors Comparison', xlabel= 'Regressor', ylabel=measure, percentage=flag_pct, rotation = False)
    
    savefig( os.path.join(get_plot_folder_path(), f'{name}_basic_reg' ) )


# Select regressor from [simple_avg, persistence, rolling_mean]
def forecast(data, target, index_target, name, variant='simple_avg', measure='R2', flag_pct=False, win=3):

    train, test = split_dataframe(data, trn_pct=0.75)

    if variant == 'simple_avg':
        fr_mod = SimpleAvgRegressor()
    elif variant == 'rolling_mean':
        fr_mod = RollingMeanRegressor(win)
    elif variant == 'persistence':
        fr_mod = PersistenceRegressor()
    else: 
        raise Exception("Unknown regressor! Please choose from: [simple_avg, persistence, rolling_mean]")

    fr_mod.fit(train)
    prd_trn = fr_mod.predict(train)
    prd_tst = fr_mod.predict(test)

    return train, test, prd_trn, prd_tst


def plot_forecasting(train, test, prd_trn, prd_tst, target, index_target, name):

    plot_evaluation_results(train.values, prd_trn, test.values, prd_tst, 
        f'{name}_forecast_eval')

    savefig(  os.path.join(get_plot_folder_path(), f'{name}_forecast_eval' ) )

    plot_forecasting_series(train, test, prd_trn, prd_tst, 
        f'{name}_forecast_plot', 
        x_label=index_target, y_label=target)

    savefig( os.path.join(get_plot_folder_path(), f'{name}_forecast_plot' ) )


def calculate_fc_with_plot(data, target, index_target, name, variant='simple_avg', measure='R2', flag_pct=False):
    
    train, test, prd_trn, prd_tst = forecast(data, target, index_target, f'{name}', 
        variant=variant, measure=measure, flag_pct=flag_pct)

    plot_forecasting(
        train, test, prd_trn, prd_tst, target, index_target, f'fc_{name}_{variant}')

