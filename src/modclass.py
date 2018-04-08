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
    X_train, X_test, y_train, y_test = split_data(data)

    model = RFR(    max_features        = 'sqrt',
                    max_depth           = 100,
                    bootstrap           = False,
                    min_samples_leaf    = 1,
                    min_samples_split   = 2,
                    n_estimators        = 200
                                )
    trained_model = model.fit(X_train, y_train)

    return trained_model

def show_columns():
    data = get_data()
    X_train, X_test, y_train, y_test = split_data(data)
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
    return data_nas

def X_y(data_nas):
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate
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
    # print('split_data - X_train.columns', X_train.columns)
    return X_train, X_test, y_train, y_test


class FinalModel(object):
    def __init__(self):
        # self._vectorizer = TfidfVectorizer(stop_words='english')
        self._regressor = RFR(  max_features        = 'sqrt',
                                max_depth           = 100,
                                bootstrap           = False,
                                min_samples_leaf    = 1,
                                min_samples_split   = 2,
                                n_estimators        = 200
                                )

    def fit(self, X, y):
        # StandardScaler here
        self._regressor.fit(X, y)

        # self.X_vectors = self._vectorizer.fit_transform(X)
        # self._classifier.fit(self.X_vectors, y)
        return self

    def predict(self, X):
        return self._regressor.predict(X)

    # def score(self, X, y):
    #     X_vectors = self._vectorizer.transform(X)
    #     return self._classifier.score(X_vectors, y)

if __name__ == '__main__':
    Boulder_X, Boulder_y[1] = county_data(data, 'boulder')
    print(Boulder_X.shape)
    print(Boulder_y.shape)
    print(type(Boulder_X))
    print(type(Boulder_y))
    train_model()

    fm = FinalModel()
    X_train, X_test, y_train, y_test = split_data(data)
    fm.fit(X_train, y_train)
    fm.predict(X_test)
    fm.feat_imps = fm._regressor.feature_importances_
    # pg.score(X_test, y_test)
    print('Feature Importances: ', fm._regressor.feature_importances_)
