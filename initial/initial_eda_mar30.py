import numpy as np
import pandas as pd
import statsmodels.api as sm


# def combine_tables():
join_coca = pd.concat([asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_co,
    asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_ca])
join_coca = join_coca.reset_index()
join_coca = join_coca.drop(['index'], axis=1)

# def lr():
join_nazero_coca = join_coca.fillna(0)
no_counties = join_nazero_coca.drop('county', axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y.values, X.values)
res = model.fit()
print(res.summary())


join_naavg_coca = join_coca.fillna(0)
no_counties = join_naavg_coca.drop('county', axis=1)
X = no_counties.drop('asthma_rate', axis=1)
y = no_counties.asthma_rate
X = sm.add_constant(X)
model = sm.OLS(y.values, X.values)
res = model.fit()
print(res.summary())
