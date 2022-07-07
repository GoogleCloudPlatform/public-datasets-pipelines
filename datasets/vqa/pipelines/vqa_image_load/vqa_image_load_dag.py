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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="vqa.vqa_image_load",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run VQA images load processes
    load_images = kubernetes_pod.KubernetesPodOperator(
        task_id="load_images",
        name="vqa.load_annotations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.vqa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Load Images",
            "SOURCE_URL": '[\n  [\n    "Images Extraction (Testing Set)",\n    "http://images.cocodataset.org/zips/test2015.zip",\n    "{{ var.value.composer_bucket }}",\n    "data/vqa/images/testing"\n  ],\n  [\n    "Images Extraction (Training Set)",\n    "http://images.cocodataset.org/zips/train2014.zip",\n    "{{ var.value.composer_bucket }}",\n    "data/vqa/images/training"\n  ],\n  [\n    "Images Extraction (Validation Set)",\n    "http://images.cocodataset.org/zips/val2014.zip",\n    "{{ var.value.composer_bucket }}",\n    "data/vqa/images/validation"\n  ]\n]',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/vqa/data_output.csv",
        },
        resources={
            "request_ephemeral_storage": "32G",
            "limit_memory": "16G",
            "limit_cpu": "3",
        },
    )

    load_images
