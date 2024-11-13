# Copyright 2022 Google LLC
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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="mnist.mnist",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "pdp-mnist",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Task to copy `t10k-images-idx3-ubyte.gz` from MNIST  Database to GCS
    download_and_process_source_zip_file = kubernetes_engine.GKEStartPodOperator(
        task_id="download_and_process_source_zip_file",
        name="mnist",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-mnist",
        image_pull_policy="Always",
        image="{{ var.json.mnist.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
            "SOURCE_FILE": "files/t10k-images-idx3-ubyte.gz",
            "TARGET_FILE": "files/t10k-images-idx3-ubyte.gz",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/mnist/mnist/t10k-images-idx3-ubyte.gz",
            "PIPELINE_NAME": "mnist",
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to copy `train-images-idx3-ubyte.gz` from MNIST  Database to GCS
    download_and_process_source_zip_file_2 = kubernetes_engine.GKEStartPodOperator(
        task_id="download_and_process_source_zip_file_2",
        name="mnist",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-mnist",
        image_pull_policy="Always",
        image="{{ var.json.mnist.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
            "SOURCE_FILE": "files/train-images-idx3-ubyte.gz",
            "TARGET_FILE": "files/train-images-idx3-ubyte.gz",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/mnist/mnist/train-images-idx3-ubyte.gz",
            "PIPELINE_NAME": "mnist",
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to copy `train-labels-idx1-ubyte.gz` from MNIST  Database to GCS
    download_and_process_source_zip_file_3 = kubernetes_engine.GKEStartPodOperator(
        task_id="download_and_process_source_zip_file_3",
        name="mnist",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-mnist",
        image_pull_policy="Always",
        image="{{ var.json.mnist.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
            "SOURCE_FILE": "files/train-labels-idx1-ubyte.gz",
            "TARGET_FILE": "files/train-labels-idx1-ubyte.gz",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/mnist/mnist/train-labels-idx1-ubyte.gz",
            "PIPELINE_NAME": "mnist",
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )

    # Task to copy `t10k-labels-idx1-ubyte.gz` from MNIST  Database to GCS
    download_and_process_source_zip_file_4 = kubernetes_engine.GKEStartPodOperator(
        task_id="download_and_process_source_zip_file_4",
        name="mnist",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="pdp-mnist",
        image_pull_policy="Always",
        image="{{ var.json.mnist.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
            "SOURCE_FILE": "files/t10k-labels-idx1-ubyte.gz",
            "TARGET_FILE": "files/t10k-labels-idx1-ubyte.gz",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/mnist/mnist/t10k-labels-idx1-ubyte.gz",
            "PIPELINE_NAME": "mnist",
        },
        container_resources={
            "memory": {"request": "16Gi"},
            "cpu": {"request": "1"},
            "ephemeral-storage": {"request": "10Gi"},
        },
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="pdp-mnist",
    )

    (
        create_cluster
        >> download_and_process_source_zip_file
        >> download_and_process_source_zip_file_2
        >> download_and_process_source_zip_file_3
        >> download_and_process_source_zip_file_4
        >> delete_cluster
    )
