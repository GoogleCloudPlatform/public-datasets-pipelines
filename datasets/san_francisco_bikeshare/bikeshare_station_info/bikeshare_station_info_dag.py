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
    dag_id="san_francisco_bikeshare.bikeshare_station_info",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="bikeshare_station_info",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_station_info }}",
        env_vars={
            "SOURCE_URL_JSON": "https://gbfs.baywheels.com/gbfs/fr/station_information",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_bikeshare/bikeshare_station_info/data_output.csv",
            "LOGGING_ENGLISH_NAME": "San francisco bikeshare station info",
            "TRANSFORM_LIST": '[ "rename_headers", "filter_empty_data", "generate_location", "resolve_datatypes", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "station_id", "name", "short_name", "lat", "lon",\n  "region_id", "rental_methods", "capacity", "external_id", "eightd_has_key_dispenser",\n  "has_kiosk", "station_geom" ]',
            "RENAME_HEADERS": '{ "data.stations.station_id": "station_id", "data.stations.name": "name",\n  "data.stations.short_name": "short_name", "data.stations.lat": "lat",\n  "data.stations.lon": "lon", "data.stations.region_id": "region_id",\n  "data.stations.rental_methods": "rental_methods", "data.stations.capacity": "capacity",\n  "data.stations.eightd_has_key_dispenser": "eightd_has_key_dispenser", "data.stations.has_kiosk": "has_kiosk",\n  "data.stations.external_id": "external_id" }',
            "GEOM_FIELD_LIST": '[ [ "station_geom", "lat", "lon" ] ]',
            "JSON_NODE_NAME": "stations",
            "FIELD_TYPE_LIST": '[ [ "region_id", "Int64" ] ]',
            "FILTER_ROWS_LIST": '[ [ "station_id", "name", "lat", "lon"] ]',
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/san_francisco_bikeshare/bikeshare_station_info/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_station_info_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "station_id",
                "type": "INTEGER",
                "description": "Unique identifier of a station.",
                "mode": "REQUIRED",
            },
            {
                "name": "name",
                "type": "STRING",
                "description": "Public name of the station",
                "mode": "REQUIRED",
            },
            {
                "name": "short_name",
                "type": "STRING",
                "description": "Short name or other type of identifier, as used by the data publisher",
                "mode": "NULLABLE",
            },
            {
                "name": "lat",
                "type": "FLOAT",
                "description": "The latitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format. See: http://en.wikipedia.org/wiki/World_Geodetic_System, https://en.wikipedia.org/wiki/Decimal_degrees",
                "mode": "REQUIRED",
            },
            {
                "name": "lon",
                "type": "FLOAT",
                "description": "The longitude of station. The field value must be a valid WGS 84 longitude in decimal degrees format. See: http://en.wikipedia.org/wiki/World_Geodetic_System, https://en.wikipedia.org/wiki/Decimal_degrees",
                "mode": "REQUIRED",
            },
            {
                "name": "region_id",
                "type": "INTEGER",
                "description": "ID of the region where station is located",
                "mode": "NULLABLE",
            },
            {
                "name": "rental_methods",
                "type": "STRING",
                "description": "Array of enumerables containing the payment methods accepted at this station.  Current valid values (in CAPS) are: KEY (i.e. operator issued bike key / fob / card) CREDITCARD PAYPASS APPLEPAY ANDROIDPAY TRANSITCARD ACCOUNTNUMBER PHONE This list is intended to be as comprehensive at the time of publication as possible but is subject to change, as defined in File Requirements above",
                "mode": "NULLABLE",
            },
            {
                "name": "capacity",
                "type": "INTEGER",
                "description": "Number of total docking points installed at this station, both available and unavailable",
                "mode": "NULLABLE",
            },
            {
                "name": "external_id",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "eightd_has_key_dispenser",
                "type": "BOOLEAN",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "has_kiosk",
                "type": "BOOLEAN",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "station_geom",
                "type": "GEOGRAPHY",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
