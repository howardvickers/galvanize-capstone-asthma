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

states = {  'California' : 'ca',
            'Colorado' : 'co',
            'Florida' : 'fl',
            'New Jersey' : 'nj'
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
    df = pd.read_csv('../data/asthma_hospitization_ca.csv')
    df.columns = ['year', 'zip', 'age', 'visits', 'asthma_rate', 'fips', 'county']
    df = df.drop(['zip', 'age', 'visits', 'fips'], axis=1)
    df = df[df['year']==2015]
    df = df.drop('year', axis=1)
    df.county = df.county.str.lower()
    df = df.reset_index()
    df = df.drop('index', axis=1)
    df = df.groupby('county').mean()
    df = df.reset_index()
    return df

asthma_datasets = { 'California'    :   asthma_ca(),
                    'Colorado'      :   asthma_ca(),
                    'Florida'       :   asthma_ca(),
                    'New Jersey'    :   asthma_ca()
                    }

state_dataframes = dict()

def merge_all():
    for state, asthma_dataset in asthma_datasets.items():
        basis = asthma_dataset
        for name, dataset in populate_dataframe_dict().items():
            basis = basis.merge(dataset, how="left", on="county")
        state_dataframes[state] = basis
    print(state_dataframes)
    return state_dataframes

if __name__ == '__main__':
    populate_dataframe_dict()
    merge_all()
