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

"""The Tools_ML class:

- Provides functions to be used with other classes relating to machine learning
data construction and retrieval

"""

import numpy as np
import pandas as pd
import os
from Definitions import root

# grab root path from project definitions
root_path = root


# returns the latest dataset location
def get_latest_dataset_folder():
    folder = root + '/results/'
    latest_location = max([os.path.join(folder, d) for d in os.listdir(folder)])
    return latest_location


# returns the latest generic dataset
def get_latest_dataset():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/dataset.csv'
    print(file)
    return file


# returns the latest sklearn dataset
def get_latest_sklearn_dataset():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset.csv'
    print(file)
    return file


# get X and y for sklearn models, excluding date/time stamps
def get_sklearn_data(file):
    data = pd.read_csv(file, usecols=['Phase', 'Result', 'Duration'], sep=',')
    X = data.drop('Result', axis=1)
    y = data.Result
    print("Dataset used: ", file)
    return X, y