import numpy as np
import pandas as pd
# source data: https://data.chhs.ca.gov/dataset/asthma-ed-visit-rates-lghc-indicator-07

# ****************** CREATE VARIABLES ******************
epa_raw =    { 'pm10'      : 'daily_81102_2017',
                'pm25'      : 'daily_88101_2017',
                'pm25non'   : 'daily_88502_2017',
                'pm25spec'  : 'daily_SPEC_2017',
                'co'        : 'daily_42101_2017',
                'so2'       : 'daily_42401_2017',
                'no2'       : 'daily_42602_2017',
                'ozo'       : 'daily_44201_2017',
                'nonox'     : 'daily_NONOxNOy_2017',
                'lead'      : 'daily_LEAD_2014',
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

states_codes = {    'California': 'ca',
                    'Colorado'  : 'co',
                    'Florida'   : 'fl',
                    'New Jersey': 'nj'
                    }

# ****************** CREATE INITIAL DATASETS ******************
def all_socio_econ_data():
    # source data: http://www.countyhealthrankings.org/rankings/data
    xls = pd.ExcelFile('../data/2016CountyHealthRankingsData.xls')
    df = pd.read_excel(xls, 'Ranked Measure Data') # select tab with data
    df = df.iloc[:, [1,2,27,31,63,68,95,105,116,135]] # get: state, county, adult smoking, adult obesity, uninsured, PCP (doctors) rate, high school graduation, unemployment, income inequality, air pollution,
    df.columns = ['state', 'county','smoke_adult', 'obese_adult', 'uninsured', 'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
    df = df.drop([0]) # drop first row (previously header)
    df.reset_index(level=0, drop=True, inplace=True) # reset index and drop the old index as column
    df.county = df.county.str.lower()
    df.state = df.state.str.lower()
    df_num = df.iloc[:, 2:10].apply(pd.to_numeric) # make all other columns numerical (this will enable .describe() for each column)

    # join back up all columns in a way that avoids numeric columns becoming all "NaN"
    df_soc_econ = pd.concat([df.state.reset_index(drop=True), df.county.reset_index(drop=True), df_num.reset_index(drop=True)], axis=1)

    fips = make_fips_df()
    fips = fips.drop(['state'], axis=1)
    socio_econ_fips = df_soc_econ.merge(fips, how="left", on="county")
    socio_econ_fips = socio_econ_fips.drop(['county'], axis=1)


    return df_soc_econ, socio_econ_fips # this is all the socio-economic data in one dataframe

def asthma_ca():
    # https://data.chhs.ca.gov/dataset/asthma-emergency-department-visit-rates-by-zip-code
    # asthma rate quoted as per 10,000 people
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

    fips = make_fips_df()[make_fips_df()['state']=='california']
    fips = fips.drop(['state'], axis=1)
    asthma_fips = df.merge(fips, how="left", on="county")
    asthma_fips = asthma_fips.drop(['county'], axis=1)
    return df, asthma_fips # this is asthma data for this state

def asthma_co():
    # https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties
    # asthma rate quoted as per 100,000 people
    asthma_co_drop_lst = [  'objectid', 'county_fips', 'l95ci', 'u95ci',
                            'stateadjrate', 'sl95ci', 'su95ci', 'display']
    df = pd.read_csv('../data/asthma_hospitization_co.csv')
    df.columns = df.columns.str.lower()
    df = df.drop(asthma_co_drop_lst, axis=1)
    df.county_name = df.county_name.str.lower()
    df.columns = ['county', 'asthma_rate']
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate / 10, axis=1)

    fips = make_fips_df()[make_fips_df()['state']=='colorado']
    fips = fips.drop(['state'], axis=1)
    asthma_fips = df.merge(fips, how="left", on="county")
    asthma_fips = asthma_fips.drop(['county'], axis=1)
    return df, asthma_fips # this is asthma data for this state

def asthma_fl():
    # http://www.flhealthcharts.com/charts/OtherIndicators/NonVitalIndDataViewer.aspx?cid=9755
    # asthma rate quoted as per 100,000 people
    df = pd.read_csv('../data/asthma_hospitization_fl.csv')
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate +.01, axis=1) # remove any zeros from 'asthma_rate' column
    df['asthma_rate']= df.apply(lambda row: row.asthma_rate / 10, axis=1) # convert rate to per 10,000 (from per 100,000)
    df = df.drop('Unnamed: 0', axis=1)

    fips = make_fips_df()[make_fips_df()['state']=='florida']
    fips = fips.drop(['state'], axis=1)
    asthma_fips = df.merge(fips, how="left", on="county")
    asthma_fips = asthma_fips.drop(['county'], axis=1)
    return df, asthma_fips # this is asthma data for this state

