# Hadoop Streaming

## Task

The task is to predict the probability of a click on an ad banner using the [Criteo Dataset](https://www.kaggle.com/c/criteo-display-ad-challenge). Training occurs on a small dataset on a local machine. Filtering of the test set and prediction are done in a distributed manner using [Hadoop Streaming](https://hadoop.apache.org/docs/r1.2.1/streaming.html).

## Dataset

Paths to the datasets:
- Training: local `/home/users/datasets/criteo/criteo_train1`, 1.3G 
- Test: HDFS `/datasets/criteo/criteo_valid_large_features`, 19.4G
- Test labels: local `/home/users/datasets/criteo/criteo_valid_large_filtered_labels`, 81M

## Solution

### Model

The script `model.py` contains the list of dataset features `fields` and the model itself `model`:
```python
from model import fields, model
print(type(fields))
print(type(model))
```

### Training

The script `train.py` extracts a validation set from the training dataset. To train the model and output the log loss:
```sh
train.sh 1 /home/users/datasets/criteo/criteo_train1
```

Arguments:
- project number
- path to the dataset

### Hadoop Streaming: Prediction

The script `predict.py` can be used for distributed prediction. For this, a mapper is launched. The script `predict.sh` defines the MapReduce task using Hadoop Streaming:
```sh
predict.sh 1.joblib,predict.py, /datasets/criteo/criteo_valid_large_features predicted predict.py
```

Arguments:
- files to send to the data:
    - `1.joblib` --- trained model
    - `predict.py` --- script making predictions
- path to the test dataset
- path to save predictions
- mapper

### Hadoop Streaming: Filtering

The script `filter_cond.py` defines the function `filter_cond()` that takes a dictionary with the values of one dataset record and returns `True` if the record passes the filter, `False` otherwise.

Filtering is implemented by the script `filter.py` using Hadoop Streaming as a MapReduce task. To start distributed filtering:
```sh
filter.sh filter.py,filter_cond.py,model.py /datasets/criteo/criteo_valid_large_features filtered filter.py
```

Arguments:
- files to send to the data:
    - `filter.py` --- filtering script
    - `filter_cond.py` --- filtering condition
    - `model.py` --- script defining field names
- path to the test dataset
- path to save predictions
- mapper

### Hadoop Streaming: Filtering + Prediction

The previous two steps can be combined into one MapReduce task, where the mapper performs filtering and the reducer makes predictions. The script is called:

```sh
filter_predict.sh filter.py,filter_cond.py,predict.py,model.py,1.joblib /datasets/criteo/criteo_valid_large_features pred_with_filter filter.py predict.py
```

Arguments:
- files to send to the data
- path to the test dataset
- path to save predictions
- mapper
- reducer

### Metric

Logloss is calculated on the filtered objects:

```sh
scorer_local.py /home/users/datasets/criteo/criteo_valid_large_filtered_labels pred_with_filter
```

Arguments:
- path to true labels
- path to predicted probabilities

