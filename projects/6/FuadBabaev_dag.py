import json
import os

from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor


TRAIN_PATH="/datasets/amazon/amazon_extrasmall_train.json"
TRAIN_PATH_OUT="FuadBabaev_hw6_train_out"

TEST_PATH="/datasets/amazon/amazon_extrasmall_test.json"
TEST_PATH_OUT="FuadBabaev_hw6_test_out"

PRED_PATH="FuadBabaev_hw6_prediction"

dsenv="/opt/conda/envs/dsenv/bin/python"


with DAG(
    'FuadBabaev_dag',
    default_args={'retries': 0},
    description='hw6',
    schedule_interval=None,
    start_date=pendulum.datetime(2023, 1, 3, tz="UTC"),
    catchup=False
) as dag:
    
    base_dir = '{{ dag_run.conf["base_dir"] if dag_run else "" }}'

    feature_eng_train_task = SparkSubmitOperator(
          application=f"{base_dir}/feature_eng_task.py",
          application_args=["--path-in", TRAIN_PATH, "--path-out", TRAIN_PATH_OUT],
          task_id="feature_eng_train_task",
          spark_binary="/usr/bin/spark3-submit",
        )

    download_train_task = BashOperator(
         task_id='download_train_task',
         bash_command = f'pwd; echo \$USER; hdfs dfs -getmerge {TRAIN_PATH_OUT} {base_dir}/{TRAIN_PATH_OUT}_local'
    )


    from pathlib import Path
    train_task = BashOperator(
         task_id='train_task',
         bash_command=f'{dsenv} {base_dir}/train_task.py --train-in {base_dir}/{TRAIN_PATH_OUT}_local --sklearn-model-out {base_dir}/6.joblib'
    )

    model_sensor = FileSensor(
      task_id=f'model_sensor',
      filepath=f"{base_dir}/6.joblib",
      poke_interval=20,
      timeout=20 * 20,
    )

    feature_eng_test_task = SparkSubmitOperator(
          application=f"{base_dir}/feature_eng_task.py",
          application_args=["--path-in", TEST_PATH, "--path-out", TEST_PATH_OUT],
          task_id="feature_eng_test_task",
          spark_binary="/usr/bin/spark3-submit",
    )

    predict_task = SparkSubmitOperator(
          application=f"{base_dir}/predict.py",
          application_args=["--test-in", TEST_PATH_OUT, "--pred-out", PRED_PATH, "--sklearn-model-in", f"{base_dir}/6.joblib"],
          task_id="predict_task",
          spark_binary="/usr/bin/spark3-submit",
          files=f'{base_dir}/6.joblib',
          env_vars={"PYSPARK_PYTHON": dsenv}
    )
 

    feature_eng_train_task >> download_train_task >> train_task >> model_sensor >> feature_eng_test_task >> predict_task