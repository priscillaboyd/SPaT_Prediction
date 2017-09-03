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

"""The DataAnalysis class:

Prepares the data by:
- Creating a CSV file with phase, result (red, red/amber, amber, green), record date/time

Allows analysis to be run
- Correlation analysis between phases
- Plotting of data for a limited amount of time (to avoid data cluttered which will not prevent useful visualisation)

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# declare data path
data = '../results/20170829_115309/dataset.csv'

# select fields that we want to use for DT
fields = ['Date', 'Time', 'Result', 'Phase']

# load data and order by phase
phase_data = pd.read_csv(data, header=0, skipinitialspace=True, usecols=fields, parse_dates=[['Date', 'Time']])
df = pd.DataFrame(phase_data)

# load list of phases and states
phase_list = ['A', 'B', 'C', 'D']
state_list = ['3', '2', '1', '0']


def prepare_data():
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
    df.to_csv('../results/20170829_115309/DA_dataset.csv', sep=',', index=False, header=False)
    print("Prepared dataset available: ../results/20170829_115309/DA_dataset.csv")

    # return final data frame
    print(df_output)
    return df_output


# analyse phase correlation
def analyse_correlation(df):
    pd.scatter_matrix(df, alpha=0.3, figsize=(14, 8), diagonal='kde')
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True, ax=ax)
    plt.show()


# plot phase vs date/time (taking existing df and number of seconds to plot)
def analyse_phase_vs_datetime(df, seconds):
    labels = ['Red', 'Red + Amber', 'Amber', 'Green']
    x = [0, 1, 2, 3]
    df = df[:seconds]
    plt.figure()
    df.set_index(['Date_Time'], inplace=True)
    df.plot()
    plt.locator_params(axis='x', nbins=10)
    plt.yticks(x, labels, rotation='vertical')
    plt.xlabel('Time')
    plt.ylabel('Phase')
    plt.yticks(np.arange(0, 4, 1))
    plt.show()


def analyse_phase_subplots(df, seconds):
    labels = ['Red', 'Red/Amber', 'Amber', 'Green']
    df = df[:seconds]
    dfA = df.loc[:, ['Date_Time', 'A']]
    dfB = df.loc[:, ['Date_Time', 'B']]
    dfC = df.loc[:, ['Date_Time', 'C']]
    dfD = df.loc[:, ['Date_Time', 'D']]
    fig, axes = plt.subplots(nrows=2, ncols=2)
    plt.setp(axes, yticks=[0, 1, 2, 3], yticklabels=labels, xlabel='time (seconds)')
    dfA.plot(ax=axes[0, 0], color='b')
    axes[0,0].set_title('A')
    dfB.plot(ax=axes[0, 1], color='g')
    axes[0,1].set_title('B')
    dfC.plot(ax=axes[1, 0], color='r')
    axes[1,0].set_title('C')
    dfD.plot(ax=axes[1, 1], color='k')
    axes[1,1].set_title('D')
    plt.tight_layout()
    plt.show()


# main function runs data analysis functions
if __name__ == '__main__':
    # df = prepare_data()
    analyse_correlation(df)
    analyse_phase_vs_datetime(df, 120)
    analyse_phase_subplots(df, 120)
