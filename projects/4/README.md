# Predicting Product Ratings from Text Reviews

## Overview

Predict the rating of a product based on its text review using Spark ML. The model training and prediction must be done using Spark ML.

## Dataset Description

The dataset consists of JSON lines with the following structure:
```json
{
  "id": 1,
  "overall": 1,
  "vote": "25",
  "verified": false,
  "reviewTime": "12 19, 2008",
  "reviewerID": "APV13CM0919JD",
  "asin": "B001GXRQW0",
  "reviewerName": "LEH",
  "reviewText": "Amazon,\nI am shopping for Amazon.com gift cards...",
  "summary": "Merry Christmas.",
  "unixReviewTime": 1229644800
}
```

### Fields:
- `id`: Record identifier, monotonically increasing from 1.
- `overall`: Rating given by the user, generally a float.
- `vote`: Number of people who liked the review.
- `verified`: `True` if the reviewer bought the product on the site.
- `reviewTime`: Time when the review was written or published.
- `reviewerID`: Identifier of the reviewer.
- `asin`: Identifier of the product.
- `reviewerName`: Name of the reviewer.
- `reviewText`: The review text.
- `summary`: Short summary or title of the review.
- `unixReviewTime`: Review time in epoch seconds.

The target variable is `overall`, and all other fields are features.

### Dataset Locations
- Training dataset: `/datasets/amazon/train.json` (approx. 20 million records)
- Test dataset: `/datasets/amazon/test83m.json` (approx. 157 million records)

## Implementation

The solution consists of three main scripts:

1. `model.py` - Defines the model pipeline.
2. `train.py` - Contains the code for training the model.
3. `predict.py` - Contains the code for model inference.

### Model

The model should be a Spark ML pipeline that processes the input DataFrame without prior preprocessing (except for filling missing values). Use only standard classes from the Spark library.

The model definition should be in `model.py` and the pipeline variable should be named `pipeline`.

### Training

The training script `train.py` should accept the following arguments:
- Path to the training dataset (in HDFS)
- Path to save the trained model (in HDFS)

Import the model in your training script as follows:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')

from model import pipeline
```

Train the model and save it:
```python
pipeline_model = pipeline.fit(training_data)
pipeline_model.write().overwrite().save(model_path)
```

### Prediction

The prediction script `predict.py` should accept the following arguments:
- Path to the saved model (in HDFS)
- Path to the test dataset
- Path to save the predictions (in HDFS)

Load the model and perform predictions:
```python
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')

model = PipelineModel.load(model_path)
predictions = model.transform(test_data)
predictions.write.csv(output_path, header=True)
```

## Running the Scripts

### Training
```sh
PYSPARK_PYTHON=/opt/conda/envs/dsenv/bin/python spark3-submit \
    --master yarn \
    --name train_model \
    projects/4/train.py /datasets/amazon/train.json /path/to/save/model
```

### Prediction
```sh
PYSPARK_PYTHON=/opt/conda/envs/dsenv/bin/python spark3-submit \
    --master yarn \
    --name predict_model \
    projects/4/predict.py /path/to/saved/model /datasets/amazon/test83m.json /path/to/save/predictions
```