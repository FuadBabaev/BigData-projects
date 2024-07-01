from pyspark.sql.types import *
from pyspark.ml.feature import *
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline


tokenizer_review = Tokenizer(inputCol="reviewText", outputCol="words_review")
hasher_review = HashingTF(numFeatures=100, inputCol="words_review", outputCol="review_vector")
assembler = VectorAssembler(inputCols=["review_vector"],outputCol="features")
lr = LinearRegression(regParam=0.0, labelCol='overall', featuresCol='features')

pipeline = Pipeline(stages = [
    tokenizer_review,
    hasher_review,
    assembler,
    lr
])