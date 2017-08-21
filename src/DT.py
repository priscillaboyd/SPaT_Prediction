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

"""The DT class:

Prepares the data by:
- Creating a CSV file with phase, result, duration until change of each state
- Ensures the data is suitable for scikit-learn (e.g. phase types are represented numerically)

Implements the Random Forest ensemble

"""
import pandas as pd

# declare data path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

data = '../results/20170813_114136/dataset.csv'

# select fields that we want to use for DT
fields = ['Date', 'Time', 'Result', 'Phase']

# load data with selected fields and parse date/time to a single Date_Time column
phase_data = pd.read_csv(data, header=0, skipinitialspace=True, usecols=fields, parse_dates=[['Date', 'Time']])
df = pd.DataFrame(phase_data)

# load list of phases and states
phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


# prepare data for scikit-learn decision tree processing
def prepare_dt_data():

    new_columns = ['Phase', 'Result', 'Start', 'End', 'Duration']
    df_new_columns = pd.DataFrame(columns=new_columns)

    # write file for the first time with header
    df_new_columns.to_csv('../results/20170813_114136/scikit_dataset.csv', sep=',', index=False, mode='w')

    # loop through phases
    for x in range(len(phase_list)):
        phase = phase_list[x]

        # create a df for phase A only
        df2 = df[df['Phase'] == phase]

        print("Preparing data...")
        # initialise by using the very first record
        start_time = df2['Date_Time'].values[0]
        current_result = df2['Result'].values[0]

        # loop through all records from DF to process duration
        for i in range(len(df2.index)):

            # if the phase is the same, set as end time
            if df2['Result'].values[i] == current_result:
                end_time = df2['Date_Time'].values[i]

            # if the phase is no longer the same or it's the last record, use end time so far to get duration
            if df2['Result'].values[i] != current_result or i+1 == len(df2.index):
                df_start = pd.to_datetime(start_time)
                df_end = pd.to_datetime(end_time)
                duration = pd.Timedelta(df_end - df_start).seconds

                # if the time is the same, force duration = 1
                if duration == 86399.0:
                    df_end = df_start
                    duration = 1.0

                # convert phase ID to int (to cater for scikit-learn requirements)
                phase_value = str(x)

                # write new row to data frame
                new_row = [phase_value, current_result, df_start, df_end, duration]
                df_new_columns.loc[(len(df_new_columns))] = new_row

                # go to the next result and start time
                current_result = df2['Result'].values[i]
                start_time = df2['Date_Time'].values[i]

        print(df_new_columns)

    # write result further to csv
    df_new_columns.to_csv('../results/20170813_114136/scikit_dataset.csv', sep=',', index=False,
                              header=False, mode='a')
    print("Prepared dataset available: ../results/20170813_114136/scikit_dataset.csv")
    return df_new_columns


# implement the Random Forest ensemble algorithm
def run_random_forest():
    # Get dataset
    df_train = pd.read_csv('../results/20170813_114136/scikit_dataset.csv')

    cols = ['Phase', 'Result']
    X = df_train[cols]
    y = df_train['Duration']

    # split data into train / test (20% for test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    rf_model = RandomForestRegressor(n_estimators=1000, min_samples_split=6, oob_score=True, min_samples_leaf=5,
                                     criterion='mae')

    # fit model using training data
    rf_model.fit(X_train, y_train)

    # predict on new (test) data and encapsulate result in data frame
    y_predicted = rf_model.predict(X_test)
    result = pd.DataFrame(y_predicted)

    # get the coefficient of determination to measure how good the random forest model is
    score = rf_model.score(X_test, y_test)

    print(result)
    print("Total number of features:", rf_model.n_features_)
    print("Total score:", score)

    # pd.DataFrame.to_csv(df_result,'../results/20170813_114136/result.csv')

# main function runs data processing for decision trees
if __name__ == '__main__':
    df = prepare_dt_data()
    run_random_forest()
