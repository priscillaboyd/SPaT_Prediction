import pandas as pd
phases_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


# TODO: Refactoring needed to split file definition
def create_df(phase):
    fields = ['Date', 'Time', 'Aspect 0 of Phase ' + phase + '  State',
              'Aspect 1 of Phase ' + phase + '  State',
              'Aspect 2 of Phase ' + phase + '  State']
    data = pd.read_csv('./emulated_data/testdata.csv', header=0, skipinitialspace=True, usecols=fields)
    df = pd.DataFrame(data)
    return df
    # TODO: Refactoring needed to split 'to csv' function


def process_aspects(phase, df):
    aspect0 = 'Aspect 0 of Phase ' + phase + '  State'
    aspect1 = 'Aspect 1 of Phase ' + phase + '  State'
    aspect2 = 'Aspect 2 of Phase ' + phase + '  State'

    # process red results
    red = df[(df[aspect0] == 1) &
             (df[aspect1] == 0) &
             (df[aspect2] == 0)]
    red['Result'] = 'Red'
    red['Phase'] = phase
    red.to_csv('./results/phases/raw/' + phase + '_' + 'red_result_out.csv', sep=',')

    # process red/amber results
    redamber = df[(df[aspect0] == 1) &
                  (df[aspect1] == 1) &
                  (df[aspect2] == 0)]
    redamber['Result'] = 'RedAmber'
    redamber['Phase'] = phase
    redamber.to_csv('./results/phases/raw/' + phase + '_' + 'redAmber_result_out.csv', sep=',')

    # process amber results
    amber = df[(df[aspect0] == 0) &
               (df[aspect1] == 1) &
               (df[aspect2] == 0)]
    amber['Result'] = 'Amber'
    amber['Phase'] = phase
    amber.to_csv('./results/phases/raw/' + phase + '_' + 'amber_result_out.csv', sep=',')

    # process green results
    green = df[(df[aspect0] == 0) &
               (df[aspect1] == 0) &
               (df[aspect2] == 1)]
    green['Result'] = 'Green'
    green['Phase'] = phase
    green.to_csv('./results/phases/raw/' + phase + '_' + 'green_result_out.csv', sep=',')

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


# TODO: Refactoring needed to split file definition
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
    data = pd.read_csv('testdata.csv', header=0, skipinitialspace=True, usecols=detector_fields)
    df = pd.DataFrame(data)
    return df


def output_detection(data):
    data.to_csv('./results/io/' + 'io_' + 'out.csv', sep=',')

dfIO = create_output_df()
output_detection(dfIO)
print(dfIO)
