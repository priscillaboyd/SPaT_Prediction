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

"""The Analyser class:

    Prepares the data by:
    - Creating a CSV file with phase, result (red, red/amber, amber, green), record date/time

    Allows analysis to be run:
    - Correlation analysis between phases
    - Plotting data for limited amount of time (to avoid data cluttered which will prevent useful visualisation)

"""

from analysis.Analyser import run_analysis
from tools.Utils import get_latest_dataset

# get total number of records
data = get_latest_dataset()

# load list of phases and states to run analysis against
phase_list = ['A', 'B', 'C', 'D']


if __name__ == '__main__':
    # run data analysis and produce necessary graphs
    run_analysis(data, phase_list)
