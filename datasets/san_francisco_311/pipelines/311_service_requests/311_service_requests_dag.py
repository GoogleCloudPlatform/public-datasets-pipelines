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
    dag_id="san_francisco_311.311_service_requests",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="311_service_requests",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_311.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.sfgov.org/api/views/vw6y-z8j6/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_311/311_service_requests/data_output.csv",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/san_francisco_311/311_service_requests/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="san_francisco_311.311_service_requests",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "unique_key",
                "type": "INTEGER",
                "description": "Unique case id",
                "mode": "REQUIRED",
            },
            {
                "name": "created_date",
                "type": "TIMESTAMP",
                "description": "The date and time when the service request was made",
                "mode": "NULLABLE",
            },
            {
                "name": "closed_date",
                "type": "TIMESTAMP",
                "description": "The date and time when the service request was closed",
                "mode": "NULLABLE",
            },
            {
                "name": "resolution_action_updated_date",
                "type": "TIMESTAMP",
                "description": "The date and time when the service request was last modified. For requests with status=closed, this will be the date the request was closed",
                "mode": "NULLABLE",
            },
            {
                "name": "status",
                "type": "STRING",
                "description": "The current status of the service request.",
                "mode": "NULLABLE",
            },
            {
                "name": "status_notes",
                "type": "STRING",
                "description": "Explanation of why status was changed to current state or more details on current status than conveyed with status alone",
                "mode": "NULLABLE",
            },
            {
                "name": "agency_name",
                "type": "STRING",
                "description": "The agency responsible for fulfilling or otherwise addressing the service request.",
                "mode": "NULLABLE",
            },
            {
                "name": "category",
                "type": "STRING",
                "description": "The Human readable name of the specific service request type (service_name)",
                "mode": "NULLABLE",
            },
            {
                "name": "complaint_type",
                "type": "STRING",
                "description": "More specific description of the problem related to the Category",
                "mode": "NULLABLE",
            },
            {
                "name": "descriptor",
                "type": "STRING",
                "description": "More specific description of the problem related to the Request Type",
                "mode": "NULLABLE",
            },
            {
                "name": "incident_address",
                "type": "STRING",
                "description": "Human readable address or description of location",
                "mode": "NULLABLE",
            },
            {
                "name": "supervisor_district",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "neighborhood",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "location",
                "type": "STRING",
                "description": "Latitude and longitude using the (WGS84) projection.",
                "mode": "NULLABLE",
            },
            {
                "name": "source",
                "type": "STRING",
                "description": "How the service request was made",
                "mode": "NULLABLE",
            },
            {
                "name": "media_url",
                "type": "STRING",
                "description": "Website URL",
                "mode": "NULLABLE",
            },
            {
                "name": "latitude",
                "type": "FLOAT",
                "description": "Latitude using the (WGS84) projection.",
                "mode": "NULLABLE",
            },
            {
                "name": "longitude",
                "type": "FLOAT",
                "description": "Longitude using the (WGS84) projection.",
                "mode": "NULLABLE",
            },
            {
                "name": "police_district",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
