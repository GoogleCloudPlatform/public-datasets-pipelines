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
from airflow.operators import bash_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="austin_311.311_service_requests",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Download source CSV file for austin 311 service requests data table
    austin_311_service_requests_download_csv = bash_operator.BashOperator(
        task_id="austin_311_service_requests_download_csv",
        bash_command="mkdir -p $airflow_home/data/$dataset/$pipeline\ncurl -o $airflow_home/data/$dataset/$pipeline/data.csv -L $csv_source_url\n",
        env={
            "airflow_home": "{{ var.json.shared.airflow_home }}",
            "dataset": "austin_311",
            "pipeline": "311_service_requests",
            "csv_source_url": "https://data.austintexas.gov/api/views/i26j-ai4z/rows.csv?accessType=DOWNLOAD",
        },
    )

    # Run CSV transform within kubernetes pod
    austin_311_service_requests_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="austin_311_service_requests_transform_csv",
        name="ren_header_conv_dt_fmt",
        namespace="default",
        image="{{ var.json.austin_311.container_registry.austin_311__ren_hdrs_conv_dt }}",
        env_vars={
            "SOURCE_FILE": "{{ var.json.shared.airflow_home }}/data/austin_311/311_service_requests/data.csv",
            "TARGET_FILE": "{{ var.json.shared.airflow_home }}/data/austin_311/311_service_requests/data_output.csv",
        },
        resources={"limit_memory": "1G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_austin_311_service_requests_to_bq = (
        gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
            task_id="load_austin_311_service_requests_to_bq",
            bucket="{{ var.json.shared.composer_bucket }}",
            source_objects=["data/austin_311/311_service_requests/data_output.csv"],
            source_format="CSV",
            destination_project_dataset_table="austin_311.311_service_requests",
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
                {
                    "name": "state_plane_x_coordinate",
                    "type": "STRING",
                    "mode": "NULLABLE",
                },
                {
                    "name": "state_plane_y_coordinate",
                    "type": "FLOAT",
                    "mode": "NULLABLE",
                },
                {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
                {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
                {"name": "location", "type": "STRING", "mode": "NULLABLE"},
                {
                    "name": "council_district_code",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {"name": "map_page", "type": "STRING", "mode": "NULLABLE"},
                {"name": "map_tile", "type": "STRING", "mode": "NULLABLE"},
            ],
        )
    )

    austin_311_service_requests_download_csv >> austin_311_service_requests_transform_csv
    austin_311_service_requests_transform_csv >> load_austin_311_service_requests_to_bq
