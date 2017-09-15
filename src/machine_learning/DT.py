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

"""The DT class:

    - Implements the CART algorithm for decision trees

"""
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import export_graphviz
from matplotlib import pyplot as plt
from tools.Utils import get_sklearn_data_with_duration, get_sklearn_X_y, get_sklearn_data_with_io, \
    get_sklearn_data_without_io


# implement CART
def run_cart():
    data = get_sklearn_data_without_io()

    # split data into training / test (20% for test)
    X, y = get_sklearn_X_y(data, duration=False, datetime=False)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, shuffle=False)

    # create decision tree model
    dt_model = GradientBoostingRegressor(min_samples_leaf=3, max_depth=None, learning_rate=0.05)
    # rf_model = RandomForestRegressor(n_estimators=200, verbose=0, min_samples_leaf=3, max_depth=20)

    # fit models using training data
    dt_model.fit(X_train, y_train)
    # rf_model.fit(X_train, y_train)

    # expose to tree graphviz format for analysis
    # folder = get_latest_dataset_folder()
    # out_file_location = folder + "/dt_tree.dot"
    # export_graphviz(dt_model, out_file=out_file_location, feature_names=X_train.columns)

    # predict on new (test) data and encapsulate result in data frame
    y_dt = dt_model.predict(X_test)
    # y_rf = rf_model.predict(X_test)

    # get the score from the estimators
    score = dt_model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_dt)
    print("MSE (DT): %.4f" % mse)
    print("Total score (DT):", score)

    # score2 = rf_model.score(X_test, y_test)
    # mse2 = mean_squared_error(y_test, y_rf)
    # print("MSE (RF): %.4f" % mse2)
    # print("Total score (RF):", score2)

    # # find the best params for the boosted DT
    # param_grid = {'max_depth': [None, 5, 10, 15, 20],
    #               'min_samples_leaf': [3, 5, 10, 20],
    #               'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.5]
    #               }
    # gs_dt = GridSearchCV(dt_model, param_grid, n_jobs=4).fit(X_train, y_train)
    # print("Best params (DT):", gs_dt.best_params_)

    # plot for visualisation
    plt.scatter(y_dt, y_test, label='Duration')
    plt.title('Boosted Decision Tree')
    plt.plot([0, 1], [0, 1], '--k', transform=plt.gca().transAxes)
    plt.xlabel('y_dt')
    plt.ylabel('y_test')
    plt.legend()
    plt.show()

    # # plot the second one for visualisation
    # plt.scatter(y_rf, y_test, label='Duration')
    # plt.title('Random Forest')
    # plt.plot([0, 1], [0, 1], '--k', transform=plt.gca().transAxes)
    # plt.xlabel('y_rf')
    # plt.ylabel('y_test')
    # plt.legend()
    # plt.show()

# main function runs data processing for decision trees
if __name__ == '__main__':
    run_cart()
