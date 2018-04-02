import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split


def lin_regress(data):
    # replacing nans with zeros
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    res = model.fit()
    print(res.summary())

    # consider replacing nans with mean (previously tried)...


if __name__ == '__main__':
    from combine_data import join_data as data
    data = data()
    lin_regress()
