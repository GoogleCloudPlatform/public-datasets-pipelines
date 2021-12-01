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
    dag_id="san_francisco_bikeshare.bikeshare_regions",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="bikeshare_trips",
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
        image="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_regions }}",
        env_vars={
            "SOURCE_URL_JSON": "https://gbfs.baywheels.com/gbfs/es/system_regions",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_bikeshare/bikeshare_regions/data_output.csv",
            "LOGGING_ENGLISH_NAME": "San francisco bikeshare regions",
            "TRANSFORM_LIST": '[ "rename_headers", "filter_empty_data", "reorder_headers" ]',
            "REORDER_HEADERS": '[ "region_id", "name" ]',
            "RENAME_HEADERS": '{ "data.regions.region_id": "region_id", "data.regions.name": "name" }',
            "GEOM_FIELD_LIST": "[ [ ] ]",
            "JSON_NODE_NAME": "regions",
            "FIELD_TYPE_LIST": "[ [ ] ]",
            "FILTER_ROWS_LIST": '[ [ "region_id", "name" ] ]',
        },
        resources={"limit_memory": "4G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/san_francisco_bikeshare/bikeshare_regions/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.san_francisco_bikeshare.container_registry.bikeshare_regions_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "region_id",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Unique identifier for the region",
            },
            {
                "name": "name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "Public name for this region",
            },
        ],
    )

    transform_csv >> load_to_bq
