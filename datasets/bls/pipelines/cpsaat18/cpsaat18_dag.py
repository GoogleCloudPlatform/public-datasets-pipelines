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
    "start_date": "2021-06-23",
}


with DAG(
    dag_id="bls.cpsaat18",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load the CPSAAT18 data to the BigQuery table
    load_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_csv_to_bq",
        bucket="{{ var.json.bls.source_bucket }}",
        source_objects=["cpsaat18/2021.csv"],
        source_format="CSV",
        destination_project_dataset_table="bls.cpsaat18",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "year", "type": "integer", "nullable": False},
            {"name": "sector", "type": "string", "nullable": False},
            {"name": "subsector", "type": "string", "nullable": True},
            {"name": "industry_group", "type": "string", "nullable": True},
            {"name": "industry", "type": "string", "nullable": True},
            {
                "name": "total_employed_in_thousands",
                "type": "integer",
                "nullable": True,
            },
            {"name": "percent_women", "type": "float", "nullable": True},
            {"name": "percent_white", "type": "float", "nullable": True},
            {
                "name": "percent_black_or_african_american",
                "type": "float",
                "nullable": True,
            },
            {"name": "percent_asian", "type": "float", "nullable": True},
            {"name": "percent_hispanic_or_latino", "type": "float", "nullable": True},
        ],
    )

    load_csv_to_bq
