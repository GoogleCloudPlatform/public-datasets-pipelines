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
from airflow.providers.google.cloud.operators import kubernetes_engine
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="new_york.311_service_requests",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "new-york--311-service-requests",
            "initial_node_count": 1,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_engine.GKEStartPodOperator(
        task_id="transform_csv",
        name="311_service_requests",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="new-york--311-service-requests",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.new_york.container_registry.311_service_requests.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "{{ var.json.new_york.container_registry.311_service_requests.source_url }}",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "{{ var.json.new_york.container_registry.311_service_requests.chunksize }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.new_york.container_registry.311_service_requests.target_path }}",
        },
        resources={"limit_memory": "16G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "{{ var.json.new_york.container_registry.311_service_requests.target_path }}"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.new_york.container_registry.311_service_requests.destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "unique_key",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "created_date",
                "type": "TIMESTAMP",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "closed_date",
                "type": "TIMESTAMP",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "agency", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "agency_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "complaint_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "descriptor",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "location_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "incident_zip",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "incident_address",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "street_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "cross_street_1",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "cross_street_2",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "intersection_street_1",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "intersection_street_2",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "address_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "city", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "landmark",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "facility_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "status", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "due_date",
                "type": "TIMESTAMP",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "resolution_description",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "resolution_action_updated_date",
                "type": "TIMESTAMP",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "community_board",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "borough",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "x_coordinate",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "y_coordinate",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "park_facility_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "park_borough",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "bbl", "type": "INTEGER", "description": "", "mode": "NULLABLE"},
            {
                "name": "open_data_channel_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "vehicle_type",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "taxi_company_borough",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "taxi_pickup_location",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "bridge_highway_name",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "bridge_highway_direction",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "road_ramp",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "bridge_highway_segment",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "latitude",
                "type": "FLOAT",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "longitude",
                "type": "FLOAT",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "location",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="new-york--311-service-requests",
    )

    create_cluster >> transform_csv >> load_to_bq >> delete_cluster
