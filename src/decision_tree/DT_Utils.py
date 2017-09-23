# Copyright 2017 Priscilla Boyd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""The DT_Util class:

    -  Provides helper functions for DT algorithm implementation, model creation and analysis

"""
import pickle
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error


# generate MSE and accuracy score
from tools.Utils import create_folder_if_not_exists


def score_dt(model_name, model, X, y, y_actual):
    print("Scoring model...")
    model_score = model.score(X, y)
    mse = mean_squared_error(y, y_actual)
    print(model_name, "- Mean Squared Error:", mse)
    print(model_name, "- Accuracy score (%):", "{:.2%}".format(model_score))
    #TODO: Save score to file


# plot decision tree, y (test) vs y (actual)
def plot_dt(model_name, y_actual, y_test, output_folder):

    # initialise plot path
    path = output_folder + '/models'
    create_folder_if_not_exists(path)

    print("Plotting results...")
    plt.scatter(y_actual, y_test, label='Duration')
    plt.title('Decision Tree')
    plt.plot([0, 1], [0, 1], '--k', transform=plt.gca().transAxes)
    plt.xlabel('y (actual)')
    plt.ylabel('y (test)')
    plt.legend()
    # plt.show()
    plot_path = path + '/plot_' + model_name + '.png'
    plt.savefig(plot_path)
    print("Plot saved location: ", plot_path)


# save model using pickle format
def save_dt_model(model_name, model, folder):
    print("Saving model...")
    model_file = folder + '/models/' + model_name + '.pkl'
    path = open(model_file, 'wb')
    pickle.dump(model, path)
    print("Model saved location: ", model_file)


# retrieve model in pickle format
def load_dt_model(pickle_model):
    return pickle.loads(pickle_model)
