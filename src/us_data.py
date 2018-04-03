import numpy as np
import pandas as pd

# source data: http://www.countyhealthrankings.org/rankings/data

def get_data():

    # def socio_econ_data():
    # read in excel file
    xls = pd.ExcelFile('../data/2017CountyHealthRankingsData.xls')
    # select tab with data and create new df
    df = pd.read_excel(xls, 'Ranked Measure Data')
    # save df to csv file
    # df.to_csv('../data/health_rank_2017.csv')
    # get: state, county, adult smoking, adult obesity, uninsured, PCP (doctors) rate, high school graduation, unemployment, income inequality, air pollution,
    df = df.iloc[:, [1,2,27,31,63,68,95,105,116,135]]
    # change column names
    df.columns = ['state', 'county','smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
    # drop first row (previously header)
    df = df.drop([0])
    # reset index and drop the old index as column
    df.reset_index(level=0, drop=True, inplace=True)

    # make county and state columns lowercase
    df.county = df.county.str.lower()
    df.state = df.state.str.lower()

    # make all other columns numerical (this will enable .describe() for each column)
    df_num = df.iloc[:, 2:10].apply(pd.to_numeric)

    # join back up all columns in a way that avoids numeric columns becoming all "NaN"
    dfc = pd.concat([df.state.reset_index(drop=True), df.county.reset_index(drop=True), df_num.reset_index(drop=True)], axis=1)

    # combine for all states selected
    cocanjfl = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'new jersey') | (dfc['state'] == 'florida')]
    cocafl = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'florida')]
    cocanj = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'new jersey') ]
    coca = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') ]

    return coca 
