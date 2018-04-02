import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

def rand_forest(data):
    data_nas = data.fillna(0)
    no_counties = data_nas.drop(['county', 'state'], axis=1)
    X = no_counties.drop('asthma_rate', axis=1)
    # X = no_counties.drop(['asthma_rate', 'ozo_mean','unemployment','uninsured','pcp','pm2_5_mean','pm2_5non_mean','pm2_5spec_mean','air_poll_partic','income_ineq', 'high_sch_grad', 'obese_adult'], axis=1)
    y = no_counties.asthma_rate

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=123)

    # Data preprocessing
    pipeline = make_pipeline(preprocessing.StandardScaler(),
                             RandomForestRegressor(n_estimators=100))

    # Hyperparameters to tune
    hyperparameters = { 'randomforestregressor__max_features' : ['auto', 'sqrt', 'log2'],
                      'randomforestregressor__max_depth': [None, 5, 3, 1]}

    # Tune model via pipeline
    clf = GridSearchCV(pipeline, hyperparameters, cv=10)

    clf.fit(X_train, y_train)

    # Evaluate models with test data
    pred = clf.predict(X_test)
    print('feature importances:', clf.feature_importances_)
    print ('r2 score:',r2_score(y_test, pred))
    print ('mse:',mean_squared_error(y_test, pred))

if __name__ == '__main__':
    # get data
    from combine_data import join_data as data
    data = data()
    # run random forest model
    rand_forest(data)
