import numpy as np
import pandas as pd
# source data: https://aqs.epa.gov/aqsweb/airdata/download_files.html

# def nonox_data():
nonox = pd.read_csv('data/daily_NONOxNOy_2017.csv')
nonox.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
nonoxca = nonox[nonox['state'] == 'California']
nonoxcacoslim = nonoxca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
nonoxcacoslim = nonoxcacoslim.reset_index()
nonoxcacoslim = nonoxcacoslim.drop(['index'], axis=1)
nonoxcacoslim['obs_x_mean'] = nonoxcacoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
nonoxcacoslim.county = nonoxcacoslim.county.str.lower()
nonoxcagroupby = nonoxcacoslim.groupby('county').sum()
nonoxcagroupby = nonoxcagroupby.reset_index()
nonoxcagroupby['new_mean'] = nonoxcagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
nonoxcafinal = nonoxcagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
nonoxcafinal.columns = ['county', 'nonox_mean']



# def haps_data():
haps = pd.read_csv('data/daily_HAPS_2017.csv')
haps.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
hapsca = haps[haps['state'] == 'California']
hapscaslim = hapsca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
hapscaslim = hapscaslim.reset_index()
hapscaslim = hapscaslim.drop(['index'], axis=1)
hapscaslim['obs_x_mean'] = hapscaslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
hapscaslim.county = hapscaslim.county.str.lower()
hapscagroupby = hapscaslim.groupby('county').sum()
hapscagroupby = hapscagroupby.reset_index()
hapscagroupby['new_mean'] = hapscagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
hapscafinal = hapscagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
hapscafinal.columns = ['county', 'haps_mean']




# def vocs_data():
# vocs16 = pd.read_csv('daily_VOCS_2016.csv')
vocs = pd.read_csv('data/daily_VOCS_2017.csv')
vocs.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
vocsca = vocs[vocs['state'] == 'California']
vocscaslim = vocsca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
vocscaslim = vocscaslim.reset_index()
vocscaslim = vocscaslim.drop(['index'], axis=1)
vocscaslim['obs_x_mean'] = vocscaslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
vocscaslim.county = vocscaslim.county.str.lower()
vocscagroupby = vocscaslim.groupby('county').sum()
vocscagroupby = vocscagroupby.reset_index()
vocscagroupby['new_mean'] = vocscagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
vocscafinal = vocscagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
vocscafinal.columns = ['county', 'vocs_mean']


# def co_data():
co = pd.read_csv('data/daily_42101_2017.csv')
co.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
coca = co[co['state'] == 'California']
cocaslim = coca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
cocaslim = cocaslim.reset_index()
cocaslim = cocaslim.drop(['index'], axis=1)
cocaslim['obs_x_mean'] = cocaslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
cocaslim.county = cocaslim.county.str.lower()
cocagroupby = cocaslim.groupby('county').sum()
cocagroupby = cocagroupby.reset_index()
cocagroupby['new_mean'] = cocagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
cocafinal = cocagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
cocafinal.columns = ['county', 'co_mean']


# def so2_data():
so2 = pd.read_csv('data/daily_42401_2017.csv')
so2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
soca = so2[so2['state'] == 'New Jersey']
socaslim = soca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
socaslim = socaslim.reset_index()
socaslim = socaslim.drop(['index'], axis=1)
socaslim['obs_x_mean'] = socaslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
socaslim.county = socaslim.county.str.lower()
socagroupby = socaslim.groupby('county').sum()
socagroupby = socagroupby.reset_index()
socagroupby['new_mean'] = socagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
socafinal = socagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
socafinal.columns = ['county', 'so_mean']

# def no2_data():
no2 = pd.read_csv('data/daily_42602_2017.csv')
no2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
       'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
       'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
       'county', 'city', 'cbsa', 'last_change_date']
noca = no2[no2['state'] == 'Colorado']
nocaslim = noca.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
       'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
       'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
       'city', 'cbsa', 'last_change_date'], axis=1)
nocaslim.county = nocaslim.county.str.lower()
nocaslim = nocaslim.reset_index()
nocaslim = nocaslim.drop(['index'], axis=1)
nocaslim['obs_x_mean'] = nocaslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
nocagroupby = nocaslim.groupby('county').sum()
nocagroupby = nocagroupby.reset_index()
nocagroupby['new_mean'] = nocagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
nocafinal = nocagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
nocafinal.columns = ['county', 'no_mean']

# def ozone_data():
ozo = pd.read_csv('data/daily_44201_2017.csv')
ozoslim = ozo.drop(['State Code', 'County Code', 'Site Num', 'POC',
       'Latitude', 'Longitude', 'Datum', 'Sample Duration',
       'Pollutant Standard', 'Date Local', 'Units of Measure', 'Event Type',
        'Observation Percent',
       '1st Max Value', '1st Max Hour', 'AQI', 'Method Code', 'Method Name',
       'Local Site Name', 'Address', 'City Name',
       'CBSA Name', 'Date of Last Change'], axis=1)
ozoslim.columns = ['param_cd', 'param', 'obs_count', 'mean_avg', 'state', 'county']
ozoca = ozoslim[ozoslim['state'] == 'Colorado']
ozoca.county = ozoca.county.str.lower()
ozoca = ozoca.reset_index()
ozoca = ozoca.drop(['index', 'param', 'state', 'param_cd'], axis= 1)
ozoca['obs_x_mean']  = ozoca.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
ozocagroupby = ozoca.groupby('county').sum()
ozocagroupby = ozocagroupby.reset_index()
ozocagroupby['new_mean'] = ozocagroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
ozocafinal = ozocagroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean'], axis=1)
ozocafinal.columns = ['county', 'ozo_mean']

# def asthma_ca():
asthmahospca = pd.read_csv('data/asthma_hospitization_ca.csv')
asthmahospca.columns = ['year', 'zip', 'age', 'visits', 'asthma_rate', 'fips', 'county']
asthmahospca = asthmahospca.drop(['zip', 'age', 'visits', 'fips'], axis=1)
asthmahospca2015 = asthmahospca[asthmahospca['year']==2015]
asthmahospca2015 = asthmahospca2015.drop('year', axis=1)
asthmahospca2015.county = asthmahospca2015.county.str.lower()
asthmahospca2015 = asthmahospca2015.reset_index()
asthmahospca2015 = asthmahospca2015.drop('index', axis=1)
asthmahospca2015 = asthmahospca2015.groupby('county').mean()
asthmahospca2015 = asthmahospca2015.reset_index()
asthmaca = asthmahospca2015

# def merge_all():
asozo_ca                       = asthmaca.merge(ozocafinal, how="left", on="county")
asozono_ca                     = asozo_ca.merge(nocafinal, how="left", on="county")
asozonoco_ca                   = asozono_ca.merge(cocafinal, how="left", on="county")
asozonocoso_ca                 = asozonoco_ca.merge(socafinal, how="left", on="county")
asozonocosovocs_ca             = asozonocoso_ca.merge(vocscafinal, how="left", on="county")
asozonocosovocshaps_ca         = asozonocosovocs_ca.merge(hapscafinal, how="left", on="county")
asozonocosovocshapsnonox_ca    = asozonocosovocshaps_ca.merge(nonoxcafinal, how="left", on="county")
