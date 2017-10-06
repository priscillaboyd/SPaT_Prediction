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
    The RNN_LSTM module implements a recurrent neural network using LSTM.
"""

import csv
import numpy as np
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from tools.Utils import current_dt, get_latest_dataset_folder, get_latest_dataset


def split_test_training(data_path, sequence_length):
    """
    Split data between test and training examples.

    :param string data_path: Location of CSV-formatted data
    :param int sequence_length: Sequence length (temporal window) to be used
    :return: Training examples (X_train), training targets (y_train), test examples (X_test) and test targets (y_test)
    :rtype: dataframe, dataframe, dataframe, dataframe
    """

    # logic for loading the CSV, using 'result' (2nd) column as basis for prediction
    with open(data_path) as f:
        record = csv.reader(f, delimiter=",")
        next(record, None)
        spat = []
        nb_of_values = 0
        for line in record:
            spat.append(float(line[2]))
            nb_of_values += 1

    # break file into chunks based on sequence length
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


def build_model():
    """
    Build the learning RNN model using Keras (Sequential) module.

    :return: RNN model
    :rtype: History object
    """
    model = Sequential()

    # declare the sizes of the layers (1d input and output)
    layers = [1, 50, 100, 1]

    # first hidden layer, using linear activation (not specified)
    model.add(LSTM(layers[1], input_shape=(None, layers[0]), return_sequences=True))
    model.add(Dropout(0.2))

    # second hidden layer
    model.add(LSTM(layers[2], return_sequences=False))
    model.add(Dropout(0.2))

    # third hidden layer
    model.add(Dense(layers[3]))
    model.add(Activation("linear"))

    # compile using MSE as loss function for regression, RMSPROP as optimiser
    model.compile(loss="mse", optimizer="RMSProp", metrics=['accuracy'])

    # return the model
    return model


def run_rnn(file):
    # define model params
    """
    Run the process to train/test a recurrent neural network using LSTM using a given dataset file.

    :param string file: Location of CSV-formatted dataset file
    :return: Model with expected (test) targets and associated scores
    :rtype: object, dataframe, object
    """
    num_epochs = 2
    sequence_length = 20

    # grab train and test data from CSV
    X_train, y_train, X_test, y_test = split_test_training(file, sequence_length)

    print(X_train)

    # build model
    model = build_model()
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=64, validation_split=0.2)

    # predict
    predict = model.predict(X_test)
    predict = np.reshape(predict, predict.size)

    # evaluate
    score = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy: ", score[1]*100, "%")

    # save model to h5 file (same folder as data)
    model_location_folder = get_latest_dataset_folder()
    model.save(model_location_folder + '/RNN_' + current_dt + '.h5')

    return model, y_test, predict
