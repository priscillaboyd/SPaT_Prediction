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

"""The GBR class:

    - Implements the Gradient Boosted Regressor ensemble for decision trees

"""

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from decision_tree.DT_Utils import score_dt, plot_dt, save_dt_model


# run Gradient Boosting Regressor ensemble algorithm for decision trees
def run_gbr(X_train, X_test, y_train, y_test, output_folder):

    # initialise model
    gbr_model = GradientBoostingRegressor()
    model_name = 'dt_model_gbr'

    # run cross validation on model to find best parameters
    param_grid = {'max_depth': [None, 5, 10, 15, 20],
                  'learning_rate': [0.05, 0.1]
                  }
    cv_gbr_model = GridSearchCV(gbr_model, param_grid, n_jobs=4).fit(X_train, y_train)

    # fit models using training data
    cv_gbr_model.fit(X_train, y_train)

    # predict on new (test) data and encapsulate result in data frame
    y_dt = cv_gbr_model.predict(X_test)

    # get the score from the estimators
    score_dt(model_name, cv_gbr_model, X_test, y_test, y_dt, output_folder)

    # plot decision tree
    plot_dt(model_name, y_dt, y_test, output_folder)

    # save (pickle) model for re-use
    save_dt_model(model_name, cv_gbr_model, output_folder)
