# Hive

Similar to [1a](https://github.com/FuadBabaev/ai-masters-bigdata/tree/main/projects/1a).

## Task

The task is to predict the probability of a click on an ad banner using the [Criteo Dataset](https://www.kaggle.com/c/criteo-display-ad-challenge). Training occurs on a small dataset on a local machine. Filtering of the test set and prediction are done in a distributed manner using [Hadoop Streaming](https://hadoop.apache.org/docs/r1.2.1/streaming.html).

## Dataset

Paths to the datasets:
- Training: local `/home/users/datasets/criteo/criteo_train1`, 1.3G 
- Test: HDFS `/datasets/criteo/criteo_valid_large_features`, 19.4G
- Test labels: local `/home/users/datasets/criteo/criteo_valid_large_filtered_labels`, 81M

## Solution

### Model

The script `model.py` contains the list of dataset features `fields` and the model itself `model`.

### Training

The script `train.py` extracts a validation set from the training dataset. To train the model and output the log loss:
```sh
train.sh 2 /home/users/datasets/criteo/criteo_train1
```

Arguments:
- project number
- path to the dataset

Additionally, the trained model is saved in the `2.joblib` file.

### Hive: Prediction and Filtering

To run the model through the same process as in [1a](https://github.com/FuadBabaev/ai-masters-bigdata/tree/main/projects/1a), execute the following script:

```
create database if not exists ${NAME};
use ${NAME};

drop table hw2_test;
source projects/2/create_test.hql;
describe hw2_test;
select count(id) from hw2_test;

drop table hw2_pred;
source projects/2/create_pred.hql;
describe hw2_pred;

source projects/2/filter_predict.hql;
select count(id) from hw2_pred;

source projects/2/select_out.hql;
```

As a result, predictions will be saved on the cluster in the `FuadBabaev_hiveout` folder.
