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
    dag_id="bls.c_cpi_u",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        startup_timeout_seconds=600,
        name="c_cpi_u",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.bls.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URLS": '["gs://pdp-feeds-staging/Bureau/inflat_listarea_area_join.csv","gs://pdp-feeds-staging/Bureau/cu.item.tsv"]',
            "SOURCE_FILES": '["files/data1.csv","files/data2.tsv"]',
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/bls/c_cpi_u/data_output.csv",
            "PIPELINE_NAME": "c_cpi_u",
            "FILE_PATH": "files/",
            "JOINING_KEY": "item_code",
            "TRIM_SPACE": '["series_id","value","footnote_codes","item_code"]',
            "CSV_HEADERS": '["series_id","year","period","value","footnote_codes","survey_abbreviation","seasonal_code","periodicity_code","area_code","area_name","item_code","item_name","date"]',
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/bls/c_cpi_u/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="bls.c_cpi_u",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "series_id", "type": "STRING", "mode": "required"},
            {"name": "year", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "period", "type": "STRING", "mode": "NULLABLE"},
            {"name": "value", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "footnote_codes", "type": "STRING", "mode": "NULLABLE"},
            {"name": "survey_abbreviation", "type": "STRING", "mode": "NULLABLE"},
            {"name": "seasonal_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "periodicity_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "area_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "area_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "item_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "item_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "date", "type": "DATE", "mode": "NULLABLE"},
        ],
    )

    transform_csv >> load_to_bq
