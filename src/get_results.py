import pandas as pd
import numpy as np
from flask import Markup

from modclass import remove_county_state as rcs

from modclass import county_data as cd
from modclass import get_data as gd
from modclass import split_data as sd
from modclass import X_y as xy
from data_processing import remove_county_state
from state_color_map import create_map as cm
from charts import create_feat_imp_chart
from data import make_fips_df as mf
from ols_model_hot_one import train_model as ols_tm
from rfr_model_hot_one import train_model as rfr_tm
from rfr_model_hot_one import predict
from svr_model_hot_one import train_model as svr_tm
from lr_model_hot_one import train_model as lr_tm
from knn_model_hot_one import train_model as knn_tm
from comparison import compare_models
from data_processing import single_county_data
from data_processing import get_state_data
from data_processing import data_for_predictions


def train_the_model():
    model = rfr_tm()

    return model

def predict(X_test):
    model = train_the_model()
    prediction = model.predict(X_test)

    return prediction


def test_predict():
    X_train, X_test, y_train, y_test = data_for_predictions()
    counties_train = X_train['county']
    counties_test = X_test['county']
    X_test, y_test = remove_county_state(X_test, y_test)
    ypred = predict(X_test)

    X = X_test.round(2)
    y = y_test.round(2)
    uninsured = X['uninsured'].values
    unemployment = X['unemployment'].values
    obesity = X['obese_adult'].values
    smokers = X['smoke_adult'].values
    particulates = X['air_poll_partic'].values
    y = y.values

    return counties_test, uninsured, unemployment, obesity, smokers, particulates, y, ypred

def test_data_preds_table():
    """returns dictionary to populate table on predictions page """
    county_tst, uninsured_tst, unemployment_tst, obesity_tst, smokers_tst, particulates_tst, y_tst, ypred = test_predict()

    # these are for the 'Actual and Predicted Asthma Rates' chart...
    county_tst = list(county_tst.str.title()),
    uninsured_tst = uninsured_tst,
    unemployment_tst = unemployment_tst,
    obesity_tst = obesity_tst,
    smokers_tst = smokers_tst,
    particulates_tst = particulates_tst,
    y_tst = y_tst,
    ypred = np.round(ypred, 2)
    num_results = len(ypred)
    v_list = []
    for i in range(num_results):
        temp_list = [uninsured_tst[0][i], unemployment_tst[0][i], obesity_tst[0][i],
        smokers_tst[0][i], particulates_tst[0][i], y_tst[0][i], ypred[i]]
        v_list.append(temp_list)
    table_dict = dict(zip(county_tst[0], v_list))

    return table_dict

def update_county_policy(row, results):
    print('row', row)
    X = row
    print('X', X)
    print('type(X)', type(X))
    print('results', results)
    results_nums = []
    for result in results:
        if result == 'plus10':
            result = 1.2
        elif result == 'minus10':
            result = 0.8
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


def get_county_pred(county, form_results):
    X, y = single_county_data(county.lower())
    row = update_county_policy(X, form_results)
    # row = row.drop(['county', 'state'], axis=1)
    pred = predict(row)
    pred = pred[0].round(2)
    y = y.values[0].round(2)

    return pred, y


def one_county(input_county):
    county = input_county.lower()
    X, y = single_county_data(county)
    X = X.round(2)
    y = y.round(2)
    uninsured = X['uninsured'].values[0]
    unemployment = X['unemployment'].values[0]
    obesity = X['obese_adult'].values[0]
    smokers = X['smoke_adult'].values[0]
    particulates = X['air_poll_partic'].values[0]
    y = y.values[0]

    return county, uninsured, unemployment, obesity, smokers, particulates, y, X

def get_state_pred_map(state, state_form_results):
    print('state'*20)
    print(state)
    state_data = get_state_data(state.lower())

    X_state = update_state_policy(state_data, state_form_results)

    X_state_counties = X_state.county
    X_state = X_state.drop(['county', 'state'], axis=1)
    state_pred_arr = predict(X_state)
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
    div_and_map = Markup(
                    '<div id="mapPrediction" class="card" style="width: 30rem;">'+
                    state_pred_map+
                    '<div class="card-body"><h2 class="card-text">Predicted</h2><p class="card-text">Map showing predicted asthma hospitalization rates by county in Colorado.  Darker colors represent higher rates.</p></div></div>'
                    )
    # print(div_and_map)
    return div_and_map

def update_state_policy(data_tuple, results):
    X = data_tuple[0]
    # X = data_tuple
    results_nums = []
    for result in results:
        if result == 'plus10':
            result = 1.2
        elif result == 'minus10':
            result = 0.8
        else:
            result = 1
        results_nums.append(result)
    X['uninsured'] *= results_nums[0]
    X['unemployment'] *= results_nums[1]
    X['obese_adult'] *= results_nums[2]
    X['smoke_adult'] *= results_nums[3]
    X['air_poll_partic'] *= results_nums[4]

    return X


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
