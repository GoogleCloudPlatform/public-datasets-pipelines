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
    dag_id="austin.311_service_requests",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="transform_csv",
        image_pull_policy="Always",
        name="austin",
        namespace="default",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub_311_service_requests }}",
        env_vars={
            "SOURCE_URL": "https://data.austintexas.gov/api/views/i26j-ai4z/rows.csv",
            "SOURCE_FILE": "/custom/data.csv",
            "TARGET_FILE": "/custom/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/311_service_requests/data_output.csv",
        },
        resources={"request_memory": "4G", "request_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/austin_311/311_service_requests/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="austin.311_service_requests",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "unique_key", "type": "STRING", "mode": "NULLABLE"},
            {"name": "complaint_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "complaint_description", "type": "STRING", "mode": "NULLABLE"},
            {"name": "owning_department", "type": "STRING", "mode": "NULLABLE"},
            {"name": "source", "type": "STRING", "mode": "NULLABLE"},
            {"name": "status", "type": "STRING", "mode": "NULLABLE"},
            {"name": "status_change_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "created_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "last_update_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "close_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "incident_address", "type": "STRING", "mode": "NULLABLE"},
            {"name": "street_number", "type": "STRING", "mode": "NULLABLE"},
            {"name": "street_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "city", "type": "STRING", "mode": "NULLABLE"},
            {"name": "incident_zip", "type": "STRING", "mode": "NULLABLE"},
            {"name": "county", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_plane_x_coordinate", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_plane_y_coordinate", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "location", "type": "STRING", "mode": "NULLABLE"},
            {"name": "council_district_code", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "map_page", "type": "STRING", "mode": "NULLABLE"},
            {"name": "map_tile", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    transform_csv >> load_to_bq
