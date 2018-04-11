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

def train_model():
    data = get_data()
    # print(type(data))
    X_train, X_test, y_train, y_test = split_data(data)
    # print(type(X_train))
    # print(X_train.shape)
    X_train, y_train = remove_county_state(X_train, y_train)
    # print(X_train.shape)

    hyperpara_dict = {  LR  : {}, # use defaults only
                        RFR : { 'randomforestregressor__max_features' : ['auto', 'sqrt'],
                                'randomforestregressor__max_depth': [10, 20, 30, 50, 80, 100, None],
                                'randomforestregressor__bootstrap': [True, False],
                                'randomforestregressor__min_samples_leaf': [1, 2, 4, 10],
                                'randomforestregressor__min_samples_split': [2, 5, 10],
                                'randomforestregressor__n_estimators': [100, 200, 500, 1000, 1500, 2000],
                                },
                        GBR : { 'gradientboostingregressor__n_estimators' :     [100, 600, 700, 800],
                                'gradientboostingregressor__max_depth':         [3, 4, 5, 10, 20],
                                'gradientboostingregressor__min_samples_split': [3, 4, 5, 10, 20],
                                'gradientboostingregressor__learning_rate':     [0.01, 0.05, 0.1],
                                'gradientboostingregressor__loss':              ['ls'],
                                },
                        KNR : { 'kneighborsregressor__n_neighbors' : [1, 2, 3, 4, 5, 6, 10],
                                'kneighborsregressor__weights': ['uniform', 'distance'],
                                },
                        SVR : { 'svr__kernel': ['rbf'],
                                'svr__C': [50],
                                'svr__epsilon': [5],
                                },
                        EN : { 'elasticnet__alpha': [1], # equivalent to lambda; alpha=0 means no regularization, ie linear regression
                                'elasticnet__l1_ratio': [0.9], # l1=1 means L1 penalty, ie Lasso (not L2/Ridge)
                                'elasticnet__max_iter': [10000],
                                }
                    }


    models = [RFR]
    # print('models for loop')
    for model in models:
        # print('this is the model', model)

        # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
        pipeline = make_pipeline(   StandardScaler(),
                                    model()
                                 )

        hyperparameters = hyperpara_dict[model]

        clf = GridSearchCV(pipeline, hyperparameters, cv=3) # cv=3 is same as cv=None (default)
        # print('past clf GridSearchCV')
        # print(X_train)
        # print(y_train)
        trained_model = clf.fit(X_train, y_train)
        # print('trained model passed ')

        # evaluate models with test data
        # pred = clf.predict(X_test)


    # model = RFR(    max_features        = 'sqrt',
    #                 max_depth           = 100,
    #                 bootstrap           = False,
    #                 min_samples_leaf    = 1,
    #                 min_samples_split   = 2,
    #                 n_estimators        = 200
    #                             )
    # print('just RFR')
    # # X_train, y_train = standard_scaler(X_train, y_train)
    # trained_model = model.fit(X_train, y_train)

    return trained_model

# def standard_scaler(X, y):
#     # standardize with StandardScaler
#     # scaler_X = StandardScaler().fit(X.values)
#     # scaler_y = StandardScaler().fit(y.values)
#     # X_scaled = scaler_X.transform(X.values)
#     # y_scaled = scaler_y.transform(y.values.reshape(1,-1))
#
#     X_scaled = X.sub(X.mean())/X.get_values().std()
#     y_scaled = y.sub(y.mean())/y.get_values().std()
#
#     return X_scaled, y_scaled


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
        # from combine_data import join_data as data
        from data import join_data as data
        data, labels = data()
        data.to_csv(csv_file_path, index=False)
    # from data import join_data as data
    # data = data()
    # data.to_csv(csv_file_path, index=False)
    return data

def clean_data(data):
    # drop problematic row with zero for asthma_rate
    data = data.drop([141, 142, 149, 153, 158])
    # replacing nans with zeros
    data_nas = data.fillna(0)
    # print('clean_data')
    # print(type(data_nas))
    return data_nas

def X_y(data_nas):
    # create X and y datasets
    X = data_nas.drop('asthma_rate', axis=1)
    y = data_nas.asthma_rate
    # print('X_y')
    # print(type(X))
    # print(type(y))
    return X, y

def county_data(county):
    data = get_data()
    data_nas = clean_data(data)
    single_county = data_nas[data_nas['county'] == county]
    X, y = X_y(single_county)

    # note that X now includes county and state
    return X, y

def split_data(data):
    cln_data = clean_data(data)
    X, y = X_y(cln_data)
    # standard_scaler(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    # note that X_train, X_test, y_train and y_test all now include county and state
    return X_train, X_test, y_train, y_test

def remove_county_state(X, y):
    X = X.drop(['county', 'state'], axis=1)
    return X, y

# class FinalModel(object):
#     def __init__(self):
#         self._scaler = SS()
#         self._regressor = RFR(  max_features        = 'sqrt',
#                                 max_depth           = 100,
#                                 bootstrap           = False,
#                                 min_samples_leaf    = 1,
#                                 min_samples_split   = 2,
#                                 n_estimators        = 200
#                                 )
#
#     def fit(self, X, y):
#         X, y = remove_county_state(X, y)
#
#         # standardize with StandardScaler
#         scaler_X = _scaler.fit(X)
#         scaler_y = _scaler.fit(y)
#         X_scaled = scaler_X.transform(X)
#         y_scaled = scaler_y.transform(y)

    #     # fit model
    #     self._regressor.fit(X_scaled, y_scaled)
    #
    #     return self
    #
    # def predict(self, X):
    #     return self._regressor.predict(X)


if __name__ == '__main__':
    # train_model()
    #
    # fm = FinalModel()
    # X_train, X_test, y_train, y_test = split_data(data)
    # fm.fit(X_train, y_train)
    # fm.predict(X_test)
    # fm.feat_imps = fm._regressor.feature_importances_
