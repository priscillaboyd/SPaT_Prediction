# Signal Phase & Timing (SPaT) Prediction

Predicts signal phase and timing (SPaT) by using a combination of machine learning techniques and historical traffic data.

This engine has been initially developed to support a dissertation towards an MSc in Software Engineering for the University of Oxford.

## Features

* Takes historical traffic controller signal phase and detection data to create datasets suitable for machine learning analyses
* Enables feature extraction from data to provide signal state and phase duration
* Implements the Classification and Regression Tree (CART) for SPaT prediction.
* Implements Recurrent Neural Network with Long Short-Term Memory for SPaT prediction.
* Supports the creation of plots for data analysis

## Getting started

The software has been divided into five packages:
* **Pre-Processing**: processes the data in the expected format, creating datasets for usage with Decision Tree and Neural Network model creation
* **Analysis**: manipulates the data for analysis, creating plots for further understanding
* **Decision Tree**: implements the Classification and Regression Tree (CART) algorithm to predict SPaT
* **Neural Network**: implements a Recurrent Neural Network (RNN) using Long Short-Term Memory (LSTM) to predict SPaT
* **Tools**: provides a number of helper functions that are re-used throughout the other packages


## Data format

TBC.

### Pre-requisites

The following versions (or newer) are required to run SPaT Prediction:

* Keras 2.0.3
* matplotlib 2.0.2
* NumPy 1.13.1
* Pandas 0.20.3
* Python 3.5.2
* seaborn 0.8
* scikit-learn 0.19.0
* TensorFlow 1.0.0


## Author

* **Priscilla Boyd** - [priscillaboyd](https://github.com/priscillaboyd)


## License

This project is licensed under the Apache Licence 2.0 - see the [LICENSE.md](LICENSE.md) file for further information