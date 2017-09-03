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

"""The DataExtract class extracts the data by:

- Processing a traffic simulator file in the expected CSV format
- Outputs results for a phase state (i.e. red = 0, red/amber = 1, amber = 2 or green = 3) using physical aspect data
- Extracting the relevant detection data and saves it to a separate CSV file

"""

# extracts phase data from the data set
from datapreprocessing.Utils import get_results_folder, create_folder_is_not_exists, get_raw_output_folder, \
    get_detector_fields, convert_raw_data_to_df


def load_phase_data(phase_list, source_data_df):
    print("Loading phase data...")

    # iterate over phases to get stats
    for i in range(len(phase_list)):
        phase = phase_list[i]
        df_phase = create_aspect_df(phase, source_data_df)
        process_aspect_df(phase, df_phase)
        print("Phase " + phase + " extracted!")


# extracts detection data from the data set
def load_io_data(df, cfg_file, detector_fields):
    print("Loading I/O data...")

    # get data frame with relevant i/o fields
    io_df = df[detector_fields]

    # create folders for results
    results_folder = get_results_folder()
    create_folder_is_not_exists(results_folder)
    io_output_folder = get_results_folder() + 'io/'
    create_folder_is_not_exists(io_output_folder)

    # process results
    io_output_filename = 'io_' + 'out.csv'
    io_df.to_csv(io_output_folder + io_output_filename, sep=',')
    print("I/O data extracted!")


# create initial data frame for a given phase
def create_aspect_df(phase, source_data_df):
    phase_fields = ['Date', 'Time', 'Aspect 0 of Phase ' + phase + '  State',
                    'Aspect 1 of Phase ' + phase + '  State',
                    'Aspect 2 of Phase ' + phase + '  State']
    df = source_data_df[phase_fields]
    return df


# process aspect I/O to get red, red/amber, amber or green for a phase
def process_aspect_df(phase, df):
    aspect0 = 'Aspect 0 of Phase ' + phase + '  State'
    aspect1 = 'Aspect 1 of Phase ' + phase + '  State'
    aspect2 = 'Aspect 2 of Phase ' + phase + '  State'

    # create folder for outputs
    raw_output_folder = get_raw_output_folder()

    # process red results
    red = df[(df[aspect0] == 1) &
             (df[aspect1] == 0) &
             (df[aspect2] == 0)]
    red['Result'] = '0'
    red['Phase'] = phase
    red_output_filename = phase + '_' + 'red_result_out.csv'
    red.to_csv(raw_output_folder + red_output_filename, sep=',')

    # process red/amber results
    red_amber = df[(df[aspect0] == 1) &
                   (df[aspect1] == 1) &
                   (df[aspect2] == 0)]
    red_amber['Result'] = '1'
    red_amber['Phase'] = phase
    red_amber_output_filename = phase + '_' + 'redAmber_result_out.csv'
    red_amber.to_csv(raw_output_folder + red_amber_output_filename, sep=',')

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
    # TODO: Print errors if they exist
    error = df[(df[aspect0] == 0) & (df[aspect1] == 0) & (df[aspect2] == 0)]


# ensure SUP values are removed
def remove_sup_values(source_data):
    source_data = source_data[~source_data['Mode Stream 0'].isin(['8 - SUP '])]
    return source_data


# run data extract
def data_extract(raw_data, cfg_file):
    # store desired fields from the processed I/O detection data as array
    detector_fields = get_detector_fields(cfg_file)

    # initialise by converting the raw data into the df
    source_data_df = convert_raw_data_to_df(raw_data)
    source_data_df = remove_sup_values(source_data_df)

    # first get the phase data
    phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    load_phase_data(phase_list, source_data_df)

    # then get the i/o data
    load_io_data(source_data_df, cfg_file, detector_fields)
