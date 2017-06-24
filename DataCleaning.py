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

"""The DataCleaning class:

- Takes CSV files with stage/phase information and filters them, leaving only
data with on date, time, result and phase fields
- Takes individual files for stages (with their data/time and result) and merges
into a single file for analysis

"""

import pandas as pd
from pathlib import Path
import os

# store desired fields as array
fields = ['Date', 'Time', 'Result', 'Phase']

# define path to analyse
path_list = Path('./results/phases/raw/').glob('**/*.csv')

# loop through files in the given path and store data in df
for path in path_list:
    path_in_str = str(path)
    fileName = os.path.basename(path_in_str)
    fullPath = './results/phases/raw/' + fileName
    print(fullPath)
    data = pd.read_csv(fullPath, header=0, skipinitialspace=True, usecols=fields)
    df = pd.DataFrame(data)

    # only output to CSV those which contain some data
    if df.shape[0] > 0:
        output_folder = './results/phases/processed/'
        fileName = 'clean_' + fileName

        # ensure folder exists before creating the file
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, mode=0o777)

        df.to_csv(output_folder + fileName, sep=',')

# store desired fields in an array
fields = ['Date', 'Time', 'Result', 'Phase']

# create an empty df
out_df = pd.DataFrame([])

# loop through files in the given path and store data in df
path_list = Path('./results/phases/processed/').glob('**/*.csv')
for path in path_list:
    path_in_str = str(path)
    fileName = os.path.basename(path_in_str)
    fullPath = './results/phases/processed/' + fileName
    data = pd.read_csv(fullPath, header=0, skipinitialspace=True, usecols=fields)
    df = pd.DataFrame(data)
    # append a df to contain only the relevant information in ascending order
    out_df = df.append(out_df)
    out_df = out_df.sort_values(['Date', 'Time', 'Phase'], ascending=[True, True, True])
    out_df.to_csv('./results/phases/raw/merged_phases.csv', sep=',')

# remove duplicates from the file (i.e. ensuring only one record per second)
dataset = pd.read_csv('./results/phases/raw/merged_phases.csv', header=0, skipinitialspace=True, usecols=fields)
dataset_df = pd.DataFrame(dataset)
dataset_df2 = dataset_df.drop_duplicates()
dataset_df2.to_csv('./results/phases/processed/clean_merged_phases.csv', sep=',', index=False)
