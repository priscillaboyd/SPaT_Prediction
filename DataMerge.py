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

"""The DataMerge_IO class:

- Merges all phase data and I/O detection data into a single dataset

"""

import pandas as pd

# store desired fields from the processed phase data as array
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

# load files that contain phase and I/O processed data and store as dfs
phase_data = pd.read_csv('./results/phases/processed/clean_merged_phases.csv', header=0, skipinitialspace=True,
                         usecols=phase_fields)
detection_data = pd.read_csv('./results/io/io_out.csv', header=0, skipinitialspace=True, usecols=detector_fields)
phase_df = pd.DataFrame(phase_data)
detection_df = pd.DataFrame(detection_data)

# merge the two files based on their Date and Time fields
output = pd.merge(phase_df, detection_df, on=['Date', 'Time'])

# store the output with any duplicates dropped and create a final dataset CSV file
dataset = output.drop_duplicates()
dataset.to_csv('./results/dataset.csv', sep=',', index=False)
