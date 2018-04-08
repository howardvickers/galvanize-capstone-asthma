from flask import Flask, request, render_template
import flask
import pickle
import pandas as pd
import numpy as np
import requests
import os
from modclass import county_data
from modclass import train_model as tm
from modclass import get_data as gd
from modclass import split_data as sd
from modclass import remove_county_state as rcs

from flask_bootstrap import Bootstrap
# from model import chart_feature_importances as make_chart

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
    return county, uninsured, unemployment, obesity, smokers, particulates, y


@app.route('/data', methods =['GET','POST'])
def data():
    chart_feature_importances()

    return flask.render_template('data.html')


@app.route('/predictions', methods =['GET','POST'])
def predictions():

    input_county, uninsured, unemployment, obesity, smokers, particulates, y = one_county('Boulder')

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



    new_uninsur = int(request.form['new_uninsur'])
    new_unemploy = int(request.form['new_unemploy'])
    new_obs = int(request.form['new_obs'])
    new_smok = int(request.form['new_smok'])
    new_partic = int(request.form['new_partic'])
    # y_new = result['object_id'][0] # change this
    print('This is from the website:', new_uninsur, new_unemploy, new_obs, new_smok, new_partic)


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



                              # county = input_county,
                              # state = state,
                                  uninsured = uninsured,
                                  unemployment = unemployment,
                                  obesity = obesity,
                                  smokers = smokers,
                                  particulates = particulates,
                              # y = y
                              )


@app.route('/', methods =['GET','POST'])
def index():

    return flask.render_template('index.html')


@app.route('/models', methods =['GET','POST'])
def models():

    return flask.render_template('models.html')


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
    # from data import join_data as data
    # data = data()
    # data.to_csv(csv_file_path, index=False)

    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