def asthma_nj():
    # https://www26.state.nj.us/doh-shad/indicator/view/NJASTHMAHOSP.stateAAR.html
    # asthma rate quoted as per 10,000 people
    df = pd.read_csv('../data/asthma_hospitization_nj.csv')
    df.county = df.county.str.lower()

    fips = make_fips_df()[make_fips_df()['state']=='new jersey']
    fips = fips.drop(['state'], axis=1)
    asthma_fips = df.merge(fips, how="left", on="county")
    asthma_fips = asthma_fips.drop(['county'], axis=1)
    return df, asthma_fips # this is asthma data for this state

def make_fips_df():
    fips = pd.ExcelFile('../data/fips.xls')
    fips = pd.read_excel(fips)
    fips.columns = ['state', 'county', 'fips_state', 'fips_county']
    fips = fips.iloc[1:,:]
    fips.reset_index(level=0, drop=True, inplace=True)
    fips['fips'] = fips.fips_state + fips.fips_county
    fips = fips.drop(['fips_state', 'fips_county'], axis=1)
    fips.state = fips.state.str.lower()
    fips.county = fips.county.str.lower()
    return fips

def make_fips_dicts(state, code):
    # for state, code in states_codes.items():
    df = 'fips_{}'.format(code)
    df = make_fips_df()
    df = df[df['state']==state]
    d = 'fips_dict_{}'.format(code)
    d = df.set_index('county').to_dict()['fips']
    return d

# ****************** ASSEMBLE DATASETS ******************
def choose_states():
    states = ['California', 'Colorado', 'Florida', 'New Jersey']
    # states = ['California', 'Colorado', 'Florida']
    # states = ['California', 'Colorado', 'New Jersey']
    # states = ['California', 'Colorado']
    return states # this is just a list of states

def populate_epa_state(state_name, state_code):
    epa_state = 'epa_{}'.format(state_code)
    epa_state = dict()
    for pollutant, filename in epa_raw.items():
        dfname = '{}_{}'.format(pollutant, state_code)
        epa_state[dfname] = make_pollutant_df(filename, state_name, pollutant)
    # print('populate_epa_state:', epa_state)
    return epa_state # this is dictionary with epa pollutants for this state

def make_pollutant_df(file, state_name, pollutant):
    df = pd.read_csv('../data/{}.csv'.format(file))
    df.columns = column_list
    df = df[df['state'] == state_name]
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
    print('make_pollutant_df:', df.columns)
    return df # this is a dataframe for a pollutant for a given state

def join_side_by_side(state):
    asthma_datasets = { 'California'    :   asthma_ca()[0],
                        'Colorado'      :   asthma_co()[0],
                        'Florida'       :   asthma_fl()[0],
                        'New Jersey'    :   asthma_nj()[0]
                        }

    df = asthma_datasets[state]
    for name, dataset in populate_epa_state(state, states_codes[state]).items():
        df = df.merge(dataset, how="left", on="county")
    print('join_side_by_side:', df.columns)
    return df # this is a dataframe with asthma and pollutant data for given state

def get_each_state_data(state):
    # socio-economic data for this state
    data, _ = all_socio_econ_data()
    state_socio_econ_data = data[data['state'] == state.lower()]

    # asthma-pollutant data for this state
    asthma_pollutants = join_side_by_side(state)

    # join socio-economic and asthma and pollutant data into one df
    df = asthma_pollutants.merge(state_socio_econ_data, how="left", on="county")
    print('get_each_state_data:', df.columns)
    return df # this is all the data for this state

def join_data():
    list_of_each_states_data = []
    for state in choose_states():
        each_state_data = get_each_state_data(state)
        list_of_each_states_data.append(each_state_data)
    df = pd.concat(list_of_each_states_data)
    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    print('join_data:', df.columns)

    return df # this is all the data stacked for the chosen states

if __name__ == '__main__':
    join_data()
