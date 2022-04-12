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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-12-30",
}


with DAG(
    dag_id="noaa.gsod_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="gsod_stations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.noaa_gsod_stations.container_registry.run_csv_transform_kub_gsod_stations }}",
        env_vars={
            "SOURCE_URL": "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.txt",
            "FTP_HOST": "ftp.ncdc.noaa.gov",
            "FTP_DIR": "/pub/data/noaa",
            "FTP_FILENAME": "isd-history.txt",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/noaa/gsod_stations/data_output.csv",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/noaa/gsod_stations/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="noaa.gsod_stations",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "usaf", "type": "STRING", "mode": "NULLABLE"},
            {"name": "wban", "type": "STRING", "mode": "NULLABLE"},
            {"name": "name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "country", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state", "type": "STRING", "mode": "NULLABLE"},
            {"name": "call", "type": "STRING", "mode": "NULLABLE"},
            {"name": "lat", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "lon", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "elev", "type": "STRING", "mode": "NULLABLE"},
            {"name": "begin", "type": "STRING", "mode": "NULLABLE"},
            {"name": "end", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    transform_csv >> load_to_bq
