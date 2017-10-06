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
    The Main module creates the decision tree models, initialises the data and runs them to obtain the scores.
"""

from sklearn.model_selection import train_test_split
from decision_tree.CART import run_cart
from decision_tree.GBR import run_gbr
from tools.Utils import get_sklearn_data_with_duration, get_latest_dataset_folder, get_sklearn_X_y

# retrieve data
data = get_sklearn_data_with_duration()
X, y = get_sklearn_X_y(data, duration=True, datetime=False)

# split data into training / test (20% for test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, shuffle=False)

# define output folder for results
output_folder = get_latest_dataset_folder()

if __name__ == '__main__':
    run_cart(X_train, X_test, y_train, y_test, output_folder)
    run_gbr(X_train, X_test, y_train, y_test, output_folder)
