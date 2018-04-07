from flask import Flask, request, render_template
import flask
import pickle
import pandas as pd
import numpy as np
import requests
import os
from modclass import *

from flask_bootstrap import Bootstrap
# from model import chart_feature_importances as make_chart

from charts import chart_feature_importances

app = Flask(__name__)


# def get_feat_imps_plot(data):
#     make_chart(data)


@app.route('/policy', methods =['GET','POST'])
def policy():

    new_uninsur = int(request.form['new_uninsur'])
    new_unemploy = int(request.form['new_unemploy'])
    new_obs = int(request.form['new_obs'])
    new_smok = int(request.form['new_smok'])
    new_partic = int(request.form['new_partic'])
    y_new = result['object_id'][0] # change this



    return flask.render_template('policy.html',
                              county = input_county,
                              # state = state,
                              uninsured = uninsured,
                              unemployment = unemployment,
                              obesity = obesity,
                              smokers = smokers,
                              particulates = particulates,
                              y = y
                              )


@app.route('/', methods =['GET','POST'])
def index():
    # get_feat_imps_plot(data)
    chart_feature_importances()

    input_county = 'Boulder'
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









    # return render_template('index.html')
    return flask.render_template('index.html',
                                  county = input_county,
                                  # state = state,
                                  uninsured = uninsured,
                                  unemployment = unemployment,
                                  obesity = obesity,
                                  smokers = smokers,
                                  particulates = particulates,
                                  y = y
                                  )



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

    # model = get_fraud_classifier('data/data.json', 'pickle.pkl')
    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
