import pandas as pd
from pathlib import Path
import os

fields = ['Date', 'Time', 'Result', 'Phase']
pathlist = Path('./results/phases/raw/').glob('**/*.csv')
for path in pathlist:
    path_in_str = str(path)
    fileName = os.path.basename(path_in_str)
    fullPath = './results/phases/raw/' + fileName
    print(fullPath)
    data = pd.read_csv(fullPath, header=0, skipinitialspace=True, usecols=fields)
    df = pd.DataFrame(data)

    if df.shape[0] > 0:
        df.to_csv('./results/phases/processed/' + 'clean_' + fileName, sep=',')