from flask import Flask, request, render_template
import flask
from flask_bootstrap import Bootstrap
from flask import Markup

import pandas as pd
import numpy as np
import requests
import os

from modclass import county_data as cd
from modclass import train_model as tm
from modclass import get_data as gd
from modclass import split_data as sd
from modclass import X_y as xy
from modclass import remove_county_state as rcs
from state_color_map import create_map as cm
from charts import chart_feature_importances
from data import make_fips_df as mf

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

def get_state_data(state):
    data = gd()
    co_data = data.loc[data['state']==state.lower()]
    X_co, y_co = xy(co_data)
    return X_co, y_co

def one_county(input_county):
    county = input_county.lower()
    X, y = cd(county)
    X = X.round(2)
    y = y.round(2)
    uninsured = X['uninsured'].values[0]
    unemployment = X['unemployment'].values[0]
    obesity = X['obese_adult'].values[0]
    smokers = X['smoke_adult'].values[0]
    particulates = X['air_poll_partic'].values[0]
    y = y.values[0]
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
    return X

def update_state_policy(data_tuple, results):
    X = data_tuple[0]
    results_nums = []
    for result in results:
        if result == 'plus10':
            result = 1.1
        elif result == 'minus10':
            result = 0.9
        else:
            result = 1
        results_nums.append(result)
    X['uninsured'] *= results_nums[0]
    X['unemployment'] *= results_nums[1]
    X['obese_adult'] *= results_nums[2]
    X['smoke_adult'] *= results_nums[3]
    X['air_poll_partic'] *= results_nums[4]
    return X


def update_county_policy(row, results):
    print('row', row)
    X = row
    print('X', X)
    print('type(X)', type(X))
    print('results', results)
    results_nums = []
    for result in results:
        if result == 'plus10':
            result = 1.1
        elif result == 'minus10':
            result = 0.9
        else:
            result = 1
        results_nums.append(result)
    print('results_nums', results_nums)
    X['uninsured'] *= results_nums[0]
    X['unemployment'] *= results_nums[1]
    X['obese_adult'] *= results_nums[2]
    X['smoke_adult'] *= results_nums[3]
    X['air_poll_partic'] *= results_nums[4]
    print('updated X', X)
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
        state_data = get_state_data(state)
        X_state = update_state_policy(state_data, state_form_results)
        X_state_counties = X_state.county
        X_state = X_state.drop(['county', 'state'], axis=1)
        X_state = X_state.fillna(0)
        state_pred_arr = train_predict(X_state)
        state_pred_arr = state_pred_arr.round(2)

        df_state_pred = pd.DataFrame(state_pred_arr)
        df_state_pred.columns = ['pred']
        df_X_state_counties = pd.DataFrame(X_state_counties)
        df_X_state_counties = df_X_state_counties.reset_index(drop=True)
        county_state_pred = df_state_pred.join(df_X_state_counties)

        fips = mf()
        fips_state = fips[fips['state']==state.lower()]

        pred_fips = county_state_pred.merge(fips_state, how="left", on="county")
        pred_fips = pred_fips.drop(['county', 'state'], axis=1)

        # create map with predicted values
        state_pred_map_svg = cm(pred_fips)

        # prepare embed for html
        dub = '"'
        state_pred_map = '<embed class="d-block w-100" src={}{}{} alt="Predicted Asthma Map">'.format(dub, state_pred_map_svg, dub)
        value = Markup(
                        '<div id="mapPrediction" class="card" style="width: 30rem;">'+
                        state_pred_map+
                        '<div class="card-body"><h2 class="card-text">Predicted</h2><p class="card-text">Map showing predicted asthma hospitalization rates by county in Colorado.  Darker colors represent higher rates.</p></div></div>'
                        )

        return flask.render_template( "state.html",
                                state_pred_map = value
                                )

    return flask.render_template('state.html')


@app.route('/county', methods =['GET','POST'])
def county():
    input_county, uninsured, unemployment, obesity, smokers, particulates, y, X = one_county('Boulder')

    # these are for the 'Public Policy and Asthma' chart
    if request.method == 'POST':
        county = 'Boulder'
        # one_county(county)
        # update_county_policy
        form_results = [request.form['new_uninsur'],
                        request.form['new_unemploy'],
                        request.form['new_obs'],
                        request.form['new_smok'],
                        request.form['new_partic']
                        ]

        X, y = cd(county.lower())

        row = update_county_policy(X, form_results)
        row = row.drop(['county', 'state'], axis=1)

        pred = train_predict(row)
        pred = pred[0].round(2)

        y = y.values[0].round(2)


        return render_template( "county.html",
                                    # these are for the 'Public Policy and Asthma' chart
                                    county = input_county.title(),
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    new_y = pred,
                                )

    # return flask.render_template('county.html')
    return flask.render_template('county.html',
                                    # these are for the 'Public Policy and Asthma' chart
                                    county = input_county.title(),
                                    uninsured = uninsured,
                                    unemployment = unemployment,
                                    obesity = obesity,
                                    smokers = smokers,
                                    particulates = particulates,
                                    y = y,
                                    # table_dict = table_dict
                                    )


@app.route('/predictions', methods =['GET','POST'])
def predictions():

    input_county, uninsured, unemployment, obesity, smokers, particulates, y, X = one_county('Boulder')

    county_tst, uninsured_tst, unemployment_tst, obesity_tst, smokers_tst, particulates_tst, y_tst, ypred = test_predict()

    # these are for the 'Actual and Predicted Asthma Rates' chart...
    num_results = 10
    county_tst = list(county_tst.str.title()),
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
        # data, labels = data()
        data = data()
        data.to_csv(csv_file_path, index=False)

    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
