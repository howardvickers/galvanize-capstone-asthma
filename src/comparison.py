import pandas as pd
import numpy as np

from ols_model_hot_one import train_model as ols_tm
from rfr_model_hot_one import train_model as rfr_tm
from rfr_model_hot_one import eval_model
from svr_model_hot_one import train_model as svr_tm
from lr_model_hot_one import train_model as lr_tm
from knn_model_hot_one import train_model as knn_tm


def compare_models():
    model_dict = {  'Random Forest': rfr_tm,
                    }

    comparison_dict = {}
    for model_name, model in model_dict.items():
        _, rmse_train, rmse_test, r2score, _ = eval_model()
        comparison_dict[model_name] =  rmse_train.round(2), rmse_test.round(2), r2score.round(2)

    return comparison_dict
