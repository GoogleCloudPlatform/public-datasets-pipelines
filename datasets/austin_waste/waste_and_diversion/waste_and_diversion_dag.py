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
    dag_id="austin_waste.waste_and_diversion",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    austin_waste_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_waste_transform_csv",
        startup_timeout_seconds=600,
        name="austin_waste",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.austin_waste.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.austintexas.gov/api/views/mbnu-4wq9/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_waste/waste_and_diversion/data_output.csv",
            "CSV_HEADERS": '[ "load_id", "report_date", "load_type", "load_time", "load_weight", "dropoff_site", "route_type", "route_number"]',
            "RENAME_MAPPINGS": '{"Load ID": "load_id","Report Date": "report_date","Load Type": "load_type","Load Time": "load_time","Load Weight": "load_weight","Dropoff Site": "dropoff_site","Route Type": "route_type","Route Number": "route_number"}',
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_austin_waste_and_diversion_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_austin_waste_and_diversion_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/austin_waste/waste_and_diversion/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="austin_waste.waste_and_diversion",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "load_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "report_date", "type": "DATE", "mode": "NULLABLE"},
            {"name": "load_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "load_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "load_weight", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "dropoff_site", "type": "STRING", "mode": "NULLABLE"},
            {"name": "route_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "route_number", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    austin_waste_transform_csv >> load_austin_waste_and_diversion_to_bq
