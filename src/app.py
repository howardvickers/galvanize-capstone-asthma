from flask import Flask, request, render_template
import flask
from flask_bootstrap import Bootstrap

import pickle
import pandas as pd
import numpy as np
import requests
import os

from modclass import county_data
from modclass import train_model as tm
from modclass import get_data as gd
from modclass import split_data as sd
from modclass import X_y as xy
from modclass import remove_county_state as rcs
from state_color_map import create_map as cm
from charts import chart_feature_importances


app = Flask(__name__)

def train_predict(X_test):
    model = tm()
    prediction = model.predict(X_test)
    return prediction

def test_predict():
    data = gd()
    X_train, X_test, y_train, y_test = sd(data)
    counties_train = X_train['county']
    counties_test = X_test['county']
    # states_train = X_train['state']
    # states_test = X_test['state']
    X_test, y_test = rcs(X_test, y_test)
    ypred = train_predict(X_test)

    X = X_test.round(2)
    y = y_test.round(2)
    uninsured = X['uninsured'].values
    unemployment = X['unemployment'].values
    obesity = X['obese_adult'].values
    smokers = X['smoke_adult'].values
    particulates = X['air_poll_partic'].values
    y = y.values

    return counties_test, uninsured, unemployment, obesity, smokers, particulates, y, ypred

def state_data(state):
    data = gd()
    co_data = data.loc[data['state']==state.lower()]
    X_co, y_co = xy(co_data)
    return X_co, y_co

def one_county(input_county):
    county = input_county.lower()
    X, y = county_data(county)
    X = X.round(2)
    y = y.round(2)
    # county = X['county']
    # state = X['state']
    uninsured = X['uninsured'].values[0]
    unemployment = X['unemployment'].values[0]
    obesity = X['obese_adult'].values[0]
    smokers = X['smoke_adult'].values[0]
    particulates = X['air_poll_partic'].values[0]
    y = y.values[0]
    print('Here is X:',X)
    return county, uninsured, unemployment, obesity, smokers, particulates, y, X

def convert_to_row(results, county):
    print('results', results)
    _, _, _, _, _, _, _, X = one_county(county)
    X = X.drop(['county', 'state'], axis=1)
    print('And here is X after dropping columns', X)
    X['uninsured'] = float(results[0])
    X['unemployment'] = float(results[1])
    X['obese_adult'] = float(results[2])
    X['smoke_adult'] = float(results[3])
    X['air_poll_partic'] = float(results[4])
    print(X)
    return X

def update_state_policy(X, results):

    X = X.drop(['county', 'state'], axis=1)
    X['uninsured'] *= 1.1
    X['unemployment'] *= 1
    X['obese_adult'] *= 1
    X['smoke_adult'] *= 1
    X['air_poll_partic'] *= 1
    print(X.shape)
    return X

@app.route('/', methods =['GET','POST'])
def index():
    return flask.render_template('index.html')

@app.route('/data', methods =['GET','POST'])
def data():
    chart_feature_importances()

    return flask.render_template('data.html')

@app.route('/models', methods =['GET','POST'])
def models():
    return flask.render_template('models.html')

@app.route('/statepredict', methods =['GET','POST'])
def statepredict():
    if request.method == 'POST':
        state = 'Colorado'
        # county = 'Boulder'
        # one_county(county)
        state_uninsur = request.form['state_uninsur']
        state_unemploy = request.form['state_unemploy']
        state_obs = request.form['state_obs']
        state_smok = request.form['state_smok']
        state_partic = request.form['state_partic']
        state_form_results = [state_uninsur, state_unemploy, state_obs, state_smok, state_partic]
        state_data = state_data(state)
        X_state, y_state = update_state_policy(state_form_results, state_data)
        X_state = X_state.drop(['county', 'state'], axis=1)
        state_pred = train_predict(X_state)
        state_pred = state_pred[0].round(2)

        # create map with predicted values
        state_pred_map_svg = cm(state_pred)

        # prepare embed for html
        state_pred_map = "<embed class="d-block w-100" src={} alt="Predicted Asthma Map">".format(state_pred_map_svg)

        return render_template( "predictions.html",
                                state_pred_map = state_pred_map
                                )

@app.route('/predictions', methods =['GET','POST'])
def predictions():

    input_county, uninsured, unemployment, obesity, smokers, particulates, y, X = one_county('Boulder')

    county_tst, uninsured_tst, unemployment_tst, obesity_tst, smokers_tst, particulates_tst, y_tst, ypred = test_predict()

    # these are for the 'Actual and Predicted Asthma Rates' chart...
    num_results = 10
    county_tst = list(county_tst.str.title()),
    # states_tst = states_tst,
    uninsured_tst = uninsured_tst,
    unemployment_tst = unemployment_tst,
    obesity_tst = obesity_tst,
    smokers_tst = smokers_tst,
    particulates_tst = particulates_tst,
    y_tst = y_tst,
    ypred = np.round(ypred, 2)
    v_list = []
    for i in range(num_results):
        temp_list = [uninsured_tst[0][i], unemployment_tst[0][i], obesity_tst[0][i], smokers_tst[0][i], particulates_tst[0][i], y_tst[0][i], ypred[i]]
        v_list.append(temp_list)
    table_dict = dict(zip(county_tst[0], v_list))

    # these are for the 'Public Policy and Asthma' chart
    if request.method == 'POST':
        county = 'Boulder'
        one_county(county)
        new_uninsur = request.form['new_uninsur']
        new_unemploy = request.form['new_unemploy']
        new_obs = request.form['new_obs']
        new_smok = request.form['new_smok']
        new_partic = request.form['new_partic']
        form_results = [new_uninsur, new_unemploy, new_obs, new_smok, new_partic]
        row = convert_to_row(form_results, county)
        pred = train_predict(row)
        pred = pred[0].round(2)

        return render_template( "predictions.html",
                                    # these are for the 'Public Policy and Asthma' chart
                                    county = input_county,
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    table_dict = table_dict,
                                    new_y = pred
                                )

    return flask.render_template('predictions.html',
                                    # these are for the 'Public Policy and Asthma' chart
                                    county = input_county,
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    table_dict = table_dict
                                    )

@app.route('/about', methods =['GET','POST'])
def about():
    return flask.render_template('about.html')

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

    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
