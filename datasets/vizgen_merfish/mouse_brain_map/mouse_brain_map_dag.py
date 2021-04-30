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
from airflow.contrib.operators import gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-04-01",
}


with DAG(
    dag_id="vizgen_merfish.mouse_brain_map",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a GoogleCloudStorageToGoogleCloudStorageOperator
    copy_data_to_gcs_destination_bucket = (
        gcs_to_gcs.GoogleCloudStorageToGoogleCloudStorageOperator(
            task_id="copy_data_to_gcs_destination_bucket",
            source_bucket="vizgen-brain-map",
            source_object="BrainReceptorShowcase/*",
            destination_bucket="{{ var.json.vizgen_merfish.destination_bucket }}",
            destination_object="datasets/mouse_brain_map/BrainReceptorShowcase/",
            move_object=False,
        )
    )

    copy_data_to_gcs_destination_bucket
