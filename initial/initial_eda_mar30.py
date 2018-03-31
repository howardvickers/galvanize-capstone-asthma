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




# def lr():




# replacing nans with zero gives r2 of 0.615
socio_pol_nazero_coca = socio_pollute.fillna(0)
no_counties = socio_pol_nazero_coca.drop(['county', 'state'], axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y, X)
res = model.fit()
print(res.summary())



# dropna gives r2 of ... didn't work because no data left after dropping nans!
join_coca_drop = join_coca.drop(['so_mean', 'no_mean'], axis=1)
join_nadrop_coca = join_coca_drop.dropna()
no_counties = join_nadrop_coca.drop('county', axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y.values, X.values)
res = model.fit()
print(res.summary())

# replacing nans with zero gives r2 of 0.478
join_nazero_coca = join_coca.fillna(0)
no_counties = join_nazero_coca.drop('county', axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y, X)
res = model.fit()
print(res.summary())

# replacing nans with zero gives r2 of 0.464
join_nazero_coca = join_coca.fillna(0)
no_counties = join_nazero_coca.drop('county', axis=1)
X = no_counties.drop(['asthma_rate', 'co_mean', 'so_mean',
       'vocs_mean', 'haps_mean', 'lead_mean', 'pm10_mean',
       'pm2_5non_mean', 'pm2_5spec_mean'], axis=1)

y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y,X)
res = model.fit()
print(res.summary())


# replacing nans with zero gives r2 of 0.476
join_nazero_coca = join_coca.fillna(0)
no_counties = join_nazero_coca.drop('county', axis=1)
X = no_counties.drop(['asthma_rate', 'co_mean', 'so_mean',
       'vocs_mean', 'lead_mean',
       'pm2_5non_mean', 'pm2_5spec_mean'], axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y.values, X.values)
res = model.fit()
print(res.summary())

# replacing nans with averages gives r2 of 0.071
join_naavg_coca = join_coca.fillna(join_coca.mean())
join_naavg_coca = join_naavg_coca.fillna(0)
no_counties = join_naavg_coca.drop('county', axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y.values, X.values)
res = model.fit()
print(res.summary())
