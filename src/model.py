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




def column_names(X_train):
    column_names = X_train.columns

    nice_labels = ['County', 'Asthma Rate', 'PM10 - Pollutant', 'PM2.5 Pollutant', 'PM2.5 non FRM Pollutant',
       'PM2.5 Spec - Pollutant', 'CO - Pollutant', 'SO2 - Pollutant', 'NO2 - Pollutant', 'Ozone - Pollutant',
       'NONOxNOy - Pollutant', 'Lead - Pollutant', 'HAPS - Pollutant', 'VOCS - Pollutant', 'State',
       'Smokers (Adult)', 'Obesity (Adult)', 'Uninsured Rate', 'PCP', 'High School Grads',
       'Unemployment', 'Income Inequality', 'Particulate Air Pollution']
    label_dict = dict(zip(column_names, nice_labels))

    return label_dict


def calc_rmse(yhat, y):
    return np.sqrt(((yhat-y)**2).mean())

def calc_mae(yhat, y):
    return np.mean(abs(yhat-y))

def calc_mape(yhat, y):
    return 100*np.mean(abs((yhat-y)/y))

def eval_model(model, X_train, y_train, X_test, y_test):
    ypred = model.predict(X_test)
    ytrainpred = model.predict(X_train)

    mae = calc_mae(ypred, y_test)
    mape = calc_mape(ypred, y_test)
    accuracy = 100 - mape

    rmse_test   = calc_rmse(ypred, y_test)
    rmse_train  = calc_rmse(ytrainpred, y_train)

    print('Model Performance Indicators')
    print('Model:', model)
    print('MAE: {:0.3f}'.format(mae))
    print('MAPE: {:0.3f}'.format(mape))
    print('Accuracy = {:0.3f}%'.format(accuracy))

    print('RMSE (test):', rmse_test)
    print('RMSE (train):', rmse_train)
    if rmse_test > rmse_train:
        print('Overfit')
    else:
        print('Underfit')
    return accuracy

def split_data(data):
    # drop problematic row with zero for asthma_rate
    data = data.drop([141, 142, 149, 153, 158])
    # replacing nans with zeros
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate

    # consider replacing nans with mean (previously tried)...
    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    return X_train, X_test, y_train, y_test

def do_model(X_train, X_test, y_train, y_test):

    model = RFR(  max_features        = 'sqrt',
                max_depth           = 100,
                bootstrap           = False,
                min_samples_leaf    = 1,
                min_samples_split   = 2,
                n_estimators        = 200
                )

    model = model.fit(X_train, y_train)

    ypred           = model.predict(X_test)
    ytrainpred      = model.predict(X_train)

    model_params    = model.get_params()
    feat_imps       = model.feature_importances_

    return model, model_params, feat_imps, ypred, ytrainpred

def policy_predict(X_train, X_test, y_train, y_test):
    model, _, _, _, _,  = do_model(X_train, X_test, y_train, y_test)
    policy_result = model.predict()

def chart_feature_importances(X_train, X_test, y_train, y_test):

    _, feat_imps, _, _, _, = do_model(X_train, X_test, y_train, y_test)

    # from data import column_names as cols
    col_dict = column_names(X_train)

    imps, names = zip(*sorted(zip(feat_imps, [col_dict.get(x, x) for x in X_train.columns])))

    plt.style.use('bmh')
    # plt.style.use('seaborn-deep')
    # plt.style.use('seaborn-dark-palette')
    # plt.style.use('seaborn-dark-palette')
    # fig = plt.figure()
    # plt.axis([0, 0.4, 0, 1])
    plt.barh(range(len(names)), imps, align='center')
    plt.yticks(range(len(names)), names)
    # plt.xticks(range(len(imps)), imps)
    plt.xlabel('Relative Importance of Features', fontsize=14)
    plt.ylabel('Features', fontsize=14)
    # plt.title('Which Factors Drive Asthma Rates?', fontsize=24)
    plt.tight_layout()
    # plt.show()
    plt.savefig('static/images/feat_imps2.png')



if __name__ == '__main__':
    csv_file_path = '../data/the_data_file.csv'

    if os.path.exists(csv_file_path):
        print("Data file found, loading data...")
        with open(csv_file_path, "r") as f:
            data = pd.read_csv(f)

    else:
        print("Data file not found, assembling dataset...")
        # from combine_data import join_data as data
        from data import join_data as data
        data, labels = data()
        data.to_csv(csv_file_path, index=False)
    # from data import join_data as data
    # data = data()
    # data.to_csv(csv_file_path, index=False)
    X_train, X_test, y_train, y_test = split_data(data)

    do_model(X_train, X_test, y_train, y_test)
    chart_feature_importances(X_train, X_test, y_train, y_test)
