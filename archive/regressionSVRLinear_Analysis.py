import quandl, math
import numpy as np
import pandas as pd
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression

# define data frames, doing pre-processing to create valuable data
df = quandl.get("WIKI/GOOGL")
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

print(df.head())
#print(df.tail())

# add another column to the data as to what we want to forecast
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

# define features and label as a np array
X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])

# preprocessing to help with scaling to be in range of -1 and 1
X = preprocessing.scale(X)
y = np.array(df['label'])

# split dataset into training and test sets, with the latter taking 20%
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# set the classifier to use Support Vector Regression, with penalty parameter (C)
clf = svm.SVR(C=1.0)

# train and test, then output confidence values using various SVR kernels
clf.fit(X_train, y_train)
for k in ['linear','poly','rbf','sigmoid']:
    clf = svm.SVR(kernel=k)
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print("SVR:", k, " - ", confidence)

# set the classifier to use Linear Regression, using 1 thread
clf = LinearRegression(n_jobs=-1)

# train and test, then output confidence values using SVR
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print("LinearRegression: ", confidence)