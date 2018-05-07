from flask import Flask, request, render_template
import flask
from flask_bootstrap import Bootstrap
from flask import Markup

import pandas as pd
import numpy as np
import requests
import os

from state_color_map import create_map as cm
from data import make_fips_df as mf
from ols_model_hot_one import train_model as ols_tm
from rfr_model_hot_one import train_model as rfr_tm
from svr_model_hot_one import train_model as svr_tm
from lr_model_hot_one import train_model as lr_tm
from knn_model_hot_one import train_model as knn_tm
from comparison import compare_models
from get_results import test_data_preds_table
from get_results import get_county_pred
from get_results import one_county
from get_results import get_state_pred_map
from charts import create_feat_imp_chart

app = Flask(__name__)

@app.route('/', methods =['GET','POST'])
def index():
    return flask.render_template('index.html')

@app.route('/data', methods =['GET','POST'])
def data():
    create_feat_imp_chart()

    return flask.render_template('data.html')

@app.route('/models', methods =['GET','POST'])
def models():
    ols_results = ols_tm()
    ols_summary = Markup(ols_results)

    comparison_dict = compare_models()

    return flask.render_template(
                                'models.html',
                                ols_results = ols_summary,
                                model_comparison_dict = comparison_dict
                                )

@app.route('/state', methods =['GET','POST'])
def state():
    if request.method == 'POST':
        state = 'Colorado'
        state_form_results = [  request.form['state_uninsur'],
                                request.form['state_unemploy'],
                                request.form['state_obs'],
                                request.form['state_smok'],
                                request.form['state_partic']
                              ]
        print('state_form_results', state_form_results)
        div_and_map = get_state_pred_map(state, state_form_results)

        return flask.render_template( "state.html",
                                state_pred_map = div_and_map
                                )

    return flask.render_template('state.html')


@app.route('/county', methods =['GET','POST'])
def county():
    county = 'Adams'
    input_county, uninsured, unemployment, obesity, smokers, particulates, y, X = one_county(county)

    # these are for the 'Public Policy and Asthma' chart
    if request.method == 'POST':
        """takes in policy changes and returns single county's prediction under policy changes"""

        form_results = [request.form['new_uninsur'],
                        request.form['new_unemploy'],
                        request.form['new_obs'],
                        request.form['new_smok'],
                        request.form['new_partic']
                        ]

        pred, y = get_county_pred(county, form_results)

        return render_template( "county.html",
                                    county = input_county.title(),
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    new_y = pred,
                                )

    return flask.render_template('county.html',
                                    county = input_county.title(),
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    )

@app.route('/predictions', methods =['GET','POST'])
def predictions():

    table_dict = test_data_preds_table()

    return flask.render_template('predictions.html',
                                    table_dict = table_dict
                                    )

@app.route('/about', methods =['GET','POST'])
def about():
    return flask.render_template('about.html')

if __name__ == '__main__':

    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
