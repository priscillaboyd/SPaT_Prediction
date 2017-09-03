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

"""The Main class is responsible for running methods to:

    - Extract data from a given CSV file with historic traffic information
    - Clean data as part of pre-processing for machine learning
    - Merge data into a single file for manipulation
    - Adapt to be used with the scikit-learn framework

"""
from preprocessing.Analysis import run_analysis
from preprocessing.Clean import clean
from preprocessing.Extract import extract
from preprocessing.ExtractSkLearn import sklearn_data_processing
from preprocessing.Merge import data_merge
from preprocessing.Utils import get_detector_fields

raw_data = '30min.csv'
cfg_file = 'e80374.8SD'

if __name__ == '__main__':
    # extract and clean data
    extract(raw_data, cfg_file)
    clean()

    # merge data with the detector fields in the config file
    detector_fields = get_detector_fields(cfg_file)
    merged_data = data_merge(detector_fields)

    # process merged data further to use with scikit-learn models
    sklearn_data_processing(merged_data)

    # run data analysis and produce necessary graphs
    run_analysis()