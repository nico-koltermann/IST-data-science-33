import sys, os

sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
sys.path.append( os.path.join(os.path.dirname(__file__)) )

from matplotlib.pyplot import subplots, show, savefig
from ds_charts import multiple_line_chart
from ts_functions import HEIGHT, PREDICTION_MEASURES, plot_evaluation_results, plot_forecasting_series

from statsmodels.tsa.arima.model import ARIMA
from pandas import DataFrame

def find_arima_parameter(
    train: DataFrame, 
    test: DataFrame, 
    index: str,
    target: str,
    freq:str,
    file_tag: str):

    measure = 'R2'
    flag_pct = False
    last_best = -100
    best = ('',  0, 0.0)
    best_model = None

    d_values = (0, 1, 2)
    params = (1, 2, 3, 5)
    ncols = len(d_values)

    fig, axs = subplots(1, ncols, figsize=(ncols*HEIGHT, HEIGHT), squeeze=False)

    for der in range(len(d_values)):
        d = d_values[der]
        values = {}
        for q in params:
            yvalues = []
            for p in params:
                pred = ARIMA(train, order=(p, d, q))
                model = pred.fit(method_kwargs={'warn_convergence': False})
                prd_tst = model.forecast(steps=len(test), signal_only=False)
                yvalues.append(PREDICTION_MEASURES[measure](test,prd_tst))
                if yvalues[-1] > last_best:
                    best = (p, d, q)
                    last_best = yvalues[-1]
                    best_model = model
            values[q] = yvalues
        multiple_line_chart(
            params, values, ax=axs[0, der], title=f'ARIMA d={d}', xlabel='p', ylabel=measure, percentage=flag_pct)

    savefig(f'{file_tag}_ts_arima_study.png')

    print(f'Best results achieved with (p,d,q)=({best[0]}, {best[1]}, {best[2]}) ==> measure={last_best:.2f}')
    
    return (best[0],best[1],best[2])

def arima_forecast(
    train: DataFrame, 
    index: str,
    target: str,
    freq:str,
    order: tuple,
    file_tag: str):

    pred = ARIMA(train, order=order)
    model = pred.fit(method_kwargs={'warn_convergence': False})
    model.plot_diagnostics(figsize=(2*HEIGHT, 2*HEIGHT))

    show()

