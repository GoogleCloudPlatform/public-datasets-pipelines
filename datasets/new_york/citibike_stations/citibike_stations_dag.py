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
    dag_id="new_york.citibike_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    new_york_citibike_stations_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="new_york_citibike_stations_transform_csv",
        name="citibike_stations",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york_citibike_stations.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://gbfs.citibikenyc.com/gbfs/en/station_information.json|https://gbfs.citibikenyc.com/gbfs/en/station_status.json",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york_citibike_stations/citibike_stations/data_output.csv",
        },
        resources={"limit_memory": "4G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_new_york_citibike_stations_to_bq = (
        gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
            task_id="load_new_york_citibike_stations_to_bq",
            bucket="{{ var.json.shared.composer_bucket }}",
            source_objects=[
                "data/new_york_citibike_stations/citibike_stations/data_output.csv"
            ],
            source_format="CSV",
            destination_project_dataset_table="new_york_citibike.citibike_stations",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            schema_fields=None,
        )
    )

    new_york_citibike_stations_transform_csv >> load_new_york_citibike_stations_to_bq
