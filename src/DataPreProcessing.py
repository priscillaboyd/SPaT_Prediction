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

Extracts the data by:
- Processing a traffic simulator file in the expected CSV format
- Performing analysis and outputs the results for a state of a phase (i.e. red = 0, red/amber = 1, amber = 2
or green = 3)
using physical aspect data, outputting results to separate CSV files
- Extracting the relevant detection data and saves it to a separate CSV file

Cleans the data by:
- Taking CSV files with stage/phase information and filters them, leaving only
data with on date, time, result and phase fields
- Taking individual files for stages (with their data/time and result) and merging
into a single file for analysis

Combines the data by:
- Mergin all phase data and I/O detection data into a single file

Prepares the data for sklearn models by:
- Creating a CSV file with phase, result, duration until change of each state
- Ensures the data is suitable for sklearn (e.g. phase types are represented numerically)

"""

import pandas as pd
from pathlib import Path
import os
import time

raw_data = './data/sample_data_small.csv'
source = pd.read_csv(raw_data, header=0, skipinitialspace=True)
source_data = pd.DataFrame(source)
# ensure SUP values are removed
source_data = source_data[~source_data['Mode Stream 0'].isin(['8 - SUP '])]

# get current date and time
current_dt = time.strftime("%Y%m%d_%H%M%S")

# create folder for results
results_folder = './results/' + current_dt + '/'
if not os.path.exists(results_folder):
    os.makedirs(results_folder, mode=0o777)

# define raw output folder
raw_output_folder = results_folder + 'phases/raw/'

# store desired fields as array
phase_fields = ['Date', 'Time', 'Result', 'Phase']

# store desired fields from the processed I/O detection data as array
detector_fields = ['Date', 'Time', 'I/O ASL1 [0] State', 'I/O BSL1 [1] State', 'I/O CSL1 [2] State',
                   'I/O DSL1 [3] State', 'I/O AR1 [4] State', 'I/O AR1 [4] State',
                   'I/O SLDA05 [16] State', 'I/O SLDB10 [18] State', 'I/O SLDC02 [20] State',
                   'I/O SLDD07 [22] State',
                   'I/O MVDA05 [17] State', 'I/O MVDB10 [19] State', 'I/O MVDC02 [21] State',
                   'I/O MVDD07 [23] State',
                   'I/O PBE04 [24] State', 'I/O PBE05 [25] State', 'I/O PBF08 [30] State',
                   'I/O PBF09 [31] State', 'I/O PBF10 [32] State', 'I/O PBG01 [48] State',
                   'I/O PBG03 [49] State', 'I/O PBH06 [54] State', 'I/O PBH07 [55] State',
                   'I/O KSDE04 [26] State', 'I/O KSDE05 [28] State', 'I/O KSDF08 [33] State',
                   'I/O KSDF10 [35] State', 'I/O KSDG01 [50] State', 'I/O KSDG03 [52] State',
                   'I/O KSDH06 [56] State', 'I/O KSDH07 [58] State',
                   'I/O ONCE04 [27] State', 'I/O ONCE05 [29] State', 'I/O ONCF08 [34] State',
                   'I/O ONCF10 [36] State', 'I/O ONCG01 [51] State', 'I/O ONCG03 [53] State',
                   'I/O ONCH06 [57] State', 'I/O ONCH07 [59] State']

# create initial data frame for a given phase
def create_aspect_df(phase):
    phase_fields = ['Date', 'Time', 'Aspect 0 of Phase ' + phase + '  State',
                    'Aspect 1 of Phase ' + phase + '  State',
                    'Aspect 2 of Phase ' + phase + '  State']
    df = source_data[phase_fields]
    return df


# process aspect I/O to get red, red/amber, amber or green for a phase
def process_aspect_df(phase, df):
    aspect0 = 'Aspect 0 of Phase ' + phase + '  State'
    aspect1 = 'Aspect 1 of Phase ' + phase + '  State'
    aspect2 = 'Aspect 2 of Phase ' + phase + '  State'

    # create folder for outputs
    if not os.path.exists(raw_output_folder):
        os.makedirs(raw_output_folder, mode=0o777)

    # process red results
    red = df[(df[aspect0] == 1) &
             (df[aspect1] == 0) &
             (df[aspect2] == 0)]
    red['Result'] = '0'
    red['Phase'] = phase
    red_output_filename = phase + '_' + 'red_result_out.csv'
    red.to_csv(raw_output_folder + red_output_filename, sep=',')

    # process red/amber results
    redAmber = df[(df[aspect0] == 1) &
                  (df[aspect1] == 1) &
                  (df[aspect2] == 0)]
    redAmber['Result'] = '1'
    redAmber['Phase'] = phase
    redamber_output_filename = phase + '_' + 'redAmber_result_out.csv'
    redAmber.to_csv(raw_output_folder + redamber_output_filename, sep=',')

    # process amber results
    amber = df[(df[aspect0] == 0) &
               (df[aspect1] == 1) &
               (df[aspect2] == 0)]
    amber['Result'] = '2'
    amber['Phase'] = phase
    amber_output_filename = phase + '_' + 'amber_result_out.csv';
    amber.to_csv(raw_output_folder + amber_output_filename, sep=',')

    # process green results
    green = df[(df[aspect0] == 0) &
               (df[aspect1] == 0) &
               (df[aspect2] == 1)]
    green['Result'] = '3'
    green['Phase'] = phase
    green_output_filename = phase + '_' + 'green_result_out.csv'
    green.to_csv(raw_output_folder + green_output_filename, sep=',')

    # process errors (do not write to file)
    error = df[(df[aspect0] == 0) & (df[aspect1] == 0) & (df[aspect2] == 0)]


# extracts phase data from the dataset
def load_phase_data():
    phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    print("Loading phase data...")
    # iterate over phases to get stats
    for i in range(len(phase_list)):
        phase = phase_list[i]
        df_phase = create_aspect_df(phase)
        process_aspect_df(phase, df_phase)
        print("Phase " + phase + " extracted!")


# create initial data frame for detectors
def create_io_df():
    df = source_data[detector_fields]
    return df


# extracts detection data from the dataset
def load_io_data():
    print("Loading I/O data...")
    data = create_io_df()

    # create folder for results
    io_output_folder = results_folder + 'io/'
    if not os.path.exists(io_output_folder):
        os.makedirs(io_output_folder, mode=0o777)

    # process results
    io_output_filename = 'io_' + 'out.csv'
    data.to_csv(io_output_folder + io_output_filename, sep=',')
    print("I/O data extracted!")


# initialises the data extraction processes
def data_extract():
    load_phase_data()
    load_io_data()


# filter phase data to ensure only desired fields are applied
def filter_phase_data():
    # path to analyse
    path_list = Path(raw_output_folder).glob('**/*.csv')

    print("Filtering phase data...")
    # loop through files in the given path and store desired fields as array
    for path in path_list:
        path_in_str = str(path)
        file_name = os.path.basename(path_in_str)
        full_path = results_folder + 'phases/raw/' + file_name
        data = pd.read_csv(full_path, header=0, skipinitialspace=True, usecols=phase_fields)
        df = pd.DataFrame(data)

        # only output to CSV those which contain some data
        if df.shape[0] > 0:
            output_folder = results_folder + 'phases/processed/'
            file_name = 'clean_' + file_name

            # ensure folder exists before creating the file
            if not os.path.exists(output_folder):
                os.makedirs(output_folder, mode=0o777)

            df.to_csv(output_folder + file_name, sep=',')
    print("Phase data filtered!")


# combines data from processed/filtered data to a single file
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
        data = pd.read_csv(full_path, header=0, skipinitialspace=True, usecols=phase_fields)
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
                                     skipinitialspace=True, usecols=phase_fields)
    df = pd.DataFrame(merged_phases_data)
    clean_df = df.drop_duplicates()
    clean_df.to_csv(results_folder + 'phases/processed/clean_merged_phases.csv', sep=',', index=False)
    print("Duplicates removed!")


# run data cleaning processes
def data_cleaning():
    filter_phase_data()
    combine_phase_data()
    remove_duplicates_phase_data()


# combine all data into single file
def data_merge():
    print("Merging final data...")
    # load files that contain phase and I/O processed data and store as dfs
    phase_data = pd.read_csv(results_folder + 'phases/processed/clean_merged_phases.csv', header=0,
                             skipinitialspace=True, usecols=phase_fields)
    detection_data = pd.read_csv(results_folder + 'io/io_out.csv', header=0, skipinitialspace=True,
                                 usecols=detector_fields)
    phase_df = pd.DataFrame(phase_data)
    detection_df = pd.DataFrame(detection_data)

    # merge the two files based on their Date and Time fields
    output = pd.merge(phase_df, detection_df, on=['Date', 'Time'])

    # store the output with any duplicates dropped and create a final CSV file
    merged_data = output.drop_duplicates()
    merged_data.to_csv(results_folder + 'dataset.csv', sep=',', index=False)
    print("Data merged!")
    print("Final dataset available: " + results_folder + 'dataset.csv')
    return results_folder + 'dataset.csv'


def sklearn_data_processing(dataset):
    # select fields that we want to use for data frame
    fields = ['Date', 'Time', 'Result', 'Phase']

    # load data and parse date/time to a single Date_Time column
    phase_data = pd.read_csv(dataset, header=0, skipinitialspace=True, usecols=fields, parse_dates=[['Date', 'Time']])
    df = pd.DataFrame(phase_data)

    # load list of phases and states
    phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    new_columns = ['Phase', 'Result', 'Start', 'End', 'Duration']
    df_new_columns = pd.DataFrame(columns=new_columns)

    # write file for the first time with header
    df_new_columns.to_csv(results_folder + 'sklearn_dataset.csv', sep=',', index=False, mode='w')

    # loop through phases
    for x in range(len(phase_list)):
        phase = phase_list[x]

        # create a df for phase A only
        df2 = df[df['Phase'] == phase]

        print("Preparing data...")
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
                duration = pd.Timedelta(df_end - df_start).seconds

                # if the time is the same, force duration = 1
                if duration == 86399.0:
                    df_end = df_start
                    duration = 1.0

                # convert phase ID to int (to cater for scikit-learn requirements)
                phase_value = str(x)

                # write new row to data frame
                new_row = [phase_value, current_result, df_start, df_end, duration]
                df_new_columns.loc[(len(df_new_columns))] = new_row

                # go to the next result and start time
                current_result = df2['Result'].values[i]
                start_time = df2['Date_Time'].values[i]

        print(df_new_columns)

    # write result further to csv
    df_new_columns.to_csv(results_folder + 'sklearn_dataset.csv', sep=',', index=False,
                          header=False, mode='a')
    print("Prepared dataset available: " + results_folder + "sklearn_dataset.csv")


# main function runs extract, clean and merge data processes
if __name__ == '__main__':
    # extract, clean and merge data
    data_extract()
    data_cleaning()
    merged_data = data_merge()

    # process data to use with scikit-learn models
    sklearn_data_processing(merged_data)

