import sys, os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '..','utils') )

from numpy import ndarray
from pandas import DataFrame, read_csv, unique
from matplotlib.pyplot import figure, subplots, savefig, show
from sklearn.ensemble import GradientBoostingClassifier
from ds_charts import plot_evaluation_results, multiple_line_chart, horizontal_bar_chart, HEIGHT
from sklearn.metrics import accuracy_score

from numpy import std, argsort

from ds_charts import plot_overfitting_study

from ds_charts_extensions import plot_evaluation_results_multi_label

from load_data import read_data_by_filename
from general_utils import get_plot_folder_path

from sklearn.model_selection import train_test_split

def gb(X, target, file_tag):

    y: ndarray = X.pop(target).values
    trnX, tstX, trnY, tstY = train_test_split(X, y, test_size=0.2, random_state=0)

    labels = unique(trnY)
    labels.sort()

    n_estimators = [5, 10, 25, 50, 75, 100, 200, 300, 400]
    max_depths = [5, 10, 25]
    learning_rate = [.1, .5, .9]
    best = ('', 0, 0)
    last_best = 0
    best_model = None

    cols = len(max_depths)
    figure()
    fig, axs = subplots(1, cols, figsize=(cols*HEIGHT, HEIGHT), squeeze=False)
    for k in range(len(max_depths)):
        d = max_depths[k]
        values = {}
        for lr in learning_rate:
            yvalues = []
            for n in n_estimators:
                print(f'Depth: {k} with LR {lr} and estimators {n}')
                gb = GradientBoostingClassifier(n_estimators=n, max_depth=d, learning_rate=lr)
                gb.fit(trnX, trnY)
                prdY = gb.predict(tstX)
                yvalues.append(accuracy_score(tstY, prdY))
                if yvalues[-1] > last_best:
                    best = (d, lr, n)
                    last_best = yvalues[-1]
                    best_model = gb
            values[lr] = yvalues
        multiple_line_chart(n_estimators, values, ax=axs[0, k], title=f'Gradient Boorsting with max_depth={d}',
                            xlabel='nr estimators', ylabel='accuracy', percentage=True)

    savefig( os.path.join(get_plot_folder_path(), f'{file_tag}_gb_study' ) )

    print('Best results with depth=%d, learning rate=%1.2f and %d estimators, with accuracy=%1.2f'%(best[0], best[1], best[2], last_best))

    prd_trn = best_model.predict(trnX)
    prd_tst = best_model.predict(tstX)
    
    if len(labels) > 2:
        plot_evaluation_results_multi_label(labels, trnY, prd_trn, tstY, prd_tst)
    else:
        plot_evaluation_results(labels, trnY, prd_trn, tstY, prd_tst)
    savefig( os.path.join(get_plot_folder_path(), f'{file_tag}_gb_best' ) )

    variables = X.columns
    importances = best_model.feature_importances_
    indices = argsort(importances)[::-1]
    stdevs = std([tree[0].feature_importances_ for tree in best_model.estimators_], axis=0)
    elems = []
    for f in range(len(variables)):
        elems += [variables[indices[f]]]
        print(f'{f+1}. feature {elems[f]} ({importances[indices[f]]})')

    figure()
    horizontal_bar_chart(elems, importances[indices], stdevs[indices], title='Gradient Boosting Features importance', xlabel='importance', ylabel='variables')
    savefig( os.path.join(get_plot_folder_path(), f'{file_tag}_gb_ranking' ) )

    lr = 0.7
    max_depth = 10
    eval_metric = accuracy_score
    y_tst_values = []
    y_trn_values = []
    for n in n_estimators:
        print(f'Overfitting: Depth: {max_depth} with LR {lr} and estimators {n}')
        gb = GradientBoostingClassifier(n_estimators=n, max_depth=d, learning_rate=lr)
        gb.fit(trnX, trnY)
        prd_tst_Y = gb.predict(tstX)
        prd_trn_Y = gb.predict(trnX)
        y_tst_values.append(eval_metric(tstY, prd_tst_Y))
        y_trn_values.append(eval_metric(trnY, prd_trn_Y))

    plot_overfitting_study(n_estimators, y_trn_values, y_tst_values, name=f'GB_depth={max_depth}_lr={lr}', xlabel='nr_estimators', ylabel=str(eval_metric))
    savefig( os.path.join(get_plot_folder_path(), f'{file_tag}_overfitting_study' ) )


def main():
    drought_data = read_data_by_filename('drought_dataset_undersampled.csv')
    diabetic_data = read_data_by_filename('diabetic_dataset_oversampled.csv')

    gb(drought_data, 'drought', 'drought')
    gb(diabetic_data, 'readmitted', 'diabetic')

if __name__ == '__main__':
    main()