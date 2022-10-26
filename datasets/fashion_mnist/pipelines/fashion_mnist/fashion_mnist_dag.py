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
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="fashion_mnist.fashion_mnist",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `fashion-mnist.gz` from FASHION MNIST Database to GCS
    download_zip_files = bash.BashOperator(
        task_id="download_zip_files",
        bash_command="mkdir -p $data_dir/fashion-mnist\ncurl -o $data_dir/fashion-mnist/t10k-images-idx3-ubyte.gz -L $fashion_mnist_test\ncurl -o $data_dir/fashion-mnist/train-images-idx3-ubyte.gz -L $fashion_mnist_train\ncurl -o $data_dir/fashion-mnist/train-labels-idx1-ubyte.gz -L $fashion_mnist_train_labels\ncurl -o $data_dir/fashion-mnist/t10k-labels-idx1-ubyte.gz -L $fashion_mnist_test_labels\n",
        env={
            "data_dir": "/home/airflow/gcs/data/fashion-mnist",
            "fashion_mnist_test": "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz",
            "fashion_mnist_train": "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz",
            "fashion_mnist_train_labels": "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz",
            "fashion_mnist_test_labels": "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz",
        },
    )

    download_zip_files
