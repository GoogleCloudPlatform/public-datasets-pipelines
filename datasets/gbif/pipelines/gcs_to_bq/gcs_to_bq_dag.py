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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-03-31",
}


with DAG(
    dag_id="gbif.gcs_to_bq",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 0 2 * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Load Parquet files to BQ
    load_parquet_files_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_parquet_files_to_bq",
        bucket="{{ var.json.gbif.source_bucket }}",
        source_objects=[
            "occurrence/{{ execution_date.strftime('%Y-%m-01') }}/occurrence.parquet/*"
        ],
        source_format="PARQUET",
        destination_project_dataset_table="gbif.occurrences",
        write_disposition="WRITE_TRUNCATE",
    )

    load_parquet_files_to_bq
