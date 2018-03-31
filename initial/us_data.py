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

def get_data():

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

    cocanj = hi[(hi['state'] == 'colorado') | (hi['state'] == 'california') | (hi['state'] == 'new jersey')]

    return cocanj
