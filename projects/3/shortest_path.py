import os
import sys

SPARK_HOME = "/usr/lib/spark3"
PYSPARK_PYTHON = "/opt/conda/envs/dsenv/bin/python"
os.environ["PYSPARK_PYTHON"]= PYSPARK_PYTHON
os.environ["PYSPARK_DRIVER_PYTHON"]= PYSPARK_PYTHON
os.environ["SPARK_HOME"] = SPARK_HOME

PYSPARK_HOME = os.path.join(SPARK_HOME, "python/lib")
sys.path.insert(0, os.path.join(PYSPARK_HOME, "py4j-0.10.9.3-src.zip"))
sys.path.insert(0, os.path.join(PYSPARK_HOME, "pyspark.zip"))

# make session

from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()
spark = SparkSession.builder.config(conf=conf).appName("Pagerank").getOrCreate()

from pyspark.sql.types import StructType, StructField, IntegerType, ArrayType

small = '/datasets/twitter/twitter_sample_small.tsv'
sample = '/datasets/twitter/twitter_sample.tsv'
full = '/datasets/twitter/twitter.tsv'

# Input data
v_from = int(sys.argv[1])
v_to = int(sys.argv[2])
dataset_path = sys.argv[3]

# load source dataset
graph = spark.read.csv(
    dataset_path, sep="\t", schema=
        StructType([
            StructField("user_id", IntegerType(), False),
            StructField("follower_id", IntegerType(), False)
        ])
)       
graph.cache()    # Optimization (as decorator cache)

collected_data = spark.createDataFrame(
    [(v_from, 0, [])], schema=
        StructType([
            StructField("vertex", IntegerType(), False),
            StructField("distance", IntegerType(), False),
            StructField("path", ArrayType(IntegerType()), False),
        ])
)

import pyspark.sql.functions as F


d = 0

# BFS algorithm
while True:
    forefront = (
        collected_data
            .join(graph, on=(collected_data.vertex==graph.follower_id))
            .cache()
    ) 
    forefront = (
        forefront.select(
            forefront['user_id'].alias("vertex"),
            (collected_data['distance'] + 1).alias("distance"),
            F.concat(forefront["path"], F.array(forefront["vertex"])).alias('path')
        )
    )
    with_newly_added = (
        collected_data
            .join(forefront, on="vertex", how="full_outer")
            .select(
                "vertex",
                F.when(collected_data.distance.isNotNull(), collected_data.distance)
                    .otherwise(forefront.distance) # `null` means it's a new record, we need to add it
                    .alias("distance"),
            )
            .persist()
    )

    count = with_newly_added.where(with_newly_added.distance == d + 1).count()

    if count == 0:
        break  

    d += 1            
    collected_data = forefront
    target = with_newly_added.where(with_newly_added.vertex == v_to).count()

    if target > 0:
        print('steps made:', d)
        break

ans = (
    collected_data
        .where(collected_data.vertex == v_to)
        .withColumn('last', F.lit(v_to))
        .select(
            F.concat_ws(',', F.concat("path", F.array("last"))).alias('path')
        )
)

ans.select('path').write.text(sys.argv[4])