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
    dag_id="san_francisco_film_locations.film_locations",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="film_locations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.san_francisco_film_locations.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.sfgov.org/api/views/yitu-d5am/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/san_francisco_film_locations/film_locations/data_output.csv",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/san_francisco_film_locations/film_locations/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="san_francisco_film_locations.film_locations",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "title", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "release_year",
                "type": "INTEGER",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "locations",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "fun_facts",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "production_company",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "distributor",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "director",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {"name": "writer", "type": "STRING", "description": "", "mode": "NULLABLE"},
            {
                "name": "actor_1",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "actor_2",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "actor_3",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
