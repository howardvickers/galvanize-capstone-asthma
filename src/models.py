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

def all_regress(data):
    # drop problematic row with zero for asthma_rate
    # data = data.drop([171])
    # replacing nans with zeros
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate

    # consider replacing nans with mean (previously tried)...
    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)

    hyperpara_dict = {  LR  : {}, # use defaults only
                        RFR : { 'randomforestregressor__max_features' : ['auto' ],
                                'randomforestregressor__max_depth': [None, 5],
                                'randomforestregressor__bootstrap': [True],
                                'randomforestregressor__min_samples_leaf': [ 5],
                                'randomforestregressor__min_samples_split': [10],                                    'randomforestregressor__n_estimators': [10, 50, 100, 150]
                                },
                        KNR : { 'kneighborsregressor__n_neighbors' : [10],
                                'kneighborsregressor__weights': ['uniform', ],
                                },
                        SVR : { 'svr__kernel': ['linear'],
                                'svr__C': [10]
                                }
                        }

    # add boosting and elasticnet
    models = [LR, RFR, KNR, SVR]
    for model in models:

        # data preprocessing (removing mean and scaling to unit variance with StandardScaler)
        pipeline = make_pipeline(   StandardScaler(),
                                    model()
                                 )

        hyperparameters = hyperpara_dict[model]

        clf = GridSearchCV(pipeline, hyperparameters, cv=3) # cv=3 is same as cv=None (default)

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

    X_train = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train)
    results = model.fit()
    print(results.summary())

if __name__ == '__main__':
    csv_file_path = '../data/the_data_file.csv'
    if os.path.exists(csv_file_path):
        print("Data file found, loading data...")
        with open(csv_file_path, "r") as f:
            data = pd.read_csv(f)

    else:
        print("Data file not found, assembling dataset...")
        from combine_data import join_data as data
        from data import join_data as data
        data = data()
        data.to_csv(csv_file_path)

    all_regress(data)
