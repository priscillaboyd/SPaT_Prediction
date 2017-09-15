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

"""The Plotter class:

    -  Plots limited amount of data (to avoid data cluttered which will prevent useful visualisation)

"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# plot phase vs date/time (taking existing df and number of seconds to plot)
def plot_phase_vs_dt(df, seconds, analysis_folder):
    labels = ['Red', 'Red + Amber', 'Amber', 'Green']
    x = [0, 1, 2, 3]
    df = df[:seconds]
    df.set_index(['Date_Time'], inplace=True)
    df.plot()
    plt.locator_params(axis='x', nbins=10)
    plt.yticks(x, labels, rotation='vertical')
    plt.xlabel('Time')
    plt.ylabel('Phase')
    plt.yticks(np.arange(0, 4, 1))
    plt.savefig(analysis_folder + 'phase_vs_dt.png')
    plt.show()


# plot subplots of phases
def plot_phases_info(df, seconds, analysis_folder):
    labels = ['Red', 'Red/Amber', 'Amber', 'Green']
    df = df[:seconds]
    dfA = df.loc[:, ['Date_Time', 'A']]
    dfB = df.loc[:, ['Date_Time', 'B']]
    dfC = df.loc[:, ['Date_Time', 'C']]
    dfD = df.loc[:, ['Date_Time', 'D']]
    fig, axes = plt.subplots(nrows=2, ncols=2)
    plt.setp(axes, yticks=[0, 1, 2, 3], yticklabels=labels, xlabel='time (seconds)')
    dfA.plot(ax=axes[0, 0], color='b')
    axes[0, 0].set_title('A')
    dfB.plot(ax=axes[0, 1], color='g')
    axes[0, 1].set_title('B')
    dfC.plot(ax=axes[1, 0], color='r')
    axes[1, 0].set_title('C')
    dfD.plot(ax=axes[1, 1], color='k')
    axes[1, 1].set_title('D')
    plt.tight_layout()
    plt.savefig(analysis_folder + 'phases_info.png')
    plt.show()


# plot phase correlation
def plot_correlation(df, analysis_folder):
    pd.plotting.scatter_matrix(df, alpha=0.3, figsize=(14, 8), diagonal='kde')
    f, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
                square=True, ax=ax)
    plt.savefig(analysis_folder + 'phase_correlation.png')
    plt.show()
