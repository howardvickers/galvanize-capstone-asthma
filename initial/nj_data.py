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
    pm2_5specnj = pm2_5spec[pm2_5spec['state'] == 'New Jersey']
    pm2_5specnjslim = pm2_5specnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5specnjslim = pm2_5specnjslim.reset_index()
    pm2_5specnjslim = pm2_5specnjslim.drop(['index'], axis=1)
    pm2_5specnjslim['obs_x_mean'] = pm2_5specnjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5specnjslim.county = pm2_5specnjslim.county.str.lower()
    pm2_5specnjgroupby = pm2_5specnjslim.groupby('county').sum()
    pm2_5specnjgroupby = pm2_5specnjgroupby.reset_index()
    pm2_5specnjgroupby['new_mean'] = pm2_5specnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5specnjfinal = pm2_5specnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5specnjfinal.columns = ['county', 'pm2_5spec_mean']

    # def pm2_5non_data():
    pm2_5non = pd.read_csv('../data/daily_88502_2017.csv')
    pm2_5non.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5nonnj = pm2_5non[pm2_5non['state'] == 'New Jersey']
    pm2_5nonnjslim = pm2_5nonnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5nonnjslim = pm2_5nonnjslim.reset_index()
    pm2_5nonnjslim = pm2_5nonnjslim.drop(['index'], axis=1)
    pm2_5nonnjslim['obs_x_mean'] = pm2_5nonnjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5nonnjslim.county = pm2_5nonnjslim.county.str.lower()
    pm2_5nonnjgroupby = pm2_5nonnjslim.groupby('county').sum()
    pm2_5nonnjgroupby = pm2_5nonnjgroupby.reset_index()
    pm2_5nonnjgroupby['new_mean'] = pm2_5nonnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5nonnjfinal = pm2_5nonnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5nonnjfinal.columns = ['county', 'pm2_5non_mean']

    # def pm2_5_data():
    pm2_5 = pd.read_csv('../data/daily_88101_2017.csv')
    pm2_5.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5nj = pm2_5[pm2_5['state'] == 'New Jersey']
    pm2_5njslim = pm2_5nj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5njslim = pm2_5njslim.reset_index()
    pm2_5njslim = pm2_5njslim.drop(['index'], axis=1)
    pm2_5njslim['obs_x_mean'] = pm2_5njslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5njslim.county = pm2_5njslim.county.str.lower()
    pm2_5njgroupby = pm2_5njslim.groupby('county').sum()
    pm2_5njgroupby = pm2_5njgroupby.reset_index()
    pm2_5njgroupby['new_mean'] = pm2_5njgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5njfinal = pm2_5njgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5njfinal.columns = ['county', 'pm2_5_mean']

    # def pm10_data():
    pm10 = pd.read_csv('../data/daily_81102_2017.csv')
    pm10.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm10nj = pm10[pm10['state'] == 'New Jersey']
    pm10njslim = pm10nj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm10njslim = pm10njslim.reset_index()
    pm10njslim = pm10njslim.drop(['index'], axis=1)
    pm10njslim['obs_x_mean'] = pm10njslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm10njslim.county = pm10njslim.county.str.lower()
    pm10njgroupby = pm10njslim.groupby('county').sum()
    pm10njgroupby = pm10njgroupby.reset_index()
    pm10njgroupby['new_mean'] = pm10njgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm10njfinal = pm10njgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm10njfinal.columns = ['county', 'pm10_mean']

    # def lead_data():
    lead = pd.read_csv('../data/daily_LEAD_2014.csv')
    lead.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    leadnj = lead[lead['state'] == 'New Jersey']
    leadnjslim = leadnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    leadnjslim = leadnjslim.reset_index()
    leadnjslim = leadnjslim.drop(['index'], axis=1)
    leadnjslim['obs_x_mean'] = leadnjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    leadnjslim.county = leadnjslim.county.str.lower()
    leadnjgroupby = leadnjslim.groupby('county').sum()
    leadnjgroupby = leadnjgroupby.reset_index()
    leadnjgroupby['new_mean'] = leadnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    leadnjfinal = leadnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    leadnjfinal.columns = ['county', 'lead_mean']

    # def nonox_data():
    nonox = pd.read_csv('../data/daily_NONOxNOy_2017.csv')
    nonox.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    nonoxnj = nonox[nonox['state'] == 'New Jersey']
    nonoxnjcoslim = nonoxnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    nonoxnjcoslim = nonoxnjcoslim.reset_index()
    nonoxnjcoslim = nonoxnjcoslim.drop(['index'], axis=1)
    nonoxnjcoslim['obs_x_mean'] = nonoxnjcoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    nonoxnjcoslim.county = nonoxnjcoslim.county.str.lower()
    nonoxnjgroupby = nonoxnjcoslim.groupby('county').sum()
    nonoxnjgroupby = nonoxnjgroupby.reset_index()
    nonoxnjgroupby['new_mean'] = nonoxnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    nonoxnjfinal = nonoxnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    nonoxnjfinal.columns = ['county', 'nonox_mean']

    # def haps_data():
    haps = pd.read_csv('../data/daily_HAPS_2017.csv')
    haps.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    hapsnj = haps[haps['state'] == 'New Jersey']
    hapsnjslim = hapsnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    hapsnjslim = hapsnjslim.reset_index()
    hapsnjslim = hapsnjslim.drop(['index'], axis=1)
    hapsnjslim['obs_x_mean'] = hapsnjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    hapsnjslim.county = hapsnjslim.county.str.lower()
    hapsnjgroupby = hapsnjslim.groupby('county').sum()
    hapsnjgroupby = hapsnjgroupby.reset_index()
    hapsnjgroupby['new_mean'] = hapsnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    hapsnjfinal = hapsnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    hapsnjfinal.columns = ['county', 'haps_mean']

    # def vocs_data():
    # vocs16 = pd.read_csv('daily_VOCS_2016.csv')
    vocs = pd.read_csv('../data/daily_VOCS_2017.csv')
    vocs.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    vocsnj = vocs[vocs['state'] == 'New Jersey']
    vocsnjslim = vocsnj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    vocsnjslim = vocsnjslim.reset_index()
    vocsnjslim = vocsnjslim.drop(['index'], axis=1)
    vocsnjslim['obs_x_mean'] = vocsnjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    vocsnjslim.county = vocsnjslim.county.str.lower()
    vocsnjgroupby = vocsnjslim.groupby('county').sum()
    vocsnjgroupby = vocsnjgroupby.reset_index()
    vocsnjgroupby['new_mean'] = vocsnjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    vocsnjfinal = vocsnjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    vocsnjfinal.columns = ['county', 'vocs_mean']

    # def co_data():
    co = pd.read_csv('../data/daily_42101_2017.csv')
    co.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    conj = co[co['state'] == 'New Jersey']
    conjslim = conj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    conjslim = conjslim.reset_index()
    conjslim = conjslim.drop(['index'], axis=1)
    conjslim['obs_x_mean'] = conjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    conjslim.county = conjslim.county.str.lower()
    conjgroupby = conjslim.groupby('county').sum()
    conjgroupby = conjgroupby.reset_index()
    conjgroupby['new_mean'] = conjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    conjfinal = conjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    conjfinal.columns = ['county', 'co_mean']

    # def so2_data():
    so2 = pd.read_csv('../data/daily_42401_2017.csv')
    so2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    sonj = so2[so2['state'] == 'New Jersey']
    sonjslim = sonj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    sonjslim = sonjslim.reset_index()
    sonjslim = sonjslim.drop(['index'], axis=1)
    sonjslim['obs_x_mean'] = sonjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    sonjslim.county = sonjslim.county.str.lower()
    sonjgroupby = sonjslim.groupby('county').sum()
    sonjgroupby = sonjgroupby.reset_index()
    sonjgroupby['new_mean'] = sonjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    sonjfinal = sonjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    sonjfinal.columns = ['county', 'so_mean']

    # def no2_data():
    no2 = pd.read_csv('../data/daily_42602_2017.csv')
    no2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    nonj = no2[no2['state'] == 'New Jersey']
    nonjslim = nonj.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    nonjslim.county = nonjslim.county.str.lower()
    nonjslim = nonjslim.reset_index()
    nonjslim = nonjslim.drop(['index'], axis=1)
    nonjslim['obs_x_mean'] = nonjslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    nonjgroupby = nonjslim.groupby('county').sum()
    nonjgroupby = nonjgroupby.reset_index()
    nonjgroupby['new_mean'] = nonjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    nonjfinal = nonjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    nonjfinal.columns = ['county', 'no_mean']

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
    ozonj = ozoslim[ozoslim['state'] == 'New Jersey']
    ozonj.county = ozonj.county.str.lower()
    ozonj = ozonj.reset_index()
    ozonj = ozonj.drop(['index', 'param', 'state', 'param_cd'], axis= 1)
    ozonj['obs_x_mean']  = ozonj.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    ozonjgroupby = ozonj.groupby('county').sum()
    ozonjgroupby = ozonjgroupby.reset_index()
    ozonjgroupby['new_mean'] = ozonjgroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    ozonjfinal = ozonjgroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean'], axis=1)
    ozonjfinal.columns = ['county', 'ozo_mean']

    # def asthma_nj():
    # https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties
    asthmahospnj = pd.read_csv('../data/asthma_hospitization_nj.csv')
    # asthmahospnj.columns = asthmahospnj.columns.str.lower()
    asthmahospnj.county = asthmahospnj.county.str.lower()
    # asthmahospnj.columns = ['county', 'asthma_rate']

    asthmanj = asthmahospnj

    # def merge_all():
    asozo_nj                       = asthmanj.merge(ozonjfinal, how="left", on="county")
    asozono_nj                     = asozo_nj.merge(nonjfinal, how="left", on="county")
    asozononj_nj                   = asozono_nj.merge(conjfinal, how="left", on="county")
    asozononjso_nj                 = asozononj_nj.merge(sonjfinal, how="left", on="county")
    asozononjsovocs_nj             = asozononjso_nj.merge(vocsnjfinal, how="left", on="county")
    asozononjsovocshaps_nj         = asozononjsovocs_nj.merge(hapsnjfinal, how="left", on="county")
    asozononjsovocshapsnonox_nj    = asozononjsovocshaps_nj.merge(nonoxnjfinal, how="left", on="county")

    asozononjsovocshapsnonoxlead_nj                         = asozononjsovocshaps_nj.merge(leadnjfinal, how="left", on="county")
    asozononjsovocshapsnonoxpm10_nj                         = asozononjsovocshapsnonoxlead_nj.merge(pm10njfinal, how="left", on="county")
    asozononjsovocshapsnonoxpm10pm2_5_nj                    = asozononjsovocshapsnonoxpm10_nj.merge(pm2_5njfinal, how="left", on="county")
    asozononjsovocshapsnonoxpm10pm2_5pm2_5non_nj            = asozononjsovocshapsnonoxpm10pm2_5_nj.merge(pm2_5nonnjfinal, how="left", on="county")
    asozononjsovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_nj   = asozononjsovocshapsnonoxpm10pm2_5pm2_5non_nj.merge(pm2_5specnjfinal, how="left", on="county")

    return asozononjsovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_nj
