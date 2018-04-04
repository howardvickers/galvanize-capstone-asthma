import numpy as np
import pandas as pd
# source data: https://data.chhs.ca.gov/dataset/asthma-ed-visit-rates-lghc-indicator-07

epa_datasets = {'pm10'      : 'daily_81102_2017',
                # 'pm25'      : 'daily_88101_2017',
                # 'pm25non'   : 'daily_88502_2017',
                # 'pm25spec'  : 'daily_SPEC_2017',
                # 'co'        : 'daily_42101_2017',
                # 'so2'       : 'daily_42401_2017',
                # 'no2'       : 'daily_42602_2017',
                # 'ozo'       : 'daily_44201_2017',
                # 'nonox'     : 'daily_NONOxNOy_2017',
                # 'lead'      : 'daily_LEAD_2014',
                'haps'      : 'daily_HAPS_2017',
                'vocs'      : 'daily_VOCS_2017'
                }

column_list =   ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
   'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
   'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
   'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
   'county', 'city', 'cbsa', 'last_change_date']

columns_to_drop = ['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
   'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
   'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
   'city', 'cbsa', 'last_change_date']

columns_to_drop2 = ['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd']

states = {  'California': 'ca',
            'Colorado'  : 'co',
            'Florida'   : 'fl',
            'New Jersey': 'nj'
            }

dataframe_dict = dict()

def populate_dataframe_dict():
    for state_name, state_code in states.items():
        for pollutant, filename in epa_datasets.items():
            dfname = '{}_{}'.format(pollutant, state_code)
            dataframe_dict[dfname] = make_df(dfname, filename, state_name, pollutant)
    print(dataframe_dict)
    return dataframe_dict

def make_df(name, file, state, pollutant):
    df = pd.read_csv('../data/{}.csv'.format(file))
    df.columns = column_list
    df = df[df['state'] == state]
    df = df.drop(columns_to_drop, axis=1)
    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    df['obs_x_mean'] = df.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    df.county = df.county.str.lower()
    df = df.groupby('county').sum()
    df = df.reset_index()
    df['new_mean'] = df.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    df = df.drop(columns_to_drop2, axis=1)
    df.columns = ['county', '{}_mean'.format(pollutant)]
    # k+'{}'.format(state_code) = df
    return df

def asthma_ca():
# https://data.chhs.ca.gov/dataset/asthma-emergency-department-visit-rates-by-zip-code
    asthma_ca_drop_lst = ['zip', 'age', 'visits', 'fips']
    df = pd.read_csv('../data/asthma_hospitization_ca.csv')
    df.columns = ['year', 'zip', 'age', 'visits', 'asthma_rate', 'fips', 'county']
    df = df.drop(asthma_ca_drop_lst, axis=1)
    df = df[df['year']==2015]
    df = df.drop('year', axis=1)
    df.county = df.county.str.lower()
    df = df.reset_index()
    df = df.drop('index', axis=1)
    df = df.groupby('county').mean()
    df = df.reset_index()
    return df

def asthma_co():
    # https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties
    asthma_co_drop_lst = [  'objectid', 'county_fips', 'l95ci', 'u95ci',
                            'stateadjrate', 'sl95ci', 'su95ci', 'display']
    df = pd.read_csv('../data/asthma_hospitization_co.csv')
    df.columns = df.columns.str.lower()
    df = df.drop(asthma_co_drop_lst, axis=1)
    df.county_name = df.county_name.str.lower()
    df.columns = ['county', 'asthma_rate']
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate / 10, axis=1)
    return df

def asthma_fl():
    # http://www.flhealthcharts.com/charts/OtherIndicators/NonVitalIndDataViewer.aspx?cid=9755
    df = pd.read_csv('../data/asthma_hospitization_fl.csv')
    # remove any zeros from 'asthma_rate' column
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate +.01, axis=1)
    # convert rate to per 10,000 (from per 100,000)
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate / 10, axis=1)
    df = df.drop('Unnamed: 0', axis=1)
    return df

def asthma_nj():
    # https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties
    df = pd.read_csv('../data/asthma_hospitization_nj.csv')
    df.county = df.county.str.lower()
    return df

def merge_states():
    asthma_datasets = { 'California'    :   asthma_ca(),
                        'Colorado'      :   asthma_co(),
                        'Florida'       :   asthma_fl(),
                        'New Jersey'    :   asthma_nj()
                        }

    state_dataframes = dict()

    for state, asthma_dataset in asthma_datasets.items():
        basis = asthma_dataset
        for name, dataset in populate_dataframe_dict().items():
            basis = basis.merge(dataset, how="left", on="county")
        state_dataframes[state] = basis
    print(state_dataframes)
    return state_dataframes

def socio_econ_data():
    # source data: http://www.countyhealthrankings.org/rankings/data
    xls = pd.ExcelFile('../data/2017CountyHealthRankingsData.xls')
    df = pd.read_excel(xls, 'Ranked Measure Data') # select tab with data
    df = df.iloc[:, [1,2,27,31,63,68,95,105,116,135]] # get: state, county, adult smoking, adult obesity, uninsured, PCP (doctors) rate, high school graduation, unemployment, income inequality, air pollution,
    df.columns = ['state', 'county','smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
    df = df.drop([0]) # drop first row (previously header)
    df.reset_index(level=0, drop=True, inplace=True) # reset index and drop the old index as column
    df.county = df.county.str.lower()
    df.state = df.state.str.lower()
    df_num = df.iloc[:, 2:10].apply(pd.to_numeric) # make all other columns numerical (this will enable .describe() for each column)

    # join back up all columns in a way that avoids numeric columns becoming all "NaN"
    dfc = pd.concat([df.state.reset_index(drop=True), df.county.reset_index(drop=True), df_num.reset_index(drop=True)], axis=1)

    # combine for all states selected
    cocanjfl = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'new jersey') | (dfc['state'] == 'florida')]
    cocafl = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'florida')]
    cocanj = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') | (dfc['state'] == 'new jersey') ]
    coca = dfc[(dfc['state'] == 'colorado') | (dfc['state'] == 'california') ]

    return coca

def join_data():
    table_lst = []
    for state, df in merge_states().items():
        table_lst.append(df)

    join_cocanjfl = pd.concat(table_lst)
    join_cocanjfl = join_cocanjfl.reset_index()
    join_cocanjfl = join_cocanjfl.drop(['index'], axis=1)

    socioecon   = socio_econ_data()
    all_data    = socioecon.merge(join_cocanjfl, how="left", on="county")

    print('all_data.head():', all_data.head())
    print('states in all_data:', all_data.state.unique())
    return all_data

if __name__ == '__main__':
    join_data()
