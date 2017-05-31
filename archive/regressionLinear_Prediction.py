import quandl, math
import numpy as np
import pandas as pd
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
from matplotlib import style

# define data using quandl
df = quandl.get("WIKI/GOOGL")
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'

# add valuable fields for analysis and replace NaNs with -99999
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

# create np array from the features and then scale it
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)

# slice the label (output)
X_lately = X[-forecast_out:]

# create a var that has the most recent features (to be used for forecasting)
X = X[:-forecast_out]

# drop any NaNs
df.dropna(inplace=True)

# create np array for the label
y = np.array(df['label'])

# split the data into train and test (80% as training, 20% as test)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# set classifier to use Linear Regression with 1 thread
clf = LinearRegression(n_jobs=-1)

# fit the training data to the classifier
clf.fit(X_train, y_train)

# calculate confidence using test data and output
confidence = clf.score(X_test, y_test)

# predicting the future value
forecast_set = clf.predict(X_lately)
print(forecast_set, confidence, forecast_out)

# set up the plot for display
style.use('ggplot')

# add another column to the data, initialise to a np NaN
df['Forecast'] = np.nan

# prepare dated info for display, note: 86,400 seconds = 1 day
last_date = df.iloc[-1].name
last_unit = last_date.timestamp()
one_day = 86400
next_unix = last_unit + one_day
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

# plot the graph
df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()