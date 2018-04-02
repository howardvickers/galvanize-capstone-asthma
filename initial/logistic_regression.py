import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split


def log_regress(data):
    # need to create threshold for binary classification 
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    model.predict(X_test)
    score = model.score(X_test, y_test)
    print(score)

if __name__ == '__main__':
    from combine_data import join_data as data
    data = data()
    log_regress(data)
