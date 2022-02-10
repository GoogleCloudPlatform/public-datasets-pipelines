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
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="covid19_cds_eu.global_cases_by_province",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    global_cases_by_province_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="global_cases_by_province_transform_csv",
        startup_timeout_seconds=600,
        name="global_cases_by_province",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.covid19_cds_eu.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://coronadatascraper.com/timeseries.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/covid19_cds_eu/global_cases_by_province/data_output.csv",
            "PIPELINE_NAME": "global_cases_by_province",
            "CSV_HEADERS": '["name","level","date","city","county","state","country","population","latitude","longitude","aggregate","tz","cases","deaths","recovered","active","tested","hospitalized","discharged","growth_factor","url","location_geom"]',
            "RENAME_MAPPINGS": '{"lat":"latitude","long":"longitude","growthFactor":"growth_factor"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_global_cases_by_province_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_global_cases_by_province_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19_cds_eu/global_cases_by_province/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_cds_eu.global_cases_by_province",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "name", "type": "string", "description": "", "mode": "nullable"},
            {"name": "level", "type": "string", "description": "", "mode": "nullable"},
            {"name": "date", "type": "date", "description": "", "mode": "nullable"},
            {"name": "city", "type": "string", "description": "", "mode": "nullable"},
            {"name": "county", "type": "string", "description": "", "mode": "nullable"},
            {"name": "state", "type": "string", "description": "", "mode": "nullable"},
            {
                "name": "country",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "population",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "latitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "longitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "aggregate",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {"name": "tz", "type": "string", "description": "", "mode": "nullable"},
            {"name": "cases", "type": "integer", "description": "", "mode": "nullable"},
            {
                "name": "deaths",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "recovered",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "active",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "tested",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "hospitalized",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "discharged",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "growth_factor",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {"name": "url", "type": "string", "description": "", "mode": "nullable"},
            {
                "name": "location_geom",
                "type": "geography",
                "description": "",
                "mode": "nullable",
            },
        ],
    )

    global_cases_by_province_transform_csv >> load_global_cases_by_province_to_bq
