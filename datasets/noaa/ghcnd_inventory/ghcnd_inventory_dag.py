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
    dag_id="noaa.ghcnd_inventory",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="transform_csv",
        name="ghcnd_inventory",
        namespace="default",
        image_pull_policy="Always",
        startup_timeout_seconds=600,
        image="{{ var.json.noaa.container_registry.run_csv_transform_kub_ghcnd_inventory }}",
        env_vars={
            "SOURCE_URL": "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt",
            "FTP_HOST": "ftp.ncdc.noaa.gov",
            "FTP_DIR": "pub/data/ghcn/daily",
            "FTP_FILENAME": "ghcnd-inventory.txt",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/ghcn_inventory/ghcnd_inventory/data_output.csv",
        },
        resources={"limit_memory": "4G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/ghcn_d_inventory/ghcn_d_inventory/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="noaa.ghcnd_inventory",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "element", "type": "STRING", "mode": "NULLABLE"},
            {"name": "firstyear", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "lastyear", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    transform_csv >> load_to_bq
