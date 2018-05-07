import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from get_feat_imps import get_feat_imps
from data_processing import nice_column_names
from data_processing import show_columns

def get_imps_names():
    _, feat_imps, cols = get_feat_imps()

    col_dict = nice_column_names()
    X_train_dot_columns = cols
    something = [col_dict.get(x, x) for x in X_train_dot_columns]
    imps, names = zip(*sorted(zip(feat_imps, [col_dict.get(x) for x in X_train_dot_columns])))
    return imps, names

def create_feat_imp_chart():
    imps, names = get_imps_names()

    plt.style.use('bmh')
    plt.barh(range(len(names)), imps, align='center')
    plt.yticks(range(len(names)), names)
    plt.xlabel('Relative Importance of Features', fontsize=10)
    plt.ylabel('Features', fontsize=10)
    plt.tight_layout()
    plt.savefig('static/images/feat_imps.png')

if __name__ == '__main__':
    create_feat_imp_chart()
