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

def column_names(data):
    column_names = data.columns
    nice_labels = ['County', 'Asthma Rate', 'PM10 - Pollutant', 'PM2.5 Pollutant', 'PM2.5 non FRM Pollutant',
       'PM2.5 Spec - Pollutant', 'CO - Pollutant', 'SO2 - Pollutant', 'NO2 - Pollutant', 'Ozone - Pollutant',
       'NONOxNOy - Pollutant', 'Lead - Pollutant', 'HAPS - Pollutant', 'VOCS - Pollutant', 'State',
       'Smokers (Adult)', 'Obesity (Adult)', 'Uninsured Rate', 'PCP', 'High School Grads',
       'Unemployment', 'Income Inequality', 'Particulate Air Pollution']
    label_dict = dict(zip(column_names, nice_labels))

    return label_dict


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
    print('Model:', model)
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
    data = data.drop([141, 142, 149, 153, 158])
    # replacing nans with zeros
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    y = no_counties.asthma_rate
    print(X.columns)
    all_columns = ['pm10_mean', 'pm25_mean', 'pm25non_mean', 'pm25spec_mean', 'co_mean',
       'so2_mean', 'no2_mean', 'ozo_mean', 'nonox_mean', 'lead_mean',
       'haps_mean', 'vocs_mean', 'smoke_adult', 'obese_adult', 'uninsured',
       'pcp', 'high_sch_grad', 'unemployment', 'income_ineq', 'air_poll_partic']
    drop_columns = []
    X = X.drop(drop_columns, axis=1)

    # consider replacing nans with mean (previously tried)...
    # train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)


    hyperpara_dict = {  LR  : {}, # use defaults only
                        RFR : { 'randomforestregressor__max_features' : ['auto', 'sqrt'],
                                'randomforestregressor__max_depth': [10, None],
                                'randomforestregressor__bootstrap': [True, False],
                                'randomforestregressor__min_samples_leaf': [1, 2, 4],
                                'randomforestregressor__min_samples_split': [2, 5],
                                'randomforestregressor__n_estimators': [10, 100],
                                },
                        GBR : { 'gradientboostingregressor__n_estimators' :     [100, 600, 700, 800],
                                'gradientboostingregressor__max_depth':         [3, 4, 5, 10, 20],
                                'gradientboostingregressor__min_samples_split': [3, 4, 5, 10, 20],
                                'gradientboostingregressor__learning_rate':     [0.01, 0.05, 0.1],
                                'gradientboostingregressor__loss':              ['ls'],
                                },
                        KNR : { 'kneighborsregressor__n_neighbors' : [1, 2, 3, 4, 5, 6, 10],
                                'kneighborsregressor__weights': ['uniform', 'distance'],
                                },
                        SVR : { 'svr__kernel': ['linear', 'poly', 'sigmoid', 'rbf'],
                                'svr__C': [0.5, 5, 10, 15, 20, 50, 100, 200, 300, 500, 1000],
                                'svr__epsilon': [0.1, 1.5, 2, 5, 10, 30, 50],
                                },
                        EN : { 'elasticnet__alpha': [1,0.1,0.01,0.001], # equivalent to lambda; alpha=0 means no regularization, ie linear regression
                                'elasticnet__l1_ratio': [0.5, 0.7, 0.8, 0.9, 1], # l1=1 means L1 penalty, ie Lasso (not L2/Ridge)
                                'elasticnet__max_iter': [10000],
                                }
                        }

    # models = [LR, RFR, GBR, KNR, SVR, EN]
    models = [EN]
    # mod_dict = {RFR:'rfr'}
    # best_params_dict = {}
    # for model, tag in mod_dict.items():
    #     print('MODEL '*12)
    #     print(model)
    #     print(tag)

    print('Check if any y_train zeros:', y_train[y_train==0])
    print('Check if any y_test zeros:', y_test[y_test==0])
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
        # print ('r2 score:',r2_score(y_test, pred))
        # print ('mse:',mean_squared_error(y_test, pred))
        print('*'*20)
        print('best params:',clf.best_params_)
        print('best grid:', clf.best_estimator_)
        print('X_test-y_test Score: ', clf.score(X_test, y_test))
        print('^'*20)
        eval_model(clf.best_estimator_, X_train, y_train, X_test, y_test)
        # print('#'*20)

    #     best_params_dict[tag] = clf.best_params_
    # print('BEST PARAMS '*10)
    #
    # print('best_params_dict', best_params_dict)
    # print('END PARAMS '*10)



    # mod = RFR(  max_features        = best_params_dict[tag]['randomforestregressor__max_features'],
    #             max_depth           = best_params_dict[tag]['randomforestregressor__max_depth'],
    #             bootstrap           = best_params_dict[tag]['randomforestregressor__bootstrap'],
    #             min_samples_leaf    = best_params_dict[tag]['randomforestregressor__min_samples_leaf'],
    #             min_samples_split   = best_params_dict[tag]['randomforestregressor__min_samples_split']
    #             )
    #
    #
    # mod.fit(X_train, y_train)
    # print('get_params()'*20)
    # print(mod.get_params())
    # mod.predict(X_test)
    # print(mod.feature_importances_)


    # from data import column_names as cols
    # col_dict = column_names(data)
    # imps, names = zip(*sorted(zip(mod.feature_importances_, [col_dict.get(x, x) for x in X_train.columns])))

    # plt.style.use('bmh')
    # plt.style.use('seaborn-deep')
    # plt.style.use('seaborn-dark-palette')
    # plt.style.use('seaborn-notebook')
    # plt.style.use('seaborn-pastel')
    # plt.style.use('ggplot')

    # fig = plt.figure()
    # plt.axis([0, 0.4, 0, 1])
    # plt.barh(range(len(names)), imps, align='center')
    # plt.yticks(range(len(names)), names)
    # plt.xlabel('Relative Importance of Features', fontsize=18)
    # plt.ylabel('Features', fontsize=18)
    # plt.title('Which Factors Drive Asthma Rates?', fontsize=24)
    #
    # plt.tight_layout()
    # plt.show()
    # plt.savefig('../saved_images/feat_imps.png')


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
        # from combine_data import join_data as data
        from data import join_data as data
        data, labels = data()
        data.to_csv(csv_file_path, index=False)
    # from data import join_data as data
    # data = data()
    # data.to_csv(csv_file_path, index=False)

    all_regress(data)
