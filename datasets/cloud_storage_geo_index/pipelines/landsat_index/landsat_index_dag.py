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
    dag_id="cloud_storage_geo_index.landsat_index",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    landsat_index_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="landsat_index_transform_csv",
        startup_timeout_seconds=600,
        name="landsat_index",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cloud_storage_geo_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/gcp-public-data-landsat/index.csv.gz",
            "SOURCE_FILE": "files/data.csv.gz",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1000000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cloud_storage_geo_index/landsat_index/data_output.csv",
            "PIPELINE_NAME": "landsat_index",
            "CSV_HEADERS": '["scene_id","product_id","spacecraft_id","sensor_id","date_acquired","sensing_time","collection_number","collection_category","data_type","wrs_path","wrs_row","cloud_cover","north_lat","south_lat","west_lon","east_lon","total_size","base_url"]',
            "RENAME_MAPPINGS": '{"SCENE_ID" : "scene_id","SPACECRAFT_ID" : "spacecraft_id","SENSOR_ID" : "sensor_id","DATE_ACQUIRED" : "date_acquired","COLLECTION_NUMBER" : "collection_number","COLLECTION_CATEGORY" : "collection_category","DATA_TYPE" : "data_type","WRS_PATH" : "wrs_path","WRS_ROW" : "wrs_row","CLOUD_COVER" : "cloud_cover","NORTH_LAT" : "north_lat","SOUTH_LAT" : "south_lat","WEST_LON" : "west_lon","EAST_LON" : "east_lon","TOTAL_SIZE" : "total_size","BASE_URL" : "base_url","PRODUCT_ID" : "product_id","SENSING_TIME" : "sensing_time"}',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_landsat_index_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_landsat_index_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/cloud_storage_geo_index/landsat_index/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="cloud_storage_geo_index.landsat_index",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "scene_id", "type": "STRING", "mode": "required"},
            {"name": "product_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "spacecraft_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "sensor_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "date_acquired", "type": "DATE", "mode": "NULLABLE"},
            {"name": "sensing_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "collection_number", "type": "STRING", "mode": "NULLABLE"},
            {"name": "collection_category", "type": "STRING", "mode": "NULLABLE"},
            {"name": "data_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "wrs_path", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "wrs_row", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cloud_cover", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "north_lat", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "south_lat", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "west_lon", "type": "FLOAt", "mode": "NULLABLE"},
            {"name": "east_lon", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "total_size", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "base_url", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    landsat_index_transform_csv >> load_landsat_index_to_bq
