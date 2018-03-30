import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# source data: http://www.countyhealthrankings.org/rankings/data



# def combine_tables():
join_coca = pd.concat([asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_co,
    asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_ca])
join_coca = join_coca.reset_index()
join_coca = join_coca.drop(['index'], axis=1)



# def socio_econ_data():
# read in excel file
xls = pd.ExcelFile('../data/2017CountyHealthRankingsData.xls')
# select tab with data and create new df
df1 = pd.read_excel(xls, 'Ranked Measure Data')
# save df to csv file
df1.to_csv('../data/health_rank_2017.csv')
# get: state, county, adult smoking, adult obesity, uninsured, PCP (doctors) rate, high school graduation, unemployment, income inequality, air pollution,
hi = df1.iloc[:, [1,2,27,31,63,68,95,105,116,135]]
# change column names
hi.columns = ['state', 'county','smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
hi.reset_index(level=0, drop=True, inplace=True)
hi.reset_index(level=0, drop=True, inplace=True)
hi.county = hi.county.str.lower()
hi.state = hi.state.str.lower()

coca = hi[(hi['state'] == 'colorado') | (hi['state'] == 'california')]

socio_pollute = coca.merge(join_coca, how="left", on="county")




# def lr():




# replacing nans with zero gives r2 of
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
