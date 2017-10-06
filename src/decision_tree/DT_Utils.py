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

"""
    The DT_Utils module provides helper functions for Decision Tree algorithms implementation, model creation and
    analysis.
"""
import pickle
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from tools.Utils import create_folder_if_not_exists


# noinspection PyTypeChecker
def score_dt(model_name, model, X, y, y_actual, output_folder):
    """
    Score a decision tree model.

    :param string model_name: title for the model used on the output filename
    :param dataframe model: model reference
    :param dataframe X: examples
    :param dataframe y: targets
    :param dataframe y_actual: target results
    :param string output_folder: location of the output / results
    """
    print("Scoring model...")
    model_score = model.score(X, y)
    mse = mean_squared_error(y, y_actual)

    mse_score = model_name, "- Mean Squared Error:", mse
    accuracy = model_name, "- Accuracy score (%):", "{:.2%}".format(model_score)

    # write to file
    path = output_folder + '/models'
    create_folder_if_not_exists(path)

    filename = path + '/score_' + model_name + '.txt'
    with open(filename, 'w') as scores:
        print(mse_score, file=scores)
        print(accuracy, file=scores)
    scores.close()
    print("Scores saved location:", filename)


def plot_dt(model_name, y_actual, y_test, output_folder):
    """
    Plot decision tree, y (training) vs y (test/actual).

    :param string model_name: title for the model used on the output filename
    :param dataframe y_actual: target results
    :param dataframe y_test: test targets
    :param string output_folder: location of the output / results
    """

    # initialise plot path
    path = output_folder + '/models'

    print("Plotting results...")
    plt.scatter(y_actual, y_test, label='Duration')
    plt.title('Decision Tree')
    plt.plot([0, 1], [0, 1], '--k', transform=plt.gca().transAxes)
    plt.xlabel('y (actual)')
    plt.ylabel('y (test)')
    plt.legend()
    plot_path = path + '/plot_' + model_name + '.png'
    plt.savefig(plot_path)
    print("Plot saved location:", plot_path)


def save_dt_model(model_name, model, folder):
    """
    Save model using Pickle binary format.

    :param dataframe model: model reference
    :param string model_name: title for the model used on the output filename
    :param string folder: location of model output
    """
    print("Saving model...")
    model_file = folder + '/models/' + model_name + '.pkl'
    path = open(model_file, 'wb')
    pickle.dump(model, path)
    print("Model saved location:", model_file)


def load_dt_model(pickle_model):
    """
    Retrieve model using Pickle binary format.

    :param string pickle_model: location of Pickle model
    :return: Pickle model for re-use
    :rtype: object
    """
    return pickle.loads(pickle_model)
