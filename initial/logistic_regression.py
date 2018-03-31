import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# source data: http://www.countyhealthrankings.org/rankings/data

from combine_data import join_data as data

# def logreg():

socio_pol_nazero_coca = data.fillna(0)
no_counties = socio_pol_nazero_coca.drop(['county', 'state'], axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
# X = sm.add_constant(X)
model = LogisticRegression()
model.fit(X_train, y_train)
model.predict(X_test)
score = model.score(X_test, y_test)
print(score)
