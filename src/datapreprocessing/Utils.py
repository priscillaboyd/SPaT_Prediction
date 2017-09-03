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

# converts the raw data (CSV file) into a data frame
def convert_raw_data_to_df(raw_data):
    raw_data = root_path + '/data/' + raw_data
    source = pd.read_csv(raw_data, header=0, skipinitialspace=True)
    source_data = pd.DataFrame(source)
    return source_data


# get the current date/time in YYMMDD_HHMMSS format
def get_current_datetime():
    return time.strftime("%Y%m%d_%H%M%S")


# create folder if it doesn't exist
def create_folder_is_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, mode=0o777)
    else:
        pass


# store desired fields as array
def get_output_fields():
    output_fields = ['Date', 'Time', 'Result', 'Phase']
    return output_fields


# adds date/time fields to the detector fields (for desired results)
def get_detector_fields(cfg_file):
    cfg_file = root_path + '/data/' + cfg_file
    desired_detector_fields = get_io_list_from_config(cfg_file)
    desired_detector_fields.insert(0, 'Date')
    desired_detector_fields.insert(1, 'Time')
    return desired_detector_fields


# get the location of the (latest created) results folder
def get_results_folder():
    results_folder = root_path + '/results/' + current_dt + '/'
    return results_folder


# define and create raw output folder if it doesn't exist yet
def get_raw_output_folder():
    results_folder = get_results_folder()
    raw_output_folder = results_folder + 'phases/raw/'
    create_folder_is_not_exists(raw_output_folder)
    return raw_output_folder


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

# get current date and time
current_dt = get_current_datetime()