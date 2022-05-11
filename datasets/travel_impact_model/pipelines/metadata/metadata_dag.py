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
    "start_date": "2021-01-09",
}


with DAG(
    dag_id="travel_impact_model.metadata",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 15 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    metadata_gcs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="metadata_gcs_to_bq",
        bucket="{{ var.json.travel_impact_model.source_bucket }}",
        source_objects=["metadata.csv"],
        source_format="CSV",
        destination_project_dataset_table="travel_impact_model.metadata",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "key",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "Key of the entry",
            },
            {
                "name": "value",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "Value of the entry",
            },
        ],
    )

    metadata_gcs_to_bq
