import numpy as np
from numpy import ndarray
from ds_charts import plot_confusion_matrix, HEIGHT
from sklearn.metrics import confusion_matrix

from matplotlib.pyplot import Axes, gca, figure, savefig, subplots, imshow, imread, axis

def plot_evaluation_results_multi_label(labels: ndarray, trn_y, prd_trn, tst_y, prd_tst):
    cnf_mtx_trn = confusion_matrix(trn_y, prd_trn, labels=labels)
    fp_trn,fn_trn,tp_trn,tn_trn = cnf_result_multilabel(cnf_mtx_trn)

    cnf_mtx_tst = confusion_matrix(tst_y, prd_tst, labels=labels)
    fp_tst,fn_tst,tp_tst,tn_tst = cnf_result_multilabel(cnf_mtx_tst)

    evaluation = {
        'Accuracy': [(tn_trn + tp_trn) / (tn_trn + tp_trn + fp_trn + fn_trn), (tn_tst + tp_tst) / (tn_tst + tp_tst + fp_tst + fn_tst)],
        'Recall': [tp_trn / (tp_trn + fn_trn), tp_tst / (tp_tst + fn_tst)],
        'Specificity': [tn_trn / (tn_trn + fp_trn), tn_tst / (tn_tst + fp_tst)],
        'Precision': [tp_trn / (tp_trn + fp_trn), tp_tst / (tp_tst + fp_tst)]}

    _, axs = subplots(1, 2, figsize=(2 * HEIGHT, HEIGHT))
    plot_confusion_matrix(cnf_mtx_tst, labels, ax=axs[1], title='Test')

def cnf_result_multilabel(cnf_mtx_trn):
    fp = np.sum(cnf_mtx_trn.sum(axis=0) - np.diag(cnf_mtx_trn)    )
    fn = np.sum(cnf_mtx_trn.sum(axis=1) - np.diag(cnf_mtx_trn)    )
    tp = np.sum(np.diag(cnf_mtx_trn)   )
    tn = np.sum(np.sum(cnf_mtx_trn) - (fp + fn + tp))
    return fp,fn,tp,tn