import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

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



def rand_forest(data):
    # drop problematic row with zero for asthma_rate
    # data = data.drop([171])
    data_nas = data.fillna(-1)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    # X = no_counties.drop('asthma_rate', axis=1)
    X = no_counties.drop(['asthma_rate', 'pm2_5_mean','pm10_mean','haps_mean','no_mean','vocs_mean','pm2_5non_mean','co_mean','pm2_5spec_mean','so_mean', 'lead_mean','income_ineq', 'high_sch_grad', 'obese_adult'], axis=1)
    y = no_counties.asthma_rate

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)

    # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
    pipeline = make_pipeline(StandardScaler(),
                             RandomForestRegressor())

    # set hyperparameters
    hyperparameters = { 'randomforestregressor__max_features' : ['auto', 'sqrt', 'log2'],
                        'randomforestregressor__max_depth': [None, 5, 2],
                        'randomforestregressor__bootstrap': [True],
                        'randomforestregressor__min_samples_leaf': [3, 4, 5],
                        'randomforestregressor__min_samples_split': [10, 12, 15],
                        'randomforestregressor__n_estimators': [10, 50, 100, 150]
                        }

    # hyperparameters = { 'randomforestregressor__max_features' : ['auto'],
    #                     'randomforestregressor__max_depth': [None, 5, 2],
    #                     'randomforestregressor__bootstrap': [True],
    #                     'randomforestregressor__min_samples_leaf': [4],
    #                     'randomforestregressor__min_samples_split': [10],
    #                     'randomforestregressor__n_estimators': [200]
    #                     }

    # tune model via pipeline
    clf = GridSearchCV(pipeline, hyperparameters, cv=3)

    clf.fit(X_train, y_train)

    # evaluate models with test data
    pred = clf.predict(X_test)
    # print('feature importances:', clf.feature_importances_)
    print('best_estimator_.feature importances:', clf.best_estimator_.feature_importances_)
    print ('r2 score:',r2_score(y_test, pred))
    print ('mse:',mean_squared_error(y_test, pred))
    print('*'*20)
    print('best params:',clf.best_params_)
    print('best grid:', clf.best_estimator_)
    print('^'*20)
    eval_model(clf.best_estimator_, X_train, y_train, X_test, y_test)
    print('#'*20)

    # print('pipeline.steps[1]', pipeline.steps[1])
    # print('pipeline.steps[1][1].feature_importances_', pipeline.steps[1][1].feature_importances_)
    # print('pipeline.steps[0][1].get_feature_names()', pipeline.steps[0][1].get_feature_names())


if __name__ == '__main__':
    # get data
    from combine_data import join_data as data
    data = data()
    # run random forest model
    rand_forest(data)
