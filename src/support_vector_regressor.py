import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.metrics import classification_report
from sklearn.utils import shuffle

def eval_model(model, X_test, y_test):
    ypred = model.predict(X_test)
    MAPE = 100 * np.mean(abs(ypred - y_test) / (y_test+.001)) # added 0.001 to prevent zeros
    accuracy = 100 - MAPE
    print('Model Performance Indicators')
    print('Average Error: {:0.3f} degrees.'.format(np.mean(abs(ypred - y_test))))
    print('Accuracy = {:0.3f}%.'.format(accuracy))

    return accuracy


def sup_vec_regress(data):
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    # X = no_counties.drop(['asthma_rate', 'ozo_mean','unemployment','uninsured','pcp','pm2_5_mean','pm2_5non_mean','pm2_5spec_mean','air_poll_partic','income_ineq', 'high_sch_grad', 'obese_adult'], axis=1)
    y = no_counties.asthma_rate

    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)

    # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
    pipeline = make_pipeline(StandardScaler(),
                             SVR())

    # set hyperparameters
    # hyperparameters =  [{'kernel': ['rbf'],
    #                     'gamma': [1e-4, 1e-3, 0.01, 0.1, 0.2, 0.5],
    #                     'C': [0.1, 1, 10, 100, 1000]},
    #                     {'kernel': ['linear'],
    #                     'C': [1, 10, 100, 1000]}
    #                     ]

    hyperparameters = { 'svr__kernel': ['linear', 'rbf'],
                        'srv__C': [0.1, 1, 10, 100, 1000]
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
    eval_model(clf.best_estimator_, X_test, y_test)
    print('#'*20)

if __name__ == '__main__':
    # get data
    from combine_data import join_data as data
    data = data()
    # run suport vector regression model
    sup_vec_regress(data)
