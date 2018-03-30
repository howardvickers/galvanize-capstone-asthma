import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# source data: http://www.countyhealthrankings.org/rankings/data/CO

# read in excel file
xls = pd.ExcelFile('../data/colorado_health_rankings_county_2017.xls')
# select tab with data and create new df
df1 = pd.read_excel(xls, 'Ranked Measure Data')
# save df to csv file
df1.to_csv('../data/co_health_rank_2017.csv')


# get: adult smoking, adult obesity, uninsured, PCP (doctors) rate, high school graduation, unemployment, income inequality, air pollution,
df1_multicols = df1.iloc[:, [24,28,60,65,98,108,119,138]]
# change column names
new_names = ['smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
df1_multicols.columns = new_names


# remove multi-indexes (first)
df1_multicols.reset_index(level=0, drop=True, inplace=True)
# repeat multi-indexes (second)
df1_multicols.reset_index(level=0, drop=True, inplace=True)
# drop the index
df1_multicols.drop(df1_multicols.index[[0]], inplace=True)

# move index (counties) to own column
df1_multicols = df1_multicols.reset_index()
# change name of counties column from index to county
df1_multicols.columns = ['county', 'smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
# make all county names lowercase
df1_multicols.county = df1_multicols.county.str.lower()
# remove top line (probably average for state/all-counties)
df1_multicols = df1_multicols.loc[1:,:]

nine_asthma = pd.merge(asthma, df1_multicols, how="outer", on="county")

scasthma = nine_asthma[['asthma_rate', 'smoke_adult', 'obese_adult', 'uninsured',
       'pcp', 'high_sch_grad', 'unemployment', 'income_ineq',
       'air_poll_partic']].astype(float)

scatter_matrix(scasthma, figsize=(8,8), diagonal='kde')


 
    def bootstrapping():
        pass
        # for i in range(0, 500):
        #     sample_index = np.random.choice(range(0, len(y)), len(y))
        #
        #     X_samples = X[sample_index]
        #     y_samples = y[sample_index]
        #
        #     lr = LinearRegression()
        #     lr.fit(X_samples, y_samples)
        #     plt.plot(x, lr.predict(X), color='grey', alpha=0.2, zorder=1)
        # https://stats.stackexchange.com/questions/183230/bootstrapping-confidence-interval-from-a-regression-prediction
