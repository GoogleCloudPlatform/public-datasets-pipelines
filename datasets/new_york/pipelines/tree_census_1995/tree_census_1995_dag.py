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
    dag_id="new_york.tree_census_1995",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="tree_census_1995",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.run_csv_transform_kub_tree_census_1995 }}",
        env_vars={
            "SOURCE_URL": "https://data.cityofnewyork.us/api/views/kyad-zm4j/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york/tree_census_1995/data_output.csv",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/new_york/tree_census_1995/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="new_york.tree_census_1995",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "recordid", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "address", "type": "STRING", "mode": "NULLABLE"},
            {"name": "house_number", "type": "STRING", "mode": "NULLABLE"},
            {"name": "street", "type": "STRING", "mode": "NULLABLE"},
            {"name": "zip_original", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cb_original", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "site", "type": "STRING", "mode": "NULLABLE"},
            {"name": "species", "type": "STRING", "mode": "NULLABLE"},
            {"name": "diameter", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "status", "type": "STRING", "mode": "NULLABLE"},
            {"name": "wires", "type": "STRING", "mode": "NULLABLE"},
            {"name": "sidewalk_condition", "type": "STRING", "mode": "NULLABLE"},
            {"name": "support_structure", "type": "STRING", "mode": "NULLABLE"},
            {"name": "borough", "type": "STRING", "mode": "NULLABLE"},
            {"name": "x", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "y", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "cb_new", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "zip_new", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "censustract_2010", "type": "STRING", "mode": "NULLABLE"},
            {"name": "censusblock_2010", "type": "STRING", "mode": "NULLABLE"},
            {"name": "nta_2010", "type": "STRING", "mode": "NULLABLE"},
            {"name": "segmentid", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "spc_common", "type": "STRING", "mode": "NULLABLE"},
            {"name": "spc_latin", "type": "STRING", "mode": "NULLABLE"},
            {"name": "location", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    transform_csv >> load_to_bq
