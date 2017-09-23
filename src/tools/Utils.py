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

"""The Utils class:

    - Provides functions to be used with other classes relating to data manipulation

"""
import os
import time
import pandas as pd
from Definitions import root

# grab root path from project definitions
root_path = root

# declare fields
output_fields = ['Date', 'Time', 'Result', 'Phase']


# converts the raw data (CSV file) into a data frame
def convert_raw_data_to_df(raw_data):
    raw_data = root_path + '/data/' + raw_data
    source = pd.read_csv(raw_data, header=0, skipinitialspace=True)
    source_data = pd.DataFrame(source)
    return source_data


# create folder if it doesn't exist
def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, mode=0o777)
    else:
        pass


# adds date/time fields to the detector fields (for desired results)
def get_detector_fields(cfg_file):
    cfg_file = root_path + '/config/' + cfg_file
    detector_fields = get_io_list_from_config(cfg_file)
    detector_fields.insert(0, 'Date')
    detector_fields.insert(1, 'Time')
    return detector_fields


# get the list of I/O names and IDs via a config file
def get_io_list_from_config(file):
    io_list = []

    for record in open(file):
        word = record.strip()

        # check if line starts with 'IOLine'
        if word.startswith('IOLine'):

            full_line = record.rstrip()
            entries = full_line.split(',')

            # get the I/O name
            io_record = entries[0].strip()
            io_name = io_record.split(':')[1]

            # get the I/O ID based on the number after 'IOLine'
            io_id_record = io_record.rsplit('IOLine')
            io_id = io_id_record[1].rsplit(':')
            io_id = io_id[0]

            # process as long as it has an I/O associated with the record
            if io_name is not '':
                # aggregate the record info to match the data file and append to list
                record = "I/O " + io_name + " [" + io_id + "] " + "State"
                io_list.append(record)

    return io_list


# returns the latest dataset location
def get_latest_dataset_folder():
    folder = root + '/results/'
    latest_location = max([os.path.join(folder, d) for d in os.listdir(folder)])
    return latest_location


# returns the latest generic dataset
def get_latest_dataset():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/dataset.csv'
    print("Dataset used: ", file)
    return file


# returns the latest sklearn dataset (excluding i/o)
def get_sklearn_data_with_duration():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_with_duration.csv'
    print(file)
    return file


# get data for sklearn models without i/o features
def get_sklearn_data_without_io():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_without_io.csv'
    return file


# get data for sklearn models with i/o features
def get_sklearn_data_with_io():
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_with_io.csv'
    return file


# get X and y for sklearn models, excluding date/time stamps
def get_sklearn_X_y(file, duration, datetime):
    data = pd.read_csv(file, sep=',')

    # if duration, remove 'end' and 'start' as not useful features for learning
    if duration:
        del data['End']
        del data['Start']

        if datetime:
            raise Exception('Datetime and Duration are not compatible features! Please choose one only.')

    else:
        # if date/time  = false, then remove it
        if datetime:
            # transform date into one-hot encoded features
            one_hot_encoded_date = pd.get_dummies(data['Date'])
            data = data.drop('Date', axis=1)
            data = data.join(one_hot_encoded_date)
            data = data.drop('Time', axis=1)

        else:
            del data['Date']
            del data['Time']

    X = data.drop('Result', axis=1)
    y = data.Result

    print("Dataset used: ", file)
    return X, y


# get the number of records in a CSV file
def print_number_records(file):
    df = pd.read_csv(file, sep=',')
    print("Total number of records: ", len(df))


# get current date and time
current_dt = time.strftime("%Y%m%d_%H%M%S")
results_folder = root_path + '/results/' + current_dt + '/'

# initialise raw folder
raw_output_folder = results_folder + 'phases/raw/'
