import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor as RFR

from data_processing import get_data
from data_processing import split_data
from data_processing import remove_county_state
from data_processing import feature_selection
from data_processing import data_for_gridsearch

def calc_rmse(yhat, y):
    return np.sqrt(((yhat-y)**2).mean())

def calc_mae(yhat, y):
    return np.mean(abs(yhat-y))

def calc_mape(yhat, y):
    return 100*np.mean(abs((yhat-y)/y))

def eval_model(model, X_train, y_train, X_test, y_test):
    ypred = model.predict(X_test)
    ytrainpred = model.predict(X_train)

    errors_for_plot = ypred - y_test

    mae = calc_mae(ypred, y_test)
    mape = calc_mape(ypred, y_test)

    rmse_train  = calc_rmse(ytrainpred, y_train)
    rmse_test   = calc_rmse(ypred, y_test)

    print('MAE: {:0.3f}'.format(mae))
    print('MAPE: {:0.3f}'.format(mape))

    print('RMSE (train):', rmse_train.round(2))
    print('RMSE (test):', rmse_test.round(2))
    if rmse_test > rmse_train:
        print('Overfit')
    else:
        print('Underfit')

    return rmse_train, rmse_test, errors_for_plot

def get_feat_imps():

    X_train, X_test, y_train, y_test = data_for_gridsearch()
    column_names = X_train.columns

    model = RFR(max_features        = 'auto',
                max_depth           = None,
                bootstrap           = True,
                min_samples_leaf    = 5,
                min_samples_split   = 10,
                n_estimators        = 100
                )

    model = model.fit(X_train, y_train)

    model_params    = model.get_params()
    feat_imps       = model.feature_importances_

    print('model_params', model_params)
    print('feat_imps', feat_imps)

    rmse_train, rmse_test, errors_for_plot = eval_model(model, X_train, y_train, X_test, y_test)
    print('RMSE train/test: ', rmse_train, rmse_test)

    return model_params, feat_imps, column_names


if __name__ == '__main__':
    get_feat_imps()
