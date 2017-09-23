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

"""The CART class:

    - Implements the CART algorithm for decision trees to create model using data provided
    - Provides the score
    - Plots the data and saves to file for analysis

"""

from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from decision_tree.DT_Utils import score_dt, plot_dt, save_dt_model


# run CART algorithm for decision trees
def run_cart(X_train, X_test, y_train, y_test, output_folder):

    # initialise model
    dt_model = DecisionTreeRegressor()
    model_name = 'dt_model_standard'

    # run cross validation on model to find best parameters
    param_grid = {'max_depth': [None, 5, 10, 15, 20],
                  'min_samples_split': [2, 5, 10, 15],
                  'min_samples_leaf': [3, 5, 10, 20]
                  }
    cv_dt_model = GridSearchCV(dt_model, param_grid, n_jobs=4).fit(X_train, y_train)

    # fit models using training data
    cv_dt_model.fit(X_train, y_train)

    # predict on new (test) data and encapsulate result in data frame
    y_dt = cv_dt_model.predict(X_test)

    # get the score from the estimators
    score_dt(model_name, cv_dt_model, X_test, y_test, y_dt)

    # plot decision tree
    plot_dt(model_name, y_dt, y_test, output_folder)

    # save (pickle) model for re-use
    save_dt_model(model_name, cv_dt_model, output_folder)
