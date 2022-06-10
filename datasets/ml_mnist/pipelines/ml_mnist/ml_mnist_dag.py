# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.operators import bash

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-06-09",
}


with DAG(
    dag_id="ml_mnist.mswc",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `train-images-idx3-ubyte.gz` from MNIST Database to GCS
    download_and_process_source_zip_file = bash.BashOperator(
        task_id="download_and_process_source_zip_file",
        bash_command="mkdir -p $data_dir/{{ ds }}\ncurl -o $data_dir/{{ ds }}/namesbystate.zip -L $zip_source_url\n",
        env={
            "zip_source_url": "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
            "data_dir": "/home/airflow/gcs/data/mnist/train_images",
        },
    )

    # Task to copy `t10k-images-idx3-ubyte.gz` from MNIST  Database to GCS
    download_and_process_source_zip_file = bash.BashOperator(
        task_id="download_and_process_source_zip_file",
        bash_command="mkdir -p $data_dir/{{ ds }}\ncurl -o $data_dir/{{ ds }}/namesbystate.zip -L $zip_source_url\n",
        env={
            "zip_source_url": "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
            "data_dir": "/home/airflow/gcs/data/mnist/test_images",
        },
    )

    download_and_process_source_zip_file
