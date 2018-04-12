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
    errors_for_plot = ypred - y_test
    print('errors_for_plot', list(errors_for_plot))

    print('Model Performance Indicators')
    print('MAE: {:0.3f}'.format(mae))
    print('MAPE: {:0.3f}'.format(mape))
    print('Accuracy = {:0.3f}%'.format(accuracy))

    print('RMSE (test):', rmse_test)
    print('RMSE (train):', rmse_train)
    if rmse_test > rmse_train:
        print('Overfit')
    else:
        print('Underfit')
    return accuracy, rmse_train, rmse_test, errors_for_plot


def train_model():
    data = get_data()
    X_train, X_test, y_train, y_test = split_data(data)
    X_train, y_train = remove_county_state(X_train, y_train)
    X_test, y_test = remove_county_state(X_test, y_test)

    print('y_train', list(y_train))
    print('y_test', list(y_test))
    print('all y', list(y_train)+list(y_test))

    # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
    pipeline = make_pipeline(StandardScaler(),
                             RFR())

    # set hyperparameters
    hyperparameters = {
                        # 'randomforestregressor__max_features' : ['auto', 'sqrt'],
                        # 'randomforestregressor__max_depth': [3, 5, None],
                        # 'randomforestregressor__bootstrap': [True, False],
                        # 'randomforestregressor__min_samples_leaf': [3, 5, 7],
                        # 'randomforestregressor__min_samples_split': [5, 10, 15],
                        # 'randomforestregressor__n_estimators': [5, 8, 10, 15],

                        # 'randomforestregressor__max_features' : ['sqrt'],
                        # 'randomforestregressor__max_depth': [100],
                        # 'randomforestregressor__bootstrap': [ False],
                        # 'randomforestregressor__min_samples_leaf': [1],
                        # 'randomforestregressor__min_samples_split': [2],
                        # 'randomforestregressor__n_estimators': [200],

                        #
                        # 'randomforestregressor__max_leaf_nodes': [None],
                        # 'randomforestregressor__min_impurity_decrease': [0.0],
                        # 'randomforestregressor__min_impurity_split':[None],
                        # 'randomforestregressor__min_weight_fraction_leaf':[0.0],

                        'randomforestregressor__max_features': ['auto'],
                        'randomforestregressor__max_depth': [None],
                        'randomforestregressor__bootstrap': [True],
                        'randomforestregressor__min_samples_leaf': [5],
                        'randomforestregressor__min_samples_split': [10],
                        'randomforestregressor__n_estimators':[10],

                        # 'randomforestregressor__max_features': ['auto'],
                        # 'randomforestregressor__max_depth': [None],
                        # 'randomforestregressor__bootstrap': [True],
                        # 'randomforestregressor__min_samples_leaf': [5],
                        # 'randomforestregressor__min_samples_split': [10],
                        # 'randomforestregressor__n_estimators':[10, 30, 50, 70, 100],
                        }




    # tune model via pipeline
    clf = GridSearchCV(pipeline, hyperparameters, cv=3)

    clf.fit(X_train, y_train)

    pred = clf.predict(X_test)
    # print('feature importances:', clf.feature_importances_)
    print ('r2 score:',r2_score(y_test, pred))
    print ('mse:',mean_squared_error(y_test, pred))
    print('*'*20)
    print('best params:',clf.best_params_)
    print('best grid:', clf.best_estimator_)
    print('^'*20)
    eval_model(clf.best_estimator_, X_train, y_train, X_test, y_test)
    print('#'*20)
    print('score', clf.score)
    return clf

def show_columns():
    data = get_data()
    X_train, X_test, y_train, y_test = split_data(data)
    X_train, y_train = remove_county_state(X_train, y_train)
    return X_train.columns


def get_data():
    csv_file_path = '../data/the_data_file.csv'

    if os.path.exists(csv_file_path):
        print("Data file found, loading data...")
        with open(csv_file_path, "r") as f:
            data = pd.read_csv(f)

    else:
        print("Data file not found, assembling dataset...")
        from data import join_data as data
        data, labels = data()
        data.to_csv(csv_file_path, index=False)

    return data

def clean_data(data):
    # drop problematic row with zero for asthma_rate
    data = data.drop([141, 142, 149, 153, 158])
    data_nas = data.fillna(0)
    return data_nas

def X_y(data_nas):
    X = data_nas.drop('asthma_rate', axis=1)
    y = data_nas.asthma_rate
    return X, y

def county_data(county):
    data = get_data()
    data_nas = clean_data(data)
    single_county = data_nas[data_nas['county'] == county]
    X, y = X_y(single_county)
    return X, y

def split_data(data):
    cln_data = clean_data(data)
    X, y = X_y(cln_data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    return X_train, X_test, y_train, y_test

def remove_county_state(X, y):
    X = X.drop(['county', 'state'], axis=1)
    return X, y

if __name__ == '__main__':
    train_model()
