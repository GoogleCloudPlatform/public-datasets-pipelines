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
from airflow.providers.google.cloud.transfers import gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-09-01",
}


with DAG(
    dag_id="noaa_passive_bioacoustic.noaa_passive_bioacoustic",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy objects from source bucket
    gcs_to_gcs = gcs_to_gcs.GCSToGCSOperator(
        task_id="gcs_to_gcs",
        source_bucket="{{ var.json.noaa_passive_bioacoustic.source_bucket }}",
        source_object="{{ var.json.noaa_passive_bioacoustic.source_object }}",
        destination_bucket="{{ var.json.noaa_passive_bioacoustic.destination_bucket }}",
        destination_object="{{ var.json.noaa_passive_bioacoustic.destination_object }}",
        move_object=False,
        replace=False,
    )

    gcs_to_gcs
