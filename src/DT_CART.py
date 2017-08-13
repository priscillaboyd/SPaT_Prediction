import pandas as pd

# declare data path
data = '../results/20170813_114136/dataset.csv'

# select fields that we want to use for DT
fields = ['Date', 'Time', 'Result', 'Phase']

# load data and order by phase
phase_data = pd.read_csv(data, header=0, skipinitialspace=True, usecols=fields, parse_dates=[['Date', 'Time']])
df = pd.DataFrame(phase_data)

# load list of phases and states
phase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
state_list = ['3', '2', '1', '0']


# prepare data for decision tree processing
def prepare_dt_data():

    # loop through phases
    for x in range(len(phase_list)):
        phase = phase_list[x]

        # create a df for phase A only
        df2 = df[df['Phase'] == phase]

        print("Preparing data...")
        # initialise by using the very first record
        start_time = df2['Date_Time'].values[0]
        current_result = df2['Result'].values[0]

        new_columns = ['Phase', 'Result', 'Start', 'End', 'Duration']
        df_new_columns = pd.DataFrame(columns=new_columns)

        # loop through all records from DF
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

                # write new row to data frame
                new_row = [phase, current_result, df_start, df_end, duration]
                df_new_columns.loc[(len(df_new_columns))] = new_row

                # go to the next result and start time
                current_result = df2['Result'].values[i]
                start_time = df2['Date_Time'].values[i]

        print(df_new_columns)

        # write result to csv
        df_new_columns.to_csv('../results/20170813_114136/' + 'DT_dataset.csv', sep=',', index=False)
        print("Prepared dataset available: ../results/20170813_114136/DT_dataset.csv")


# main function runs data processing for decision trees
if __name__ == '__main__':
    prepare_dt_data()
