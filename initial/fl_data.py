import numpy as np
import pandas as pd
# source data: https://aqs.epa.gov/aqsweb/airdata/download_files.html

def get_data():
    # def pm2_5spec_data():
    pm2_5spec = pd.read_csv('../data/daily_88502_2017.csv')
    pm2_5spec.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5specfl = pm2_5spec[pm2_5spec['state'] == 'Florida']
    pm2_5specflslim = pm2_5specfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5specflslim = pm2_5specflslim.reset_index()
    pm2_5specflslim = pm2_5specflslim.drop(['index'], axis=1)
    pm2_5specflslim['obs_x_mean'] = pm2_5specflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5specflslim.county = pm2_5specflslim.county.str.lower()
    pm2_5specflgroupby = pm2_5specflslim.groupby('county').sum()
    pm2_5specflgroupby = pm2_5specflgroupby.reset_index()
    pm2_5specflgroupby['new_mean'] = pm2_5specflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5specflfinal = pm2_5specflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5specflfinal.columns = ['county', 'pm2_5spec_mean']

    # def pm2_5non_data():
    pm2_5non = pd.read_csv('../data/daily_88502_2017.csv')
    pm2_5non.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5nonfl = pm2_5non[pm2_5non['state'] == 'Florida']
    pm2_5nonflslim = pm2_5nonfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5nonflslim = pm2_5nonflslim.reset_index()
    pm2_5nonflslim = pm2_5nonflslim.drop(['index'], axis=1)
    pm2_5nonflslim['obs_x_mean'] = pm2_5nonflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5nonflslim.county = pm2_5nonflslim.county.str.lower()
    pm2_5nonflgroupby = pm2_5nonflslim.groupby('county').sum()
    pm2_5nonflgroupby = pm2_5nonflgroupby.reset_index()
    pm2_5nonflgroupby['new_mean'] = pm2_5nonflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5nonflfinal = pm2_5nonflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5nonflfinal.columns = ['county', 'pm2_5non_mean']

    # def pm2_5_data():
    pm2_5 = pd.read_csv('../data/daily_88101_2017.csv')
    pm2_5.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5fl = pm2_5[pm2_5['state'] == 'Florida']
    pm2_5flslim = pm2_5fl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5flslim = pm2_5flslim.reset_index()
    pm2_5flslim = pm2_5flslim.drop(['index'], axis=1)
    pm2_5flslim['obs_x_mean'] = pm2_5flslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5flslim.county = pm2_5flslim.county.str.lower()
    pm2_5flgroupby = pm2_5flslim.groupby('county').sum()
    pm2_5flgroupby = pm2_5flgroupby.reset_index()
    pm2_5flgroupby['new_mean'] = pm2_5flgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5flfinal = pm2_5flgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5flfinal.columns = ['county', 'pm2_5_mean']

    # def pm10_data():
    pm10 = pd.read_csv('../data/daily_81102_2017.csv')
    pm10.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm10fl = pm10[pm10['state'] == 'Florida']
    pm10flslim = pm10fl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm10flslim = pm10flslim.reset_index()
    pm10flslim = pm10flslim.drop(['index'], axis=1)
    pm10flslim['obs_x_mean'] = pm10flslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm10flslim.county = pm10flslim.county.str.lower()
    pm10flgroupby = pm10flslim.groupby('county').sum()
    pm10flgroupby = pm10flgroupby.reset_index()
    pm10flgroupby['new_mean'] = pm10flgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm10flfinal = pm10flgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm10flfinal.columns = ['county', 'pm10_mean']

    # def lead_data():
    lead = pd.read_csv('../data/daily_LEAD_2014.csv')
    lead.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    leadfl = lead[lead['state'] == 'Florida']
    leadflslim = leadfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    leadflslim = leadflslim.reset_index()
    leadflslim = leadflslim.drop(['index'], axis=1)
    leadflslim['obs_x_mean'] = leadflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    leadflslim.county = leadflslim.county.str.lower()
    leadflgroupby = leadflslim.groupby('county').sum()
    leadflgroupby = leadflgroupby.reset_index()
    leadflgroupby['new_mean'] = leadflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    leadflfinal = leadflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    leadflfinal.columns = ['county', 'lead_mean']

    # def nonox_data():
    nonox = pd.read_csv('../data/daily_NONOxNOy_2017.csv')
    nonox.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    nonoxfl = nonox[nonox['state'] == 'Florida']
    nonoxflcoslim = nonoxfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    nonoxflcoslim = nonoxflcoslim.reset_index()
    nonoxflcoslim = nonoxflcoslim.drop(['index'], axis=1)
    nonoxflcoslim['obs_x_mean'] = nonoxflcoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    nonoxflcoslim.county = nonoxflcoslim.county.str.lower()
    nonoxflgroupby = nonoxflcoslim.groupby('county').sum()
    nonoxflgroupby = nonoxflgroupby.reset_index()
    nonoxflgroupby['new_mean'] = nonoxflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    nonoxflfinal = nonoxflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    nonoxflfinal.columns = ['county', 'nonox_mean']

    # def haps_data():
    haps = pd.read_csv('../data/daily_HAPS_2017.csv')
    haps.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    hapsfl = haps[haps['state'] == 'Florida']
    hapsflslim = hapsfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    hapsflslim = hapsflslim.reset_index()
    hapsflslim = hapsflslim.drop(['index'], axis=1)
    hapsflslim['obs_x_mean'] = hapsflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    hapsflslim.county = hapsflslim.county.str.lower()
    hapsflgroupby = hapsflslim.groupby('county').sum()
    hapsflgroupby = hapsflgroupby.reset_index()
    hapsflgroupby['new_mean'] = hapsflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    hapsflfinal = hapsflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    hapsflfinal.columns = ['county', 'haps_mean']

    # def vocs_data():
    # vocs16 = pd.read_csv('daily_VOCS_2016.csv')
    vocs = pd.read_csv('../data/daily_VOCS_2017.csv')
    vocs.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    vocsfl = vocs[vocs['state'] == 'Florida']
    vocsflslim = vocsfl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    vocsflslim = vocsflslim.reset_index()
    vocsflslim = vocsflslim.drop(['index'], axis=1)
    vocsflslim['obs_x_mean'] = vocsflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    vocsflslim.county = vocsflslim.county.str.lower()
    vocsflgroupby = vocsflslim.groupby('county').sum()
    vocsflgroupby = vocsflgroupby.reset_index()
    vocsflgroupby['new_mean'] = vocsflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    vocsflfinal = vocsflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    vocsflfinal.columns = ['county', 'vocs_mean']

    # def co_data():
    co = pd.read_csv('../data/daily_42101_2017.csv')
    co.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    cofl = co[co['state'] == 'Florida']
    coflslim = cofl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    coflslim = coflslim.reset_index()
    coflslim = coflslim.drop(['index'], axis=1)
    coflslim['obs_x_mean'] = coflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    coflslim.county = coflslim.county.str.lower()
    coflgroupby = coflslim.groupby('county').sum()
    coflgroupby = coflgroupby.reset_index()
    coflgroupby['new_mean'] = coflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    coflfinal = coflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    coflfinal.columns = ['county', 'co_mean']

    # def so2_data():
    so2 = pd.read_csv('../data/daily_42401_2017.csv')
    so2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    sofl = so2[so2['state'] == 'Florida']
    soflslim = sofl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    soflslim = soflslim.reset_index()
    soflslim = soflslim.drop(['index'], axis=1)
    soflslim['obs_x_mean'] = soflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    soflslim.county = soflslim.county.str.lower()
    soflgroupby = soflslim.groupby('county').sum()
    soflgroupby = soflgroupby.reset_index()
    soflgroupby['new_mean'] = soflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    soflfinal = soflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    soflfinal.columns = ['county', 'so_mean']

    # def no2_data():
    no2 = pd.read_csv('../data/daily_42602_2017.csv')
    no2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    nofl = no2[no2['state'] == 'Florida']
    noflslim = nofl.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    noflslim.county = noflslim.county.str.lower()
    noflslim = noflslim.reset_index()
    noflslim = noflslim.drop(['index'], axis=1)
    noflslim['obs_x_mean'] = noflslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    noflgroupby = noflslim.groupby('county').sum()
    noflgroupby = noflgroupby.reset_index()
    noflgroupby['new_mean'] = noflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    noflfinal = noflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    noflfinal.columns = ['county', 'no_mean']

    # def ozone_data():
    ozo = pd.read_csv('../data/daily_44201_2017.csv')
    ozoslim = ozo.drop(['State Code', 'County Code', 'Site Num', 'POC',
           'Latitude', 'Longitude', 'Datum', 'Sample Duration',
           'Pollutant Standard', 'Date Local', 'Units of Measure', 'Event Type',
            'Observation Percent',
           '1st Max Value', '1st Max Hour', 'AQI', 'Method Code', 'Method Name',
           'Local Site Name', 'Address', 'City Name',
           'CBSA Name', 'Date of Last Change'], axis=1)
    ozoslim.columns = ['param_cd', 'param', 'obs_count', 'mean_avg', 'state', 'county']
    ozofl = ozoslim[ozoslim['state'] == 'Florida']
    ozofl.county = ozofl.county.str.lower()
    ozofl = ozofl.reset_index()
    ozofl = ozofl.drop(['index', 'param', 'state', 'param_cd'], axis= 1)
    ozofl['obs_x_mean']  = ozofl.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    ozoflgroupby = ozofl.groupby('county').sum()
    ozoflgroupby = ozoflgroupby.reset_index()
    ozoflgroupby['new_mean'] = ozoflgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    ozoflfinal = ozoflgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean'], axis=1)
    ozoflfinal.columns = ['county', 'ozo_mean']

    # def asthma_fl():
    # http://www.flhealthcharts.com/charts/OtherIndicators/NonVitalIndDataViewer.aspx?cid=9755
    asthmahospfl = pd.read_csv('../data/asthma_hospitization_fl.csv')
    # asthmahospfl.columns = asthmahospfl.columns.str.lower()
    asthmahospfl.county = asthmahospfl.county.str.lower()
    # asthmahospfl.columns = ['county', 'asthma_rate']
    asthmahospfl['asthma_rate']= asthmahospfl.apply(lambda row: row.asthma_rate / 10, axis=1)

    asthmafl = asthmahospfl.drop('Unnamed: 0', axis=1)

    # def merge_all():
    asozo_fl                       = asthmafl.merge(ozoflfinal, how="left", on="county")
    asozono_fl                     = asozo_fl.merge(noflfinal, how="left", on="county")
    asozonofl_fl                   = asozono_fl.merge(coflfinal, how="left", on="county")
    asozonoflso_fl                 = asozonofl_fl.merge(soflfinal, how="left", on="county")
    asozonoflsovocs_fl             = asozonoflso_fl.merge(vocsflfinal, how="left", on="county")
    asozonoflsovocshaps_fl         = asozonoflsovocs_fl.merge(hapsflfinal, how="left", on="county")
    asozonoflsovocshapsnonox_fl    = asozonoflsovocshaps_fl.merge(nonoxflfinal, how="left", on="county")

    asozonoflsovocshapsnonoxlead_fl                         = asozonoflsovocshaps_fl.merge(leadflfinal, how="left", on="county")
    asozonoflsovocshapsnonoxpm10_fl                         = asozonoflsovocshapsnonoxlead_fl.merge(pm10flfinal, how="left", on="county")
    asozonoflsovocshapsnonoxpm10pm2_5_fl                    = asozonoflsovocshapsnonoxpm10_fl.merge(pm2_5flfinal, how="left", on="county")
    asozonoflsovocshapsnonoxpm10pm2_5pm2_5non_fl            = asozonoflsovocshapsnonoxpm10pm2_5_fl.merge(pm2_5nonflfinal, how="left", on="county")
    asozonoflsovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_fl   = asozonoflsovocshapsnonoxpm10pm2_5pm2_5non_fl.merge(pm2_5specflfinal, how="left", on="county")

    return asozonoflsovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_fl
