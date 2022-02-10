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
    dag_id="austin_bikeshare.bikeshare_stations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    austin_bikeshare_stations_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_bikeshare_stations_transform_csv",
        name="bikeshare_stations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.austin_bikeshare.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.austintexas.gov/api/views/qd73-bsdg/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin_bikeshare/bikeshare_stations/data_output.csv",
            "PIPELINE_NAME": "bikeshare_stations",
            "CSV_HEADERS": '["station_id","name","status","address","alternate_name","city_asset_number","property_type","number_of_docks","power_type","footprint_length","footprint_width","notes","council_district","modified_date"]',
            "RENAME_MAPPINGS": '{"Kiosk ID": "station_id","Kiosk Name": "name","Kiosk Status": "status","Address": "address","Alternate Name": "alternate_name","City Asset Number": "city_asset_number","Property Type": "property_type","Number of Docks": "number_of_docks","Power Type": "power_type","Footprint Length": "footprint_length","Footprint Width": "footprint_width","Notes": "notes","Council District": "council_district","Modified Date": "modified_date"}',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_austin_bikeshare_stations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_austin_bikeshare_stations_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/austin_bikeshare/bikeshare_stations/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="austin_bikeshare.bikeshare_stations",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "station_id", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "status", "type": "STRING", "mode": "NULLABLE"},
            {"name": "address", "type": "STRING", "mode": "NULLABLE"},
            {"name": "alternate_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "city_asset_number", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "property_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "number_of_docks", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "power_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "footprint_length", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "footprint_width", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "notes", "type": "STRING", "mode": "NULLABLE"},
            {"name": "council_district", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "modified_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ],
    )

    austin_bikeshare_stations_transform_csv >> load_austin_bikeshare_stations_to_bq
