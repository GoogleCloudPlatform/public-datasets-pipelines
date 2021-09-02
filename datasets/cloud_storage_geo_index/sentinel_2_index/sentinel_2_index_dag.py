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
    dag_id="cloud_storage_geo_index.sentinel_2_index",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    sentinel_2_index_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="sentinel_2_index_transform_csv",
        startup_timeout_seconds=600,
        name="sentinel_2_index",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.cloud_storage_geo_index.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://storage.googleapis.com/gcp-public-data-sentinel-2/index.csv.gz",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cloud_storage_geo_index/sentinel_2_index/data_output.csv",
            "CSV_HEADERS": '["invoice_and_item_number","date","store_number","store_name","address","city","zip_code","store_location","county_number","county","category","category_name","vendor_number","vendor_name","item_number","item_description","pack","bottle_volume_ml","state_bottle_cost","state_bottle_retail","bottles_sold","sale_dollars","volume_sold_liters","volume_sold_gallons"]',
            "RENAME_MAPPINGS": '{"Invoice/Item Number" : "invoice_and_item_number","Date" : "date","Store Number" : "store_number","Store Name" : "store_name","Address" : "address","City" : "city","Zip Code" : "zip_code","Store Location" : "store_location","County Number" : "county_number","County" : "county","Category" : "category","Category Name" : "category_name","Vendor Number" : "vendor_number","Vendor Name" : "vendor_name","Item Number" : "item_number","Item Description" : "item_description","Pack" : "pack","Bottle Volume (ml)" : "bottle_volume_ml","State Bottle Cost" : "state_bottle_cost","State Bottle Retail" : "state_bottle_retail","Bottles Sold" : "bottles_sold","Sale (Dollars)" : "sale_dollars","Volume Sold (Liters)" : "volume_sold_liters","Volume Sold (Gallons)" : "volume_sold_gallons"}',
        },
        resources={"limit_memory": "4G", "limit_cpu": "2"},
    )

    # Task to load CSV data to a BigQuery table
    load_sentinel_2_index_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_sentinel_2_index_to_bq",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/cloud_storage_geo_index/sentinel_2_index/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="cloud_storage_geo_index.sentinel_2_index",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "granule_id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "product_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datatake_identifier", "type": "STRING", "mode": "NULLABLE"},
            {"name": "mgrs_tile", "type": "STRING", "mode": "NULLABLE"},
            {"name": "sensing_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "geometric_quality_flag", "type": "STRING", "mode": "NULLABLE"},
            {"name": "generation_time", "type": "TIMSTAMP", "mode": "NULLABLE"},
            {"name": "north_lat", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "south_lat", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "west_lon", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "east_lon", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "base_url", "type": "STRING", "mode": "NULLABLE"},
            {"name": "total_size", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cloud_cover", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    sentinel_2_index_transform_csv >> load_sentinel_2_index_to_bq
