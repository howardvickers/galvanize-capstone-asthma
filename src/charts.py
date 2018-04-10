import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt

from modclass import train_model as tm
from modclass import show_columns

def chart_feature_importances():
    model = tm()
    feat_imps = model.feature_importances_

    # from data import column_names as cols
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
                 'vocs_mean': 'VOCS - Pollutant'}

    X_train_dot_columns = show_columns()

    imps, names = zip(*sorted(zip(feat_imps, [col_dict.get(x, x) for x in X_train_dot_columns])))

    plt.style.use('bmh')
    plt.barh(range(len(names)), imps, align='center')
    plt.yticks(range(len(names)), names)
    plt.xlabel('Relative Importance of Features', fontsize=10)
    plt.ylabel('Features', fontsize=10)
    plt.tight_layout()
    plt.savefig('static/images/feat_imps.png')

if __name__ == '__main__':
    chart_feature_importances()
