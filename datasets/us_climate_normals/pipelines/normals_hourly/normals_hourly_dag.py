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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="us_climate_normals.normals_hourly",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 */6 * * *",
    catchup=False,
    default_view="graph",
) as dag:
    hourly_load_current_AQW = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="hourly_load_current_AQW",
        bucket="normals",
        source_objects=["normals-hourly/access/AQW*.csv"],
        destination_project_dataset_table="us_climate_normals.normals_hourly_AQW",
        schema_object="gs://{{ var.value.composer_bucket }}/data/us_climate_normals/schema/normals_hourly_schema.json",
        source_format="CSV",
        skip_leading_rows=1,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
    )
    hourly_load_historical_AQW = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="hourly_load_historical_AQW",
        bucket="normals",
        source_objects=[
            "normals-hourly/1981-2010/access/AQW*.csv",
            "normals-hourly/1991-2010/access/AQW*.csv",
            "normals-hourly/2006-2020/access/AQW*.csv",
        ],
        destination_project_dataset_table="us_climate_normals.normals_hourly_AQW",
        schema_update_options=["ALLOW_FIELD_ADDITION"],
        source_format="CSV",
        skip_leading_rows=1,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
    )

    hourly_load_current_AQW >> hourly_load_historical_AQW
