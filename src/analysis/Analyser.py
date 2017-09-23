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

    - Prepares data with phase, result (red, red/amber, amber, green), record date/time
    - Runs analysis for correlation between phases

"""
from analysis.Extractor import create_analysis_dataset
from analysis.Plotter import plot_phase_vs_dt, plot_phases_info, plot_correlation
from tools.Utils import print_number_records, get_latest_dataset_folder, create_folder_if_not_exists


# create folder for all analyses / results
def create_analysis_folder():
    results_folder = get_latest_dataset_folder()
    analysis_folder = results_folder + '/analysis/'
    create_folder_if_not_exists(analysis_folder)
    return analysis_folder


# run data analysis from given dataset and phase list required
def run_analysis(dataset, phase_list):
    # define folder
    analysis_folder = create_analysis_folder()

    # print number of records in the dataset originally
    print_number_records(dataset)

    # prepare data for analysis
    df = create_analysis_dataset(dataset, phase_list, analysis_folder)

    # # perform correlation analysis and plot graphs for 5 min
    plot_correlation(df, analysis_folder)
    plot_phase_vs_dt(df, 300, analysis_folder)
    plot_phases_info(df, 300, analysis_folder)
