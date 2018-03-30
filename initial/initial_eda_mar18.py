import numpy as np
import pandas as pd
from dbfread import DBF
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# source data:

class OilEDA(object):
    def __init__(self):
        self.df = None

    def oil_data(self):
        dbf = DBF('../data/oil_gas_locations/oil_mar27.dbf')
        df = pd.DataFrame(iter(dbf))

        dfmin = df[['loc_id', 'fac_status', 'county']]

        # filter 'fac_status' for 'PR' and 'AC' for 'producing' and 'active'
        dfac = dfmin[dfmin['fac_status']=='AC']
        # make all strings lowercase
        dfac = dfac.astype(str).apply(lambda x: x.str.lower())
        # get counts of facilities in each county
        dfcounts = dfac[['loc_id','county']].groupby('county').agg('count')
        # drop superflous column
        dfcounts = dfcounts.drop(dfcounts.index[0])
        # rename 'loc_id' column (containing counts) as 'fac_count'
        dfcounts.columns = ['fac_count']
        # set the index as a column and create new index
        dfcounts = dfcounts.reset_index()
        # join f and dfcounts on 'county' column

        dfcnt_cnty_arr = np.array(dfcounts.county)
        res_cnty_arr = np.array(asthma.county)
        counties_wo_oil = list(set(res_cnty_arr) - set(dfcnt_cnty_arr))

        # outer join on 'county' of dfcounts and result
        merged = pd.merge(dfcounts, asthma, how='outer', on='county')
        # replace NaN with zeros
        merged.fac_count.fillna(0, inplace=True)
        # restore alphabetical sorting by county
        merged = merged.sort_values(by=['county'])


    def plotting(self):
        plt.figure(1)
        plt.scatter(merged.fac_count, merged.asthma_rate)
        plt.plot((0,17000),(0,10), 'r--')
        plt.title('Scatter of fac_count vs asthma_rate')
        plt.xlabel('asthma_rate')
        plt.ylabel('fac_count')
        plt.figure(2)
        plt.scatter(combo.smoker, combo.asthma_rate)
        plt.title('Scatter of smoker vs asthma_rate')
        plt.xlabel('asthma_rate')
        plt.ylabel('smoker')
        plt.plot((5,30),(5,12), 'b--')

        plt.show()

    # def yuma_county(self):
    #     self.dfmin.county['YUMA']
    #     dfmin_yuma = self.dfmin.loc[dfmin['county']=='YUMA']
    #     plt.hist(dfmin_yuma)

    def pivot_table(self):
        dfmin_pivot = pd.pivot_table(dfmin, index=["county"], values=["loc_id"],aggfunc=np.size)
        dfmin_pivot.head(100)
        dfmin_pivot.sort_values(by='loc_id').tail()

class AsthmaEDA(object):
    def __init__(self):
        self.df_ast = None

    def ast_data(self):
        df_ast = pd.read_csv('../data/asthma_prevalence1.csv')
        # make column names lowercase
        df_ast.columns = map(str.lower, df_ast.columns)
        dropped = df_ast.drop(['objectid', 'fips', 'name', 'hsr', 'map_symbol','state_avg', 'hsr_symbol', 'mconfint' ], axis=1)
        # removing text... (note that this leaves just the column vector 'e')
        d = dropped.ctyreg_est.str.split('%').apply(lambda x: x[0])
        # e = d.ctyreg_est.str.split('Estimate ').apply(lambda x: x[1])
        e = d.str.split('Estimate ').apply(lambda x: x[1])
        # convert text to float
        e = e.astype(float)
        # convert to DataFrame
        f = pd.DataFrame(e)
        # rename only column
        f.columns = ['asthma']
        counties = dropped.drop(['asthma', 'ctyreg_est', 'popover18'], axis=1)
        # join counties and e
        # result = pd.concat([counties, e], axis=1)
        asthma = pd.concat([counties, e], axis=1)
        # county names to lowercase
        asthma = asthma.astype(str).apply(lambda x: x.str.lower())
        # rename ctyreg_est as asthma_rate
        asthma.columns = ['county','asthma_rate']
        # convert asthma_rate column to float
        asthma.asthma_rate = asthma.asthma_rate.astype(float)


        # groupby in order to almalgamate duplicates of counties
        asthma = asthma.groupby('county').mean()
        # change index to colunm ('county') and add index
        asthma = asthma.reset_index()


class SmokerEDA(object):
    def __init__(self):
        pass

    def smoke_data(self):
        df_smoke = pd.read_csv('../data/smoking_adults.csv')
        df_smoke.columns = df_smoke.columns.str.lower()
        smokemin = df_smoke[['county', 'smoker']]
        smokegrouped = smokemin.groupby('county')['smoker'].mean()
        smok = smokegrouped.reset_index()
        smok = smok.astype(str).apply(lambda x: x.str.lower())

        smok.smoker = smok.smoker.round(2)
    # def larimer_county(self):
    #     smoke_larimer = smokemin.loc[smokemin['county']=='Larimer']


if __name__ == '__main__':
    oil = OilEDA()
    oil.oil_data()
    # oil.yuma_county()
    oil.pivot_table()

    ast = AsthmaEDA()
    ast.ast_data()

    smk = SmokerEDA()
    smk.smoke_data()
    smk.larimer_county()
