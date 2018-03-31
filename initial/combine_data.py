import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
# source data: http://www.countyhealthrankings.org/rankings/data

from co_data import get_data as colorado
from ca_data import get_data as california
from nj_data import get_data as newjersey
from us_data import get_data as socio_economic

def join_data():
    # def combine_tables():
    table1 = colorado()
    table2 = california()
    table3 = newjersey()
    socioecon = socio_economic()

    join_cocanj = pd.concat([table1, table2, table3])
    join_cocanj = join_cocanj.reset_index()
    join_cocanj = join_cocanj.drop(['index'], axis=1)

    socio_pollute = socioecon.merge(join_cocanj, how="left", on="county")

    print(socio_pollute.head())
    return socio_pollute
