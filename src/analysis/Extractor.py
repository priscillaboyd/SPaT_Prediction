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
    The Extractor module takes phase, result (red, red/amber, amber, green), record date/time to prepare for
    data analysis.
"""

from __future__ import absolute_import
from tools.Utils import output_fields
import pandas as pd


def create_analysis_dataset(data, phase_list, analysis_folder):

    """
    Prepares data for data analysis by creating the analysis dataset.

    :param object data: CSV-formatted file (as generated by the Analysis module)
    :param list[str] phase_list: list of stage names (e.g. ['A', 'B'])
    :param string analysis_folder: analysis folder location
    :return: data formatted for analysis
    :rtype: object
    """

    # load data and order by phase
    phase_data = pd.read_csv(data, header=0, skipinitialspace=True, usecols=output_fields,
                             parse_dates=[['Date', 'Time']])
    df = pd.DataFrame(phase_data)

    # initialise for later usage
    df_output = pd.DataFrame()

    # loop through all phases in the list
    for x in range(len(phase_list)):
        phase = phase_list[x]

        # extract data for rows in the current phase
        df_phase_only = df.loc[df['Phase'] == phase]

        # remove unnecessary fields and rename 'result' as the given phase
        df_result = df_phase_only.loc[:, :'Result']
        df_result.rename(columns={'Result': phase}, inplace=True)

        # append to empty data frame if first time running, otherwise merge on Date_Time
        if df_output.empty:
            df_output = df_output.append(df_result)
        else:
            df_output = pd.merge(df_output, df_result, on=['Date_Time'])

    # write result further to csv
    df.to_csv(analysis_folder + 'analysis_dataset.csv', sep=',', index=False, header=False)
    print('Prepared analysis data available:' + analysis_folder + 'analysis_dataset.csv')

    # return final data frame
    return df_output
