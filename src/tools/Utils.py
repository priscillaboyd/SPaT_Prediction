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
    The Utils module provides helper functions to be used with other classes relating to data manipulation.
"""

import os
import time
import pandas as pd

# grab root path from project definitions
root_path = os.path.dirname(os.path.abspath('../'))

# declare fields
output_fields = ['Date', 'Time', 'Result', 'Phase']


def convert_raw_data_to_df(raw_data):
    """
    Converts CSV-formatted raw data into a Pandas data frame

    :param string raw_data: location of CSV-formatted raw data
    :return: Data as dataframe
    :rtype: dataframe
    """

    # read CSV file
    raw_data = root_path + '/data/' + raw_data
    source = pd.read_csv(raw_data, header=0, skipinitialspace=True)
    source_data = pd.DataFrame(source)

    # return source data
    return source_data


def create_folder_if_not_exists(folder):
    """
    Create a folder if it does not already exist.

    :param string folder: location of folder
    """

    if not os.path.exists(folder):
        os.makedirs(folder, mode=0o777)
    else:
        pass


def get_detector_fields(cfg_file):
    """
    Add date/time fields to the detector fields.

    :param string cfg_file: location of configuration file.
    :return: Dataframe with date/time fields
    :rtype: dataframe
    """
    cfg_file = root_path + '/config/' + cfg_file
    detector_fields = get_io_list_from_config(cfg_file)
    detector_fields.insert(0, 'Date')
    detector_fields.insert(1, 'Time')

    return detector_fields


def get_io_list_from_config(file):
    """
    Get list of detector I/O names and their IDs via a given configuration file.

    :param string file: location of configuration file
    :return: List of I/O names
    :rtype: list[str]
    """
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


def get_latest_dataset_folder():
    """
        Return the location of the latest dataset in the 'results' folder.

    :return: Location of the latest dataset
    :rtype: string
    """
    folder = root_path + '/results/'
    latest_location = max([os.path.join(folder, d) for d in os.listdir(folder)])

    return latest_location


def get_latest_dataset():
    """
    Return the latest dataset (generic, i.e. dataset.csv file as created by the PreProcessing module).

    :return: Location of the latest generic dataset
    :rtype: string
    """
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/dataset.csv'
    print("Dataset used: ", file)

    return file


def get_sklearn_data_with_duration():
    """
    Return the latest scikit-learn dataset with duration data.

    :return: Location of the latest scikit-learn dataset with duration data.
    :rtype: string
    """
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_with_duration.csv'
    print(file)

    return file


def get_sklearn_data_without_io():
    """
    Return data the latest scikit-learn dataset without I/O data.

    :return: Location of the latest scikit-learn dataset without I/O data.
    :rtype: string
    """
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_without_io.csv'

    return file


def get_sklearn_data_with_io():
    """
    Return data the latest scikit-learn dataset with I/O data.

    :return: Location of the latest scikit-learn dataset with I/O data.
    :rtype: string
    """
    latest_folder = get_latest_dataset_folder()
    file = latest_folder + '/sklearn_dataset_with_io.csv'
    return file


def get_sklearn_X_y(file, duration, datetime):
    """
    Return x and y values to be used with the scikit-learn framework.

    :param string file: Location of the latest scikit-learn dataset
    :param boolean duration: Indicates whether dataset contains duration data
    :param boolean datetime: Indicates whether dataset contains timestamped records
    :return: x and y values for scikit-learn model as individual dataframes
    :rtype: dataframe, dataframe
    :raises ValueError: if both duration and date/time are set to True.
    """
    data = pd.read_csv(file, sep=',')

    # if duration, remove 'end' and 'start' as not useful features for learning
    if duration:
        del data['End']
        del data['Start']

        if datetime:
            raise ValueError('Datetime and Duration are not compatible features! Please choose one only.')

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


def print_number_records(file):
    """
    Print out the number of records in a given CSV file.

    :param file: location of the CSV-formatted file
    """
    df = pd.read_csv(file, sep=',')
    print("Total number of records: ", len(df))


# get current date and time
current_dt = time.strftime("%Y%m%d_%H%M%S")
results_folder = root_path + '/results/' + current_dt + '/'

# initialise raw folder
raw_output_folder = results_folder + 'phases/raw/'
