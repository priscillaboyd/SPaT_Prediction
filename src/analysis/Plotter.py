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
    The Plotter module plots a limited amount of examples (to avoid graph cluttering), helpign understanding the nature
    and the components available in the data.
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def plot_phase_vs_dt(df, seconds, analysis_folder):
    """
    Plot phase versus date/time, taking data frame and number of seconds to plot.

    :param object df: dataframe
    :param int seconds: number of seconds to plot
    :param string analysis_folder: analysis folder location
    """

    # define x values and data source (sliced from data frame)
    x = [0, 1, 2, 3]
    df = df[:seconds]

    # define index based on date_time column from the data
    df.set_index(['Date_Time'], inplace=True)

    # plot the data
    df.plot()

    # configure plot
    plt.locator_params(axis='x', nbins=10)
    labels = ['Red', 'Red + Amber', 'Amber', 'Green']
    plt.yticks(x, labels, rotation='vertical')
    plt.xlabel('Time')
    plt.ylabel('Phase')
    plt.yticks(np.arange(0, 4, 1))

    # save plot to file
    plt.savefig(analysis_folder + 'phase_vs_dt.png')

    # display plot
    plt.show()


def plot_phases_info(df, seconds, analysis_folder):
    """
    Plot sub-plots of each phase within a data frame for the given number of seconds.

    :param object df: dataframe
    :param int seconds: number of seconds to plot
    :param string analysis_folder: analysis folder location
    """

    # define x values and data source (sliced from data frame)
    df = df[:seconds]
    df_a = df.loc[:, ['Date_Time', 'A']]
    df_b = df.loc[:, ['Date_Time', 'B']]
    df_c = df.loc[:, ['Date_Time', 'C']]
    df_d = df.loc[:, ['Date_Time', 'D']]

    # configure plot
    labels = ['Red', 'Red/Amber', 'Amber', 'Green']
    fig, axes = plt.subplots(nrows=2, ncols=2)
    plt.setp(axes, yticks=[0, 1, 2, 3], yticklabels=labels, xlabel='Time (seconds)')

    # plot the data
    df_a.plot(ax=axes[0, 0], color='b')
    axes[0, 0].set_title('A')
    df_b.plot(ax=axes[0, 1], color='g')
    axes[0, 1].set_title('B')
    df_c.plot(ax=axes[1, 0], color='r')
    axes[1, 0].set_title('C')
    df_d.plot(ax=axes[1, 1], color='k')
    axes[1, 1].set_title('D')
    plt.tight_layout()

    # save plot to file
    plt.savefig(analysis_folder + 'phases_info.png')

    # display plot
    plt.show()


def plot_correlation(df, analysis_folder):
    """
    Plot correlation of stages as a heat map.

    :param object df: dataframe
    :param string analysis_folder: analysis folder location
    """

    # configure the heat map
    pd.plotting.scatter_matrix(df, alpha=0.3, figsize=(14, 8), diagonal='kde')
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True, ax=ax)

    # save plot to file
    plt.savefig(analysis_folder + 'phase_correlation.png')

    # display plot
    plt.show()
