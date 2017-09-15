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

"""The Cleaner class cleans the data by:

    - Taking CSV files with stage/phase information and filtering them, leaving date, time, result and phase fields
    - Taking individual files for stages (with data/time and result) and merging into a single file
    - Removing duplicates from the files merged

"""

import os
import pandas as pd
from pathlib import Path
from tools.Utils import create_folder_if_not_exists, output_fields, \
    raw_output_folder, results_folder


# filter phase data for files in raw data folder to ensure only desired fields are taken
def filter_phase_data():
    print("Filtering phase data...")

    # path to analyse
    path_list = Path(raw_output_folder).glob('**/*.csv')

    # loop through files in the given path and store desired fields as array
    for path in path_list:
        path_in_str = str(path)
        file_name = os.path.basename(path_in_str)
        full_path = results_folder + 'phases/raw/' + file_name
        data = pd.read_csv(full_path, header=0, skipinitialspace=True, usecols=output_fields)
        df = pd.DataFrame(data)

        # only output to CSV those which contain some data
        if df.shape[0] > 0:
            output_folder = results_folder + 'phases/processed/'
            file_name = 'clean_' + file_name

            # ensure folder exists before creating the file
            create_folder_if_not_exists(output_folder)

            # write output to a file
            df.to_csv(output_folder + file_name, sep=',')

    print("Phase data filtered!")


# combine data from processed/filtered data to a single file
def combine_phase_data():
    print("Combining phase data...")

    # create an empty data frame
    out_df = pd.DataFrame([])

    # loop through files in the given path and store data in df
    path_list = Path(results_folder + 'phases/processed/').glob('**/*.csv')
    for path in path_list:
        path_in_str = str(path)
        file_name = os.path.basename(path_in_str)
        full_path = results_folder + 'phases/processed/' + file_name
        data = pd.read_csv(full_path, header=0, skipinitialspace=True, usecols=output_fields)
        df = pd.DataFrame(data)
        # append a df to contain only the relevant information in ascending order
        out_df = df.append(out_df)
        out_df = out_df.sort_values(['Date', 'Time', 'Phase'], ascending=[True, True, True])
        out_df.to_csv(results_folder + 'phases/raw/merged_phases.csv', sep=',')

    print("Data combined!")


# remove duplicates from the file (i.e. ensuring only one record per second)
def remove_duplicates_phase_data():
    print("Removing any duplicates...")
    merged_phases_data = pd.read_csv(results_folder + 'phases/raw/merged_phases.csv', header=0,
                                     skipinitialspace=True, usecols=output_fields)
    df = pd.DataFrame(merged_phases_data)
    clean_df = df.drop_duplicates()
    clean_df.to_csv(results_folder + 'phases/processed/clean_merged_phases.csv', sep=',', index=False)
    print("Duplicates removed!")


# run data cleaning processes
def clean():
    filter_phase_data()
    combine_phase_data()
    remove_duplicates_phase_data()
