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

"""The Extractor module extracts the data by:

    - Processing a traffic simulator file in the expected CSV format.
    - Outputting results for a phase state (i.e. red = 0, red/amber = 1, amber = 2 or green = 3) using aspect I/O data.
    - Extracting the relevant detection data and saving it to a separate CSV file.

"""

from tools.Utils import create_folder_if_not_exists, get_detector_fields, convert_raw_data_to_df, results_folder, \
    raw_output_folder


def remove_sup_values(raw_data):
    """
    Ensure non-relevant (SUP) dummy values, which are generated on system startup, are removed.

    :param dataframe raw_data: raw CSV data
    :return: raw data excluding SUP values
    :rtype: dataframe
    """

    raw_data = raw_data[~raw_data['Mode Stream 0'].isin(['8 - SUP '])]
    return raw_data


def extract_phase_data(stage_list, df):
    """
    Extract stage data using stage list and given data frame.

    :param list[str] stage_list: list of stage names (e.g. ['A', 'B'])
    :param dataframe df: CSV-formatted data
    """

    print("Loading stage data...")

    # iterate over stages to get stats
    for i in range(len(stage_list)):
        stage = stage_list[i]
        df_phase = create_aspect_df(stage, df)
        process_aspect_df(stage, df_phase)
        print("Phases for stage " + stage + " extracted!")


def extract_io_data(detector_fields, df):
    """
    Extract detection I/O data from a given data frame using pre-defined detector names.

    :param list[str] detector_fields: list containing strings associated to the names of each detector
    :param dataframe df: CSV-formatted data with I/O states
    """
    print("Loading I/O data...")

    # get data frame with relevant I/O fields
    io_df = df[detector_fields]
    io_output_folder = results_folder + 'io/'
    create_folder_if_not_exists(io_output_folder)

    # process results to file
    io_output_filename = 'io_' + 'out.csv'
    io_df.to_csv(io_output_folder + io_output_filename, sep=',')

    print("I/O data extracted!")


def create_aspect_df(stage, df):
    """
    Create initial data frame for a given stage using aspect I/O data.

    :param string stage: Name of stage
    :param dataframe df: CSV-formatted data with I/O aspect states
    :return: Data frame for grouped aspect I/O data
    :rtype: dataframe
    """
    phase_fields = ['Date', 'Time', 'Aspect 0 of Phase ' + stage + '  State',
                    'Aspect 1 of Phase ' + stage + '  State',
                    'Aspect 2 of Phase ' + stage + '  State']
    aspect_df = df[phase_fields]
    return aspect_df


def process_aspect_df(stage, df):
    """
    Process aspect I/O data to infer red, red/amber, amber or green phase for a given stage

    :param string stage: Name of stage
    :param dataframe df: CSV-formatted data with grouped aspect I/O data
    """

    # create folder if it does not exist to store the outputs
    create_folder_if_not_exists(raw_output_folder)

    # declare aspect variables for re-usability
    aspect0 = 'Aspect 0 of Phase ' + stage + '  State'
    aspect1 = 'Aspect 1 of Phase ' + stage + '  State'
    aspect2 = 'Aspect 2 of Phase ' + stage + '  State'

    # process red results
    red = df[(df[aspect0] == 1) &
             (df[aspect1] == 0) &
             (df[aspect2] == 0)]
    red['Result'] = '0'
    red['Phase'] = stage
    red_output_filename = stage + '_' + 'red_result_out.csv'
    red.to_csv(raw_output_folder + red_output_filename, sep=',')

    # process red/amber results
    red_amber = df[(df[aspect0] == 1) &
                   (df[aspect1] == 1) &
                   (df[aspect2] == 0)]
    red_amber['Result'] = '1'
    red_amber['Phase'] = stage
    red_amber_output_filename = stage + '_' + 'redAmber_result_out.csv'
    red_amber.to_csv(raw_output_folder + red_amber_output_filename, sep=',')

    # process amber results
    amber = df[(df[aspect0] == 0) &
               (df[aspect1] == 1) &
               (df[aspect2] == 0)]
    amber['Result'] = '2'
    amber['Phase'] = stage
    amber_output_filename = stage + '_' + 'amber_result_out.csv'
    amber.to_csv(raw_output_folder + amber_output_filename, sep=',')

    # process green results
    green = df[(df[aspect0] == 0) &
               (df[aspect1] == 0) &
               (df[aspect2] == 1)]
    green['Result'] = '3'
    green['Phase'] = stage
    green_output_filename = stage + '_' + 'green_result_out.csv'
    green.to_csv(raw_output_folder + green_output_filename, sep=',')

    # process errors (do not write to file)
    error = df[(df[aspect0] == 0) & (df[aspect1] == 0) & (df[aspect2] == 0)]
    if error.size > 0:
        print("Errors removed (not written to file)...")


def extract(raw_data, cfg_file):
    """
    Run data extract method.

    :param dataframe raw_data: CSV-formatted raw data
    :param string cfg_file: location of the configuration file
    """

    # get folder to store results of all phases
    create_folder_if_not_exists(results_folder)

    # initialise by converting the raw data into the df
    source_data_df = convert_raw_data_to_df(raw_data)
    source_data_df = remove_sup_values(source_data_df)

    # first get the phase data (all possible phases included)
    phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    extract_phase_data(phase_list, source_data_df)

    # then get the I/O data using detector fields
    detector_fields = get_detector_fields(cfg_file)
    extract_io_data(detector_fields, source_data_df)
