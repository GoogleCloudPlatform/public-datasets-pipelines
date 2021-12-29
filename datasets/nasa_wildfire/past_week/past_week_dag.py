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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="nasa_wildfire.past_week",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    past_week_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="past_week_transform_csv",
        startup_timeout_seconds=600,
        name="past_week",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.nasa_wildfire.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_Global_7d.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nasa_wildfire/past_week/data_output.csv",
            "PIPELINE_NAME": "past_week",
            "CSV_HEADERS": '["latitude","longitude","bright_ti4","scan","track","acq_date","acq_time","satellite","confidence","version","bright_ti5","frp","daynight"]',
            "RENAME_MAPPINGS": '{"latitude":"latitude","longitude":"longitude","bright_ti4":"bright_ti4","scan":"scan","track":"track","acq_date":"acq_date","acq_time":"acq_time","satellite":"satellite","confidence":"confidence","version":"version","bright_ti5":"bright_ti5","frp":"frp","daynight":"daynight"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_past_week_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_past_week_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nasa_wildfire/past_week/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="nasa_wildfire.past_week",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    past_week_transform_csv >> load_past_week_to_bq
