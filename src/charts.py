import numpy as np
import pandas as pd
import os
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression as LR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.neighbors import KNeighborsRegressor as KNR
from sklearn.svm import SVR as SVR
from sklearn.linear_model import ElasticNet as EN
from sklearn.ensemble import GradientBoostingRegressor as GBR
import matplotlib.pyplot as plt

# from modclass import *
# import modclass
from modclass import train_model as tm
from modclass import show_columns

def chart_feature_importances():
    model = tm()
    # fm = modclass.FinalModel()
    # feat_imps = fm._regressor.feature_importances_
    feat_imps = model.feature_importances_
    print('feat_imps from chart function', feat_imps)

    # from data import column_names as cols
    col_dict = { 'air_poll_partic': 'Particulate Air Pollution',
                 'asthma_rate': 'Asthma Rate',
                 'co_mean': 'CO - Pollutant',
                 'county': 'County',
                 'haps_mean': 'HAPS - Pollutant',
                 'high_sch_grad': 'High School Grads',
                 'income_ineq': 'Income Inequality',
                 'lead_mean': 'Lead - Pollutant',
                 'no2_mean': 'NO2 - Pollutant',
                 'nonox_mean': 'NONOxNOy - Pollutant',
                 'obese_adult': 'Obesity (Adult)',
                 'ozo_mean': 'Ozone - Pollutant',
                 'pcp': 'PCP',
                 'pm10_mean': 'PM10 - Pollutant',
                 'pm25_mean': 'PM2.5 Pollutant',
                 'pm25non_mean': 'PM2.5 non FRM Pollutant',
                 'pm25spec_mean': 'PM2.5 Spec - Pollutant',
                 'smoke_adult': 'Smokers (Adult)',
                 'so2_mean': 'SO2 - Pollutant',
                 'state': 'State',
                 'unemployment': 'Unemployment',
                 'uninsured': 'Uninsured Rate',
                 'vocs_mean': 'VOCS - Pollutant'}

    # X_train_dot_columns = ['pm10_mean', 'pm25_mean', 'pm25non_mean',
    #    'pm25spec_mean', 'co_mean', 'so2_mean', 'no2_mean', 'ozo_mean',
    #    'nonox_mean', 'lead_mean', 'haps_mean', 'vocs_mean',
    #    'smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad',
    #    'unemployment', 'income_ineq', 'air_poll_partic']

    X_train_dot_columns = show_columns()

    imps, names = zip(*sorted(zip(feat_imps, [col_dict.get(x, x) for x in X_train_dot_columns])))


    plt.style.use('bmh')
    # plt.style.use('seaborn-deep')
    # plt.style.use('seaborn-dark-palette')
    # plt.style.use('seaborn-dark-palette')
    # fig = plt.figure()
    # plt.axis([0, 0.4, 0, 1])
    plt.barh(range(len(names)), imps, align='center')
    plt.yticks(range(len(names)), names)
    # plt.xticks(range(len(imps)), imps)
    plt.xlabel('Relative Importance of Features', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    # plt.title('Which Factors Drive Asthma Rates?', fontsize=24)
    plt.tight_layout()
    # plt.show()
    plt.savefig('static/images/feat_imps.png')

    # plt.style.use('seaborn-dark-palette')
    # # fig = plt.figure()
    # # plt.axis([0, 0.4, 0, 1])
    # plt.barh(range(len(names)), imps, align='center')
    # plt.yticks(range(len(names)), names)
    # # plt.xticks(range(len(imps)), imps)
    # plt.xlabel('Relative Importance of Features', fontsize=18)
    # plt.ylabel('Features', fontsize=18)
    # plt.title('Which Factors Drive Asthma Rates?', fontsize=20)
    # plt.tight_layout()
    # # plt.show()
    # plt.savefig('static/images/feat_imps.png')



if __name__ == '__main__':
    chart_feature_importances()
