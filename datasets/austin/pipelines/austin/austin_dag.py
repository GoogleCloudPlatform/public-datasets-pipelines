# Copyright 2022 Google LLC
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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="austin.austin",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="3 10 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    austin_bs_stations_source_data_to_gcs = bash.BashOperator(
        task_id="austin_bs_stations_source_data_to_gcs",
        bash_command="curl https://data.austintexas.gov/api/views/qd73-bsdg/rows.csv | gsutil cp - gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_stations_source.csv\n",
    )

    # Run CSV transform within kubernetes pod
    austin_bs_stations_process = kubernetes_pod.KubernetesPodOperator(
        task_id="austin_bs_stations_process",
        name="austin_bs_stations_process",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.austin.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://{{ var.value.composer_bucket }}/data/austin/austin_bs_stations_source.csv",
            "SOURCE_FILE": "files/austin_bs_stations_source.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/austin/bikeshare_stations_batch",
            "PIPELINE_NAME": "Austin Bikeshare Stations",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATE_FORMAT_LIST": '[\n  ["modified_date", "%m/%d/%Y %H:%M:%S %p", "%Y-%m-%d %H:%M:%S"]\n]',
            "NULL_ROWS_LIST": '[\n  "station_id"\n]',
            "INPUT_CSV_HEADERS": '[\n  "Kiosk ID",\n  "Kiosk Name",\n  "Kiosk Status",\n  "Location",\n  "Address",\n  "Alternate Name",\n  "City Asset Number",\n  "Property Type",\n  "Number of Docks",\n  "Power Type",\n  "Footprint Length",\n  "Footprint Width",\n  "Notes",\n  "Council District",\n  "Image",\n  "Modified Date"\n]',
            "DATA_DTYPES": '{\n  "station_id": "str",\n  "name": "str",\n  "status": "str",\n  "location": "str",\n  "address": "str",\n  "alternate_name": "str",\n  "city_asset_number": "str",\n  "property_type": "str",\n  "number_of_docks": "str",\n  "power_type": "str",\n  "footprint_length": "str",\n  "footprint_width": "str",\n  "notes": "str",\n  "council_district": "str",\n  "image": "str",\n  "modified_date": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "Kiosk ID": "station_id",\n  "Kiosk Name": "name",\n  "Kiosk Status": "status",\n  "Location": "location",\n  "Address": "address",\n  "Alternate Name": "alternate_name",\n  "City Asset Number": "city_asset_number",\n  "Property Type": "property_type",\n  "Number of Docks": "number_of_docks",\n  "Power Type": "power_type",\n  "Footprint Length": "footprint_length",\n  "Footprint Width": "footprint_width",\n  "Notes": "notes",\n  "Council District": "council_district",\n  "Image": "image",\n  "Modified Date": "modified_date"\n}',
            "REORDER_HEADERS_LIST": '[\n  "station_id",\n  "name",\n  "status",\n  "location",\n  "address",\n  "alternate_name",\n  "city_asset_number",\n  "property_type",\n  "number_of_docks",\n  "power_type",\n  "footprint_length",\n  "footprint_width",\n  "notes",\n  "council_district",\n  "image",\n  "modified_date"\n]',
        },
    )

    # Task to load CSV data to a BigQuery table
    load_full_to_bq_bs_stations = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_full_to_bq_bs_stations",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/austin/bikeshare_stations_batch/austin_bs_stations_output-*.csv"
        ],
        source_format="CSV",
        field_delimiter="|",
        destination_project_dataset_table="austin_bikeshare.bikeshare_stations",
        skip_leading_rows=1,
        ignore_unknown_values=True,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_object="data/austin/schema/austin_bikeshare_stations_schema.json",
    )

    (
        austin_bs_stations_source_data_to_gcs
        >> austin_bs_stations_process
        >> load_full_to_bq_bs_stations
    )
