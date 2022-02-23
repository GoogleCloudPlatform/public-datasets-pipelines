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
    dag_id="city_health_dashboard.chdb_data_tract_all",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    data_tract_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="data_tract_transform_csv",
        startup_timeout_seconds=600,
        name="city_health_dashboard_chdb_data_tract_all",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.city_health_dashboard.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.cityhealthdashboard.com/drupal/media/23/download",
            "SOURCE_FILE": "files/data.zip",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/city_health_dashboard/chdb_data_tract_all/data_output.csv",
            "CSV_HEADERS": '["state_abbr","state_fips","county_fips","county_name","tract_code","stcotr_fips","stpl_fips","city_name","metric_name","metric_number","group_name","group_number","num","denom","est","lci","uci","data_yr_type","geo_level","date_export"]',
            "RENAME_MAPPINGS": '{"state_abbr": "state_abbr","state_fips": "state_fips","county_fips": "county_fips","county_name": "county_name","tract_code": "tract_code","stcotr_fips": "stcotr_fips","stpl_fips": "stpl_fips","city_name": "city_name","metric_name": "metric_name","metric_number": "metric_number","group_name": "group_name","group_number": "group_number","num": "num","denom": "denom","est": "est","lci": "lci","uci": "uci","data_yr_type": "data_yr_type","geo_level": "geo_level","date_export": "date_export"}',
            "PIPELINE_NAME": "chdb_data_tract_all",
            "FILE_NAME": "CHDB_data_tract_all_v13.1.csv",
        },
        resources={
            "limit_memory": "2G",
            "limit_cpu": "1",
            "request_ephemeral_storage": "8G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_data_tract_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_data_tract_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/city_health_dashboard/chdb_data_tract_all/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="city_health_dashboard.chdb_data_tract_all",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "state_abbr", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_fips", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "county_fips", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "county_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "tract_code", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "stcotr_fips", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "stpl_fips", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "city_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "metric_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "metric_number", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "group_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "group_number", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "num", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "denom", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "est", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "lci", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "uci", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "data_yr_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "geo_level", "type": "STRING", "mode": "NULLABLE"},
            {"name": "date_export", "type": "DATE", "mode": "NULLABLE"},
        ],
    )

    data_tract_transform_csv >> load_data_tract_to_bq
