import numpy as np
import pandas as pd
import os
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression as LR
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.neighbors import KNeighborsRegressor as KNR
from sklearn.svm import SVR as SVR
from sklearn.linear_model import ElasticNet as EN
from sklearn.ensemble import GradientBoostingRegressor as GBR
import matplotlib.pyplot as plt


def get_data():
    csv_file_path = '../data/the_data_file.csv'

    if os.path.exists(csv_file_path):
        print("Data file found, loading data...")
        with open(csv_file_path, "r") as f:
            data = pd.read_csv(f)

    else:
        print("Data file not found, assembling dataset...")
        from data import join_data as data
        data = data()
        data.to_csv(csv_file_path, index=False)

    return data

def nice_column_names():
    col_dict = { 'air_poll_partic': 'Particulate Air Pollution',
                 'asthma_rate': 'Asthma Rate',
                 'co_mean': 'CO - Pollutant',
                 'county': 'County',
                 'haps_mean': 'HAPS - Pollutant',
                 'high_sch_grad': 'High School Grads',
                 'income_ineq': 'Income Inequality',
                 'lead_mean': 'Lead - Pollutant',
                 'no2_mean': 'NO2 - Pollutant',
                 'nonox_mean': 'NONOxNOy - Pollutant',
                 'obese_adult': 'Obesity (Adult)',
                 'ozo_mean': 'Ozone - Pollutant',
                 'pcp': 'PCP',
                 'pm10_mean': 'PM10 - Pollutant',
                 'pm25_mean': 'PM2.5 Pollutant',
                 'pm25non_mean': 'PM2.5 non FRM Pollutant',
                 'pm25spec_mean': 'PM2.5 Spec - Pollutant',
                 'smoke_adult': 'Smokers (Adult)',
                 'so2_mean': 'SO2 - Pollutant',
                 'state': 'State',
                 'unemployment': 'Unemployment',
                 'uninsured': 'Uninsured Rate',
                 'vocs_mean': 'VOCS - Pollutant',
                 'co': 'Colo.',
                 'fl': 'Fla.',
                 'nj': 'N.J.',
                 'ca': 'Calif.'
                 }

    return col_dict

def feature_selection(data):

    all_columns = ['pm10_mean', 'pm25_mean', 'pm25non_mean', 'pm25spec_mean', 'co_mean',
       'so2_mean', 'no2_mean', 'ozo_mean', 'nonox_mean', 'lead_mean',
       'haps_mean', 'vocs_mean', 'smoke_adult', 'obese_adult', 'uninsured',
       'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']

    drop_columns = ['pm10_mean', 'pm25_mean', 'pm25non_mean', 'pm25spec_mean', 'co_mean',
        'no2_mean', 'ozo_mean', 'nonox_mean', 'lead_mean',
       'haps_mean', 'vocs_mean', 'pcp', 'high_sch_grad', 'income_ineq', 'co', 'ca']

    data = data.drop(drop_columns, axis=1)

    return data, data.columns

def show_columns():
    data = get_data()
    X_train, X_test, y_train, y_test = split_data(data)
    X_train, y_train = remove_county_state(X_train, y_train)
    return X_train.columns

def column_names(X_train):
    column_names = X_train.columns

    nice_labels = ['County', 'Asthma Rate', 'PM10 - Pollutant', 'PM2.5 Pollutant', 'PM2.5 non FRM Pollutant',
       'PM2.5 Spec - Pollutant', 'CO - Pollutant', 'SO2 - Pollutant', 'NO2 - Pollutant', 'Ozone - Pollutant',
       'NONOxNOy - Pollutant', 'Lead - Pollutant', 'HAPS - Pollutant', 'VOCS - Pollutant', 'State',
       'Smokers (Adult)', 'Obesity (Adult)', 'Uninsured Rate', 'PCP', 'High School Grads',
       'Unemployment', 'Income Inequality', 'Particulate Air Pollution']
    label_dict = dict(zip(column_names, nice_labels))

    return label_dict

def fill_nans(data):
    data = data[data.asthma_rate != 0]
    data_nas = data.fillna(0)
    return data_nas

def X_y(df):
    """take data and returns X and y """
    X = df.drop('asthma_rate', axis=1)
    y = df.asthma_rate
    return X, y

def single_county_data(county):
    """takes data and returns X and y for a single county """
    data = get_data()
    data, _ = feature_selection(data)
    cln_data = fill_nans(data)
    single_county = cln_data[cln_data['county'] == county]
    X, y = X_y(single_county)
    X, y = remove_county_state(X, y)
    return X, y

def get_state_data(state):
    """takes data and returns X and y for a single state """
    data = get_data()
    data, _ = feature_selection(data)
    cln_data = fill_nans(data)
    single_state = cln_data[cln_data['state'] == state]
    X, y = X_y(single_state)
    
    return X, y

def split_data(data):
    pass

def remove_county_state(X, y):
    X = X.drop(['county', 'state'], axis=1)

    return X, y

def data_for_gridsearch():
    data = get_data()
    data, _ = feature_selection(data)
    cln_data = fill_nans(data)
    X, y = X_y(cln_data)
    X, y = remove_county_state(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    return X_train, X_test, y_train, y_test


def data_for_predictions():
    data = get_data()
    data, _ = feature_selection(data)
    cln_data = fill_nans(data)
    X, y = X_y(cln_data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    train_model()
