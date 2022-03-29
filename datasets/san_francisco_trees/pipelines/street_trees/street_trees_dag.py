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
    dag_id="san_francisco_trees.street_trees",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    street_trees_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="street_trees_transform_csv",
        startup_timeout_seconds=600,
        name="street_trees",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_trees.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.sfgov.org/api/views/tkzw-k3nq/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_trees/street_trees/data_output.csv",
            "PIPELINE_NAME": "street_trees",
            "CSV_HEADERS": '["tree_id","legal_status","species","address","site_order","site_info","plant_type","care_taker","care_assistant","plant_date","dbh","plot_size","permit_notes","x_coordinate","y_coordinate","latitude","longitude","location"]',
            "RENAME_MAPPINGS": '{"TreeID" : "tree_id" ,"qLegalStatus" : "legal_status" ,"qSpecies" : "species" ,"qAddress" : "address" ,"SiteOrder" : "site_order" ,"qSiteInfo" : "site_info" ,"PlantType" : "plant_type" ,"qCaretaker" : "care_taker" ,"qCareAssistant" : "care_assistant" ,"PlantDate" : "plant_date" ,"DBH" : "dbh" ,"PlotSize" : "plot_size" ,"PermitNotes" : "permit_notes" ,"XCoord" : "x_coordinate" ,"YCoord" : "y_coordinate" ,"Latitude" : "latitude" ,"Longitude" : "longitude" ,"Location" : "location"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_street_trees_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_street_trees_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/san_francisco_trees/street_trees/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="san_francisco_trees.street_trees",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tree_id",
                "type": "integer",
                "description": "Unique ID for Tree",
                "mode": "required",
            },
            {
                "name": "legal_status",
                "type": "string",
                "description": "Legal staus: Permitted or DPW maintained",
                "mode": "nullable",
            },
            {
                "name": "species",
                "type": "string",
                "description": "Species of tree",
                "mode": "nullable",
            },
            {
                "name": "address",
                "type": "string",
                "description": "Address of Tree",
                "mode": "nullable",
            },
            {
                "name": "site_order",
                "type": "integer",
                "description": "Order of tree at address where multiple trees are at same address. Trees are ordered in ascending address order",
                "mode": "nullable",
            },
            {
                "name": "site_info",
                "type": "string",
                "description": "Description of location of tree",
                "mode": "nullable",
            },
            {
                "name": "plant_type",
                "type": "string",
                "description": "Landscaping or Tree",
                "mode": "nullable",
            },
            {
                "name": "care_taker",
                "type": "string",
                "description": "Agency or person that is primary caregiver to tree. Owner of Tree",
                "mode": "nullable",
            },
            {
                "name": "care_assistant",
                "type": "string",
                "description": "Agency or person that is secondary caregiver to tree",
                "mode": "nullable",
            },
            {
                "name": "plant_date",
                "type": "timestamp",
                "description": "Date tree was planted",
                "mode": "nullable",
            },
            {
                "name": "dbh",
                "type": "string",
                "description": "depth height",
                "mode": "nullable",
            },
            {
                "name": "plot_size",
                "type": "string",
                "description": "dimension of tree plot",
                "mode": "nullable",
            },
            {
                "name": "permit_notes",
                "type": "string",
                "description": "Tree permit number reference",
                "mode": "nullable",
            },
            {
                "name": "x_coordinate",
                "type": "float",
                "description": "CA State Plane III",
                "mode": "nullable",
            },
            {
                "name": "y_coordinate",
                "type": "float",
                "description": "CA State Plane III",
                "mode": "nullable",
            },
            {
                "name": "latitude",
                "type": "float",
                "description": "WGS84",
                "mode": "nullable",
            },
            {
                "name": "longitude",
                "type": "float",
                "description": "WGS84",
                "mode": "nullable",
            },
            {
                "name": "location",
                "type": "string",
                "description": "Location formatted for mapping",
                "mode": "nullable",
            },
        ],
    )

    street_trees_transform_csv >> load_street_trees_to_bq
