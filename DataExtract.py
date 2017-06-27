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

"""The DataExtract class:

- Processes a traffic simulator file in the expected CSV format
- Performs analysis and outputs the results for a state of a phase (i.e. red = 0, red/amber = 1, amber = 2
or green = 3)
using physical aspect data, outputting results to separate CSV files
- Extracts the relevant detection data and saves it to a separate CSV file

"""

import pandas as pd
import os
phases_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

source = pd.read_csv('./emulated_data/testdata_short.csv', header=0, skipinitialspace=True)
source_data = pd.DataFrame(source)

# ensure SUP values are removed
source_data = source_data[~source_data['Mode Stream 0'].isin(['8 - SUP '])]

def create_df(phase):
    phase_fields = ['Date', 'Time', 'Aspect 0 of Phase ' + phase + '  State',
                    'Aspect 1 of Phase ' + phase + '  State',
                    'Aspect 2 of Phase ' + phase + '  State']
    df = source_data[phase_fields]
    return df


def process_aspects(phase, df):
    aspect0 = 'Aspect 0 of Phase ' + phase + '  State'
    aspect1 = 'Aspect 1 of Phase ' + phase + '  State'
    aspect2 = 'Aspect 2 of Phase ' + phase + '  State'

    # process red results
    red = df[(df[aspect0] == 1) &
             (df[aspect1] == 0) &
             (df[aspect2] == 0)]
    red['Result'] = '0'
    red['Phase'] = phase

    red_output_folder = './results/phases/raw/'
    red_output_filename = phase + '_' + 'red_result_out.csv'

    # ensure folder exists before creating the file
    if not os.path.exists(red_output_folder):
        os.makedirs(red_output_folder, mode=0o777)
    red.to_csv(red_output_folder + red_output_filename, sep=',')

    # process red/amber results
    redamber = df[(df[aspect0] == 1) &
                  (df[aspect1] == 1) &
                  (df[aspect2] == 0)]
    redamber['Result'] = '1'
    redamber['Phase'] = phase

    redamber_output_folder = './results/phases/raw/'
    redamber_output_filename = phase + '_' + 'redAmber_result_out.csv'

    # ensure folder exists before creating the file
    if not os.path.exists(redamber_output_folder):
        os.makedirs(redamber_output_folder, mode=0o777)

    # save to csv
    redamber.to_csv(redamber_output_folder + redamber_output_filename, sep=',')

    # process amber results
    amber = df[(df[aspect0] == 0) &
               (df[aspect1] == 1) &
               (df[aspect2] == 0)]
    amber['Result'] = '2'
    amber['Phase'] = phase
    amber.to_csv('./results/phases/raw/' + phase + '_' + 'amber_result_out.csv', sep=',')

    # process green results
    green = df[(df[aspect0] == 0) &
               (df[aspect1] == 0) &
               (df[aspect2] == 1)]
    green['Result'] = '3'
    green['Phase'] = phase

    green_output_folder = './results/phases/raw/'
    green_output_filename = phase + '_' + 'green_result_out.csv'

    # ensure folder exists before creating the file
    if not os.path.exists(green_output_folder):
        os.makedirs(green_output_folder, mode=0o777)

    green.to_csv(green_output_folder + green_output_filename, sep=',')

    # process errors (do not write to file)
    error = df[(df[aspect0] == 0) &
               (df[aspect1] == 0) &
               (df[aspect2] == 0)]

    # TODO: Refactoring needed to split the actual stats from df definition
    print("number of red:", len(red))
    print("number of red and amber:", len(redamber))
    print("number of amber:", len(amber))
    print("number of green:", len(green))
    print("number of errors:", len(error))
    print("total for phase " + phase + ":", len(df))

# iterate over phases to get stats
for i in range(len(phases_list)):
    phase = phases_list[i]
    dfPhase = create_df(phase)
    process_aspects(phase, dfPhase)
    print(phase)


# process the
def create_output_df():
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

    df = source_data[detector_fields]
    return df


def output_detection(data):
    io_output_folder = './results/io/'
    io_output_filename = 'io_' + 'out.csv'

    # ensure folder exists before creating the file
    if not os.path.exists(io_output_folder):
        os.makedirs(io_output_folder, mode=0o777)

    data.to_csv(io_output_folder + io_output_filename, sep=',')

dfIO = create_output_df()
output_detection(dfIO)
print(dfIO)
