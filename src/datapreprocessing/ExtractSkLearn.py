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

"""The ExtractSkLearn class prepares the data for sklearn models by:

    - Creating a CSV file with phase, result, duration until change of each state
    - Ensures the data is suitable for sklearn (e.g. phase types are represented numerically)

"""
import pandas as pd
from datapreprocessing.Utils import results_folder


# process data for scikit-learn
def sklearn_data_processing(merged_data):

    print("Creating Scikit-Learn dataset...")

    # select fields that we want to use for data frame
    fields = ['Date', 'Time', 'Result', 'Phase']

    # load data and parse date/time to a single Date_Time column
    phase_data = pd.read_csv(merged_data, header=0, skipinitialspace=True, usecols=fields, parse_dates=[['Date', 'Time']])
    df = pd.DataFrame(phase_data)

    # load list of phases and states (excluding phases E and F as they are pedestrian phases)
    phase_list = ['A', 'B', 'C', 'D']

    new_columns = ['Phase', 'Result', 'Start', 'End', 'Duration']
    df_new_columns = pd.DataFrame(columns=new_columns)

    # write file for the first time with header
    df_new_columns.to_csv(results_folder + 'sklearn_dataset.csv', sep=',', index=False, mode='w')

    # loop through phases
    for x in range(len(phase_list)):
        phase = phase_list[x]

        # create a df for phase A only
        df2 = df[df['Phase'] == phase]

        # initialise by using the very first record
        start_time = df2['Date_Time'].values[0]
        current_result = df2['Result'].values[0]

        # loop through all records from DF to process duration
        for i in range(len(df2.index)):

            # if the phase is the same, set as end time
            if df2['Result'].values[i] == current_result:
                end_time = df2['Date_Time'].values[i]

            # if the phase is no longer the same or it's the last record, use end time so far to get duration
            if df2['Result'].values[i] != current_result or i+1 == len(df2.index):
                df_start = pd.to_datetime(start_time)
                df_end = pd.to_datetime(end_time)

                # # start > end will happen if only 1 second record, so set duration = 1
                if df_start > df_end:
                    duration = 1
                else:
                    duration = pd.Timedelta(df_end - df_start).seconds

                # convert phase ID to int (to cater for scikit-learn requirements)
                phase_value = str(x)

                # write new row to data frame
                new_row = [phase_value, current_result, df_start, df_end, duration]
                df_new_columns.loc[(len(df_new_columns))] = new_row

                # go to the next result and start time
                current_result = df2['Result'].values[i]
                start_time = df2['Date_Time'].values[i]

    # write result further to csv
    df_new_columns.to_csv(results_folder + 'sklearn_dataset.csv', sep=',', index=False,
                          header=False, mode='a')

    print("Scikit-learn dataset available: " + results_folder + "sklearn_dataset.csv")
