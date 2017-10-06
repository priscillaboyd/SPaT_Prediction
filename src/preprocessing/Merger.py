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
    The Merger class combines the data by merging all phase data and I/O detection data into a single data set CSV file.
"""

import pandas as pd
from tools.Utils import results_folder, output_fields


def data_merge(detector_fields):
    """
    Combine all processed data into a single dataset file.

    :param list[str] detector_fields: list of strings with detector names
    :return: location of dataset
    :rtype: string
    """
    print("Merging final data...")

    # load files that contain phase and I/O processed data and store as dfs
    phase_data = pd.read_csv(results_folder + 'phases/processed/clean_merged_phases.csv', header=0,
                             skipinitialspace=True, usecols=output_fields)
    detection_data = pd.read_csv(results_folder + 'io/io_out.csv', header=0, skipinitialspace=True,
                                 usecols=detector_fields)
    phase_df = pd.DataFrame(phase_data)
    detection_df = pd.DataFrame(detection_data)

    # merge the two files based on their Date and Time fields
    output = pd.merge(phase_df, detection_df, on=['Date', 'Time'])

    # store the output with any duplicates dropped and create a final CSV file
    merged_df = output.drop_duplicates()
    merged_df.to_csv(results_folder + 'dataset.csv', sep=',', index=False)

    print("Data merged!")
    print("Main dataset available: " + results_folder + 'dataset.csv')

    # return location of dataset
    return results_folder + 'dataset.csv'
