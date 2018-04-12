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
    data['co'] = data.state == 'colorado'
    data['fl'] = data.state == 'florida'
    data['nj'] = data.state == 'new jersey'
    data['ca'] = data.state == 'california'
    print(data.shape)
    X_train, X_test, y_train, y_test = split_data(data)
    X_train, y_train = remove_county_state(X_train, y_train)
    model = RFR(    max_features        = 'auto',
                    max_depth           = None,
                    bootstrap           = True,
                    min_samples_leaf    = 5,
                    min_samples_split   = 10,
                    n_estimators        = 10
                                )
    trained_model = model.fit(X_train, y_train)
    return trained_model

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
    pass
