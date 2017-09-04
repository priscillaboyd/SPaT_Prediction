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

import matplotlib.pyplot as plt
import numpy as np
import csv
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from machine_learning.UtilsML import get_latest_dataset

# np.random.seed(1234)


# split data into test and training
def split_test_training(data_path, sequence_length=50):

    # logic for loading the CSV, using 'result' (2nd) column as basis for prediction
    with open(data_path) as f:
        data = csv.reader(f, delimiter=",")
        next(data, None)
        spat = []
        nb_of_values = 0
        for line in data:
            spat.append(float(line[2]))
            nb_of_values += 1

    # break file into chunks
    result = []
    for index in range(len(spat) - sequence_length):
        result.append(spat[index: index + sequence_length])
    result = np.array(result)

    # divide set into 20% for test, 80% for training
    row = int(round(0.8 * result.shape[0]))
    train = result[:row, :]
    np.random.shuffle(train)
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = result[row:, :-1]
    y_test = result[row:, -1]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    return [X_train, y_train, X_test, y_test]


# build model using Keras' Sequential
def build_model():
    model = Sequential()

    # declare the sizes of the layers (1d input and output)
    layers = [1, 50, 100, 1]

    # first hidden layer
    model.add(LSTM(layers[1], input_shape=(None, layers[0]), return_sequences=True))
    model.add(Dropout(0.2))

    # second hidden layer
    model.add(LSTM(layers[2], return_sequences=False))
    model.add(Dropout(0.2))

    # third hidden layer
    model.add(Dense(layers[3]))
    model.add(Activation("linear"))

    # compile using MSE as loss function for regression, RMSPROP as optimiser
    model.compile(loss="mse", optimizer="rmsprop", metrics=['accuracy'])

    # return the model
    return model


def run_RNN():
    # define model params
    num_epochs = 5
    sequence_length = 10
    data_path = get_latest_dataset()

    # grab train and test data from CSV
    X_train, y_train, X_test, y_test = split_test_training(data_path, sequence_length)

    print(X_train)


    # build model
    model = build_model()
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=16, validation_split=0.2)

    # predict
    predict = model.predict(X_test)
    predict = np.reshape(predict, (predict.size,))

    # evaluate
    score = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy: ", score[1]*100, "%")

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(y_test[:100])
    plt.plot(predict[:100])
    plt.show()

    # save model to h5 file
    model.save('model.h5')

    return model, y_test, predict


# main function
if __name__ == '__main__':
    run_RNN()
