import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.metrics import classification_report
from sklearn.utils import shuffle

def calc_rmse(yhat, y):
    return np.sqrt(((yhat-y)**2).mean())

def calc_mae(yhat, y):
    return np.mean(abs(yhat-y))

def calc_mape(yhat, y):
    return 100*np.mean(abs((yhat-y)/y))

def eval_model(model, X_train, y_train, X_test, y_test):
    ypred = model.predict(X_test)
    ytrainpred = model.predict(X_train)

    mae = calc_mae(ypred, y_test)
    mape = calc_mape(ypred, y_test)
    accuracy = 100 - mape

    rmse_test   = calc_rmse(ypred, y_test)
    rmse_train  = calc_rmse(ytrainpred, y_train)

    print('Model Performance Indicators')
    print('MAE: {:0.3f}'.format(mae))
    print('MAPE: {:0.3f}'.format(mape))
    print('Accuracy = {:0.3f}%'.format(accuracy))

    print('RMSE (test):', rmse_test)
    print('RMSE (train):', rmse_train)
    if rmse_test > rmse_train:
        print('Overfit')
    else:
        print('Underfit')
    return accuracy


def knn_regress(data):
    # drop problematic row with zero for asthma_rate
    # data = data.drop([171])
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)

    # X = no_counties.drop('asthma_rate', axis=1)
    # X = no_counties.drop(['asthma_rate', 'ozo_mean','unemployment','uninsured','pcp','pm2_5_mean','pm2_5non_mean','pm2_5spec_mean','air_poll_partic','income_ineq', 'high_sch_grad', 'obese_adult'], axis=1)
    X = no_counties.drop(['asthma_rate', 'pm2_5_mean','pm10_mean','haps_mean','no_mean','vocs_mean','pm2_5non_mean','co_mean','pm2_5spec_mean','so_mean', 'lead_mean','income_ineq', 'high_sch_grad', 'obese_adult'], axis=1)
    y = no_counties.asthma_rate

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)

    # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
    pipeline = make_pipeline(StandardScaler(),
                             KNeighborsRegressor())

    # set hyperparameters
    hyperparameters = { 'kneighborsregressor__n_neighbors' : [20, 10, 5, 3, 2],
                        'kneighborsregressor__weights': ['uniform', 'distance'],
                       }

    # tune model via pipeline
    clf = GridSearchCV(pipeline, hyperparameters, cv=3)

    clf.fit(X_train, y_train)

    # evaluate models with test data
    pred = clf.predict(X_test)
    # print('feature importances:', clf.feature_importances_)
    print ('r2 score:',r2_score(y_test, pred))
    print ('mse:',mean_squared_error(y_test, pred))
    print('*'*20)
    print('best params:',clf.best_params_)
    print('best grid:', clf.best_estimator_)
    print('^'*20)
    eval_model(clf.best_estimator_, X_train, y_train, X_test, y_test)
    print('#'*20)

if __name__ == '__main__':
    # get data
    from combine_data import join_data as data
    data = data()
    # run k nearest neighbors model
    knn_regress(data)
