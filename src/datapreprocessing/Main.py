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

"""The DataPreProcessing class:

Runs:
    - Data Extract (Generic)
    - Data Cleaning
    - Data Merge
    - Sk Learn Data Extract

"""

from datapreprocessing.Clean import data_cleaning
from datapreprocessing.Extract import data_extract
from datapreprocessing.ExtractSkLearn import sklearn_data_processing
from datapreprocessing.Merge import data_merge
from datapreprocessing.Utils import get_results_folder, get_output_fields, get_detector_fields

raw_data = '20170821_2.csv'
cfg_file = 'e80374.8SD'

# create folder for results
results_folder = get_results_folder()

# declare fields
output_fields = get_output_fields()
detector_fields = get_detector_fields(cfg_file)

if __name__ == '__main__':
    # extract, clean and merge data
    data_extract(raw_data, cfg_file)
    data_cleaning()
    merged_data = data_merge(results_folder, output_fields, detector_fields)

    # # process data to use with scikit-learn models
    sklearn_data_processing(merged_data, results_folder)
