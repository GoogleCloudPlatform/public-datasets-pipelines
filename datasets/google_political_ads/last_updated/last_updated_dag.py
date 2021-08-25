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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="google_political_ads.last_updated",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    last_updated_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="last_updated_transform_csv",
        startup_timeout_seconds=600,
        name="last_updated",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.google_political_ads.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip",
            "SOURCE_FILE": "files/data.zip",
            "FILE_NAME": "google-political-ads-transparency-bundle/google-political-ads-updated*",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/google_political_ads/last_updated/data_output.csv",
            "PIPELINE_NAME": "last_updated",
            "CSV_HEADERS": '["report_data_updated_date"]',
            "RENAME_MAPPINGS": '{"Report_Data_Updated_Date": "report_data_updated_date"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_last_updated_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_last_updated_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/google_political_ads/last_updated/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_political_ads.last_updated",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "report_data_updated_date",
                "type": "Date",
                "description": "The date the report data was most reecntly updated",
                "mode": "nullable",
            }
        ],
    )

    last_updated_transform_csv >> load_last_updated_to_bq
