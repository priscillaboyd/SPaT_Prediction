import pandas as pd
from pathlib import Path
import os

# TODO: Create file if doesn't exist in the right shape
# output = pd.read_csv('./results/merge_test.csv', header=0, skipinitialspace=True)
fields = ['Date', 'Time', 'Result', 'Phase']
out_df = pd.DataFrame([])

pathlist = Path('./results/phases/processed/').glob('**/*.csv')
for path in pathlist:
    path_in_str = str(path)
    fileName = os.path.basename(path_in_str)
    fullPath = './results/phases/processed/' + fileName
    data = pd.read_csv(fullPath, header=0, skipinitialspace=True, usecols=fields)
    df = pd.DataFrame(data)
    out_df = df.append(out_df)
    out_df = out_df.sort_values(['Date', 'Time', 'Phase'], ascending=[True, True, True])
    out_df.to_csv('./results/phases/phases.csv', sep=',')


dataset = pd.read_csv('./results/phases/phases.csv', header=0, skipinitialspace=True, usecols=fields)
dataset_df = pd.DataFrame(dataset)
dataset_df2 = dataset_df.drop_duplicates()
dataset_df2.to_csv('./results/phases/phases.csv', sep=',', index=False)

print(dataset_df2)