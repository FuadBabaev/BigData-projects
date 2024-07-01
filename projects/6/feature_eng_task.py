import os
import sys
import argparse


# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
parser = argparse.ArgumentParser()

parser.add_argument("--path-in", dest="path_in", type=str)
parser.add_argument("--path-out", dest="path_out", type=str)

args = parser.parse_args()

SPARK_HOME = "/usr/lib/spark3"
PYSPARK_PYTHON = "/opt/conda/envs/dsenv/bin/python"
os.environ["PYSPARK_PYTHON"]= PYSPARK_PYTHON
os.environ["PYSPARK_DRIVER_PYTHON"]= PYSPARK_PYTHON
os.environ["SPARK_HOME"] = SPARK_HOME

PYSPARK_HOME = os.path.join(SPARK_HOME, "python/lib")
sys.path.insert(0, os.path.join(PYSPARK_HOME, "py4j-0.10.9.5-src.zip"))
sys.path.insert(0, os.path.join(PYSPARK_HOME, "pyspark.zip"))

from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()

spark = SparkSession.builder.config(conf=conf).appName("Spark SQL").getOrCreate()


train = spark.read.json(args.path_in).fillna( {"reviewText": "missingreview"})

if "label" in train.columns:
    tmp_table = train.select("label", "reviewText", "id")
else:
    tmp_table = train.select("reviewText", "id")
    

tmp_table.write.mode("overwrite").json(args.path_out)