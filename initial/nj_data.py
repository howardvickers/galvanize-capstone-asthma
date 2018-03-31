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
    pm2_5specco = pm2_5spec[pm2_5spec['state'] == 'Colorado']
    pm2_5speccoslim = pm2_5specco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5speccoslim = pm2_5speccoslim.reset_index()
    pm2_5speccoslim = pm2_5speccoslim.drop(['index'], axis=1)
    pm2_5speccoslim['obs_x_mean'] = pm2_5speccoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5speccoslim.county = pm2_5speccoslim.county.str.lower()
    pm2_5speccogroupby = pm2_5speccoslim.groupby('county').sum()
    pm2_5speccogroupby = pm2_5speccogroupby.reset_index()
    pm2_5speccogroupby['new_mean'] = pm2_5speccogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5speccofinal = pm2_5speccogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5speccofinal.columns = ['county', 'pm2_5spec_mean']

    # def pm2_5non_data():
    pm2_5non = pd.read_csv('../data/daily_88502_2017.csv')
    pm2_5non.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5nonco = pm2_5non[pm2_5non['state'] == 'Colorado']
    pm2_5noncoslim = pm2_5nonco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5noncoslim = pm2_5noncoslim.reset_index()
    pm2_5noncoslim = pm2_5noncoslim.drop(['index'], axis=1)
    pm2_5noncoslim['obs_x_mean'] = pm2_5noncoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5noncoslim.county = pm2_5noncoslim.county.str.lower()
    pm2_5noncogroupby = pm2_5noncoslim.groupby('county').sum()
    pm2_5noncogroupby = pm2_5noncogroupby.reset_index()
    pm2_5noncogroupby['new_mean'] = pm2_5noncogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5noncofinal = pm2_5noncogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5noncofinal.columns = ['county', 'pm2_5non_mean']

    # def pm2_5_data():
    pm2_5 = pd.read_csv('../data/daily_88101_2017.csv')
    pm2_5.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm2_5co = pm2_5[pm2_5['state'] == 'Colorado']
    pm2_5coslim = pm2_5co.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm2_5coslim = pm2_5coslim.reset_index()
    pm2_5coslim = pm2_5coslim.drop(['index'], axis=1)
    pm2_5coslim['obs_x_mean'] = pm2_5coslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm2_5coslim.county = pm2_5coslim.county.str.lower()
    pm2_5cogroupby = pm2_5coslim.groupby('county').sum()
    pm2_5cogroupby = pm2_5cogroupby.reset_index()
    pm2_5cogroupby['new_mean'] = pm2_5cogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm2_5cofinal = pm2_5cogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm2_5cofinal.columns = ['county', 'pm2_5_mean']

    # def pm10_data():
    pm10 = pd.read_csv('../data/daily_81102_2017.csv')
    pm10.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    pm10co = pm10[pm10['state'] == 'Colorado']
    pm10coslim = pm10co.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    pm10coslim = pm10coslim.reset_index()
    pm10coslim = pm10coslim.drop(['index'], axis=1)
    pm10coslim['obs_x_mean'] = pm10coslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    pm10coslim.county = pm10coslim.county.str.lower()
    pm10cogroupby = pm10coslim.groupby('county').sum()
    pm10cogroupby = pm10cogroupby.reset_index()
    pm10cogroupby['new_mean'] = pm10cogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    pm10cofinal = pm10cogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    pm10cofinal.columns = ['county', 'pm10_mean']

    # def lead_data():
    lead = pd.read_csv('../data/daily_LEAD_2014.csv')
    lead.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    leadco = lead[lead['state'] == 'Colorado']
    leadcoslim = leadco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    leadcoslim = leadcoslim.reset_index()
    leadcoslim = leadcoslim.drop(['index'], axis=1)
    leadcoslim['obs_x_mean'] = leadcoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    leadcoslim.county = leadcoslim.county.str.lower()
    leadcogroupby = leadcoslim.groupby('county').sum()
    leadcogroupby = leadcogroupby.reset_index()
    leadcogroupby['new_mean'] = leadcogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    leadcofinal = leadcogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    leadcofinal.columns = ['county', 'lead_mean']

    # def nonox_data():
    nonox = pd.read_csv('../data/daily_NONOxNOy_2017.csv')
    nonox.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    nonoxco = nonox[nonox['state'] == 'Colorado']
    nonoxcocoslim = nonoxco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    nonoxcocoslim = nonoxcocoslim.reset_index()
    nonoxcocoslim = nonoxcocoslim.drop(['index'], axis=1)
    nonoxcocoslim['obs_x_mean'] = nonoxcocoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    nonoxcocoslim.county = nonoxcocoslim.county.str.lower()
    nonoxcogroupby = nonoxcocoslim.groupby('county').sum()
    nonoxcogroupby = nonoxcogroupby.reset_index()
    nonoxcogroupby['new_mean'] = nonoxcogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    nonoxcofinal = nonoxcogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    nonoxcofinal.columns = ['county', 'nonox_mean']

    # def haps_data():
    haps = pd.read_csv('../data/daily_HAPS_2017.csv')
    haps.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    hapsco = haps[haps['state'] == 'Colorado']
    hapscoslim = hapsco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    hapscoslim = hapscoslim.reset_index()
    hapscoslim = hapscoslim.drop(['index'], axis=1)
    hapscoslim['obs_x_mean'] = hapscoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    hapscoslim.county = hapscoslim.county.str.lower()
    hapscogroupby = hapscoslim.groupby('county').sum()
    hapscogroupby = hapscogroupby.reset_index()
    hapscogroupby['new_mean'] = hapscogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    hapscofinal = hapscogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    hapscofinal.columns = ['county', 'haps_mean']

    # def vocs_data():
    # vocs16 = pd.read_csv('daily_VOCS_2016.csv')
    vocs = pd.read_csv('../data/daily_VOCS_2017.csv')
    vocs.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    vocsco = vocs[vocs['state'] == 'Colorado']
    vocscoslim = vocsco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    vocscoslim = vocscoslim.reset_index()
    vocscoslim = vocscoslim.drop(['index'], axis=1)
    vocscoslim['obs_x_mean'] = vocscoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    vocscoslim.county = vocscoslim.county.str.lower()
    vocscogroupby = vocscoslim.groupby('county').sum()
    vocscogroupby = vocscogroupby.reset_index()
    vocscogroupby['new_mean'] = vocscogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    vocscofinal = vocscogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    vocscofinal.columns = ['county', 'vocs_mean']

    # def co_data():
    co = pd.read_csv('../data/daily_42101_2017.csv')
    co.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    coco = co[co['state'] == 'Colorado']
    cocoslim = coco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    cocoslim = cocoslim.reset_index()
    cocoslim = cocoslim.drop(['index'], axis=1)
    cocoslim['obs_x_mean'] = cocoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    cocoslim.county = cocoslim.county.str.lower()
    cocogroupby = cocoslim.groupby('county').sum()
    cocogroupby = cocogroupby.reset_index()
    cocogroupby['new_mean'] = cocogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    cocofinal = cocogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    cocofinal.columns = ['county', 'co_mean']

    # def so2_data():
    so2 = pd.read_csv('../data/daily_42401_2017.csv')
    so2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    soco = so2[so2['state'] == 'New Jersey']
    socoslim = soco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    socoslim = socoslim.reset_index()
    socoslim = socoslim.drop(['index'], axis=1)
    socoslim['obs_x_mean'] = socoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    socoslim.county = socoslim.county.str.lower()
    socogroupby = socoslim.groupby('county').sum()
    socogroupby = socogroupby.reset_index()
    socogroupby['new_mean'] = socogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    socofinal = socogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    socofinal.columns = ['county', 'so_mean']

    # def no2_data():
    no2 = pd.read_csv('../data/daily_42602_2017.csv')
    no2.columns = ['st_cd', 'cnt_cd', 'site_nm', 'param_cd', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'units', 'event_type',
           'obs_count', 'obs_perc', 'mean_avg', 'first_max_val', 'first_max_hour',
           'aqi', 'method_cd', 'method', 'local_site', 'address', 'state',
           'county', 'city', 'cbsa', 'last_change_date']
    noco = no2[no2['state'] == 'Colorado']
    nocoslim = noco.drop(['st_cd', 'cnt_cd', 'site_nm', 'poc', 'lat', 'lon', 'datum',
           'param', 'duration', 'pollutant', 'date', 'event_type', 'units', 'aqi',
           'obs_perc', 'first_max_val', 'first_max_hour', 'method_cd', 'method', 'local_site', 'address', 'state',
           'city', 'cbsa', 'last_change_date'], axis=1)
    nocoslim.county = nocoslim.county.str.lower()
    nocoslim = nocoslim.reset_index()
    nocoslim = nocoslim.drop(['index'], axis=1)
    nocoslim['obs_x_mean'] = nocoslim.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    nocogroupby = nocoslim.groupby('county').sum()
    nocogroupby = nocogroupby.reset_index()
    nocogroupby['new_mean'] = nocogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    nocofinal = nocogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean', 'param_cd'], axis=1)
    nocofinal.columns = ['county', 'no_mean']

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
    ozoco = ozoslim[ozoslim['state'] == 'Colorado']
    ozoco.county = ozoco.county.str.lower()
    ozoco = ozoco.reset_index()
    ozoco = ozoco.drop(['index', 'param', 'state', 'param_cd'], axis= 1)
    ozoco['obs_x_mean']  = ozoco.apply(lambda row: row.obs_count * row.mean_avg, axis=1)
    ozocogroupby = ozoco.groupby('county').sum()
    ozocogroupby = ozocogroupby.reset_index()
    ozocogroupby['new_mean'] = ozocogroupby.apply(lambda row: row.obs_x_mean / row.obs_count, axis=1)
    ozocofinal = ozocogroupby.drop(['obs_count', 'mean_avg', 'obs_x_mean'], axis=1)
    ozocofinal.columns = ['county', 'ozo_mean']

    # def asthma_co():
    # https://data-cdphe.opendata.arcgis.com/datasets/asthma-hospitalization-rate-counties
    asthmahospnj = pd.read_csv('../data/asthma_hospitization_nj.csv')
    # asthmahospnj.columns = asthmahospnj.columns.str.lower()
    asthmahospnj.county = asthmahospnj.county.str.lower()
    # asthmahospnj.columns = ['county', 'asthma_rate']

    asthmanj = asthmahospnj

    # def merge_all():
    asozo_co                       = asthmaco.merge(ozocofinal, how="left", on="county")
    asozono_co                     = asozo_co.merge(nocofinal, how="left", on="county")
    asozonoco_co                   = asozono_co.merge(cocofinal, how="left", on="county")
    asozonocoso_co                 = asozonoco_co.merge(socofinal, how="left", on="county")
    asozonocosovocs_co             = asozonocoso_co.merge(vocscofinal, how="left", on="county")
    asozonocosovocshaps_co         = asozonocosovocs_co.merge(hapscofinal, how="left", on="county")
    asozonocosovocshapsnonox_co    = asozonocosovocshaps_co.merge(nonoxcofinal, how="left", on="county")

    asozonocosovocshapsnonoxlead_co                         = asozonocosovocshaps_co.merge(leadcofinal, how="left", on="county")
    asozonocosovocshapsnonoxpm10_co                         = asozonocosovocshapsnonoxlead_co.merge(pm10cofinal, how="left", on="county")
    asozonocosovocshapsnonoxpm10pm2_5_co                    = asozonocosovocshapsnonoxpm10_co.merge(pm2_5cofinal, how="left", on="county")
    asozonocosovocshapsnonoxpm10pm2_5pm2_5non_co            = asozonocosovocshapsnonoxpm10pm2_5_co.merge(pm2_5noncofinal, how="left", on="county")
    asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_co   = asozonocosovocshapsnonoxpm10pm2_5pm2_5non_co.merge(pm2_5speccofinal, how="left", on="county")

    return asozonocosovocshapsnonoxpm10pm2_5pm2_5nonpm2_5spec_co
